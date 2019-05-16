from typing import Any, Dict, Optional, Union

from tartiflette import Scalar
from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import IntValueNode

_MAX_INT = 2_147_483_647
_MIN_INT = -2_147_483_648


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
        return int(value)

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
        if not isinstance(value, int) or isinstance(value, bool):
            raise TypeError(
                f"Int cannot represent non-integer value: < {value} >"
            )
        if not _MIN_INT <= value <= _MAX_INT:
            raise TypeError(
                "Int cannot represent non 32-bit signed integer value: "
                f"< {value} >"
            )
        return value

    def parse_literal(self, ast: "Node") -> Union[int, "UNDEFINED_VALUE"]:
        """
        Coerce the input value from an AST node.
        :param ast: AST node to coerce
        :type ast: Node
        :return: the coerced value
        :rtype: Union[int, UNDEFINED_VALUE]
        """
        # pylint: disable=no-self-use
        if not isinstance(ast, IntValueNode):
            return UNDEFINED_VALUE

        try:
            value = int(ast.value)
            if _MIN_INT <= value <= _MAX_INT:
                return value
        except Exception:  # pylint: disable=broad-except
            pass
        return UNDEFINED_VALUE


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
