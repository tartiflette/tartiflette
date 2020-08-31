from typing import Any, Dict, Optional

from tartiflette import Scalar
from tartiflette.language.ast import IntValueNode
from tartiflette.types.exceptions.tartiflette import TartifletteError
from tartiflette.utils.errors import graphql_error_from_nodes
from tartiflette.utils.values import is_integer

_MIN_INT = -2_147_483_648
_MAX_INT = 2_147_483_647


class ScalarInt:
    """
    Built-in scalar which handle int values.
    """

    def coerce_output(self, value: Any) -> int:
        """
        Coerce the resolved value for output.
        :param value: value to coerce
        :type value: Any
        :return: the coerced value
        :rtype: int
        """
        # pylint: disable=no-self-use
        if isinstance(value, bool):
            return int(value)

        try:
            result = value
            if value and isinstance(value, str):
                float_value = float(value)
                result = int(float_value)
                if result != float_value:
                    raise ValueError()

            if not is_integer(result):
                raise ValueError()
        except Exception:  # pylint: disable=broad-except
            raise TartifletteError(
                f"Int cannot represent non-integer value: < {value} >."
            )

        if not _MIN_INT <= result <= _MAX_INT:
            raise TartifletteError(
                "Int cannot represent non 32-bit signed integer value: "
                f"< {value} >."
            )
        return result

    def coerce_input(self, value: Any) -> int:
        """
        Coerce the user input from variable value.
        :param value: value to coerce
        :type value: Any
        :return: the coerced value
        :rtype: int
        """
        # pylint: disable=no-self-use
        # ¯\_(ツ)_/¯ booleans are int: `assert isinstance(True, int) is True`
        if not is_integer(value):
            raise TartifletteError(
                f"Int cannot represent non-integer value: < {value} >."
            )
        if not _MIN_INT <= value <= _MAX_INT:
            raise TartifletteError(
                "Int cannot represent non 32-bit signed integer value: "
                f"< {value} >."
            )
        return int(value)

    def parse_literal(self, ast: "Node") -> int:
        """
        Coerce the input value from an AST node.
        :param ast: AST node to coerce
        :type ast: Node
        :return: the coerced value
        :rtype: int
        """
        # pylint: disable=no-self-use
        if isinstance(ast, IntValueNode):
            value = int(ast.value)
            if _MIN_INT <= value <= _MAX_INT:
                return value

            raise graphql_error_from_nodes(
                "Int cannot represent non 32-bit signed integer value: "
                f"{ast.value}.",
                nodes=[ast],
            )

        raise graphql_error_from_nodes(
            f"Int cannot represent non-integer value: {ast}.", nodes=[ast]
        )


def bake(schema_name: str, config: Optional[Dict[str, Any]] = None) -> str:
    """
    Links the scalar to the appropriate schema and returns the SDL related
    to the scalar.
    :param schema_name: schema name to link with
    :param config: configuration of the scalar
    :type schema_name: str
    :type config: Optional[Dict[str, Any]]
    :return: the SDL related to the scalar
    :rtype: str
    """
    # pylint: disable=unused-argument
    Scalar("Int", schema_name=schema_name)(ScalarInt())
    return '''
    """The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1."""
    scalar Int
    '''
