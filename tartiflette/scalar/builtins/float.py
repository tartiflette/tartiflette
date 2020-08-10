from math import isfinite
from typing import Any, Dict, Optional

from tartiflette import Scalar
from tartiflette.language.ast import FloatValueNode, IntValueNode
from tartiflette.types.exceptions.tartiflette import TartifletteError
from tartiflette.utils.errors import graphql_error_from_nodes


class ScalarFloat:
    """
    Built-in scalar which handle float values.
    """

    def coerce_output(self, value: Any) -> float:
        """
        Coerce the resolved value for output.
        :param value: value to coerce
        :type value: Any
        :return: the coerced value
        :rtype: float
        """
        # pylint: disable=no-self-use
        try:
            result = value
            if value and isinstance(value, str):
                result = float(value)

            if not isfinite(result):
                raise ValueError()

            return result if isinstance(result, float) else float(result)
        except Exception:  # pylint: disable=broad-except
            pass

        raise TartifletteError(
            f"Float cannot represent non numeric value: < {value} >."
        )

    def coerce_input(self, value: Any) -> float:
        """
        Coerce the user input from variable value.
        :param value: value to coerce
        :type value: Any
        :return: the coerced value
        :rtype: float
        """
        # pylint: disable=no-self-use
        # ¯\_(ツ)_/¯ booleans are int: `assert isinstance(True, int) is True`
        try:
            if not isinstance(value, bool) and isfinite(value):
                return float(value)
        except Exception:  # pylint: disable=broad-except
            pass

        raise TartifletteError(
            f"Float cannot represent non numeric value: < {value} >."
        )

    def parse_literal(self, ast: "Node") -> float:
        """
        Coerce the input value from an AST node.
        :param ast: AST node to coerce
        :type ast: Node
        :return: the coerced value
        :rtype: float
        """
        # pylint: disable=no-self-use
        if isinstance(ast, (FloatValueNode, IntValueNode)):
            return float(ast.value)

        raise graphql_error_from_nodes(
            f"Float cannot represent non numeric value: {ast}.", nodes=[ast],
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
    Scalar("Float", schema_name=schema_name)(ScalarFloat())
    return '''
    """The `Float` scalar type represents signed double-precision fractional values as specified by [IEEE 754](https://en.wikipedia.org/wiki/IEEE_floating_point)."""
    scalar Float
    '''
