from math import isfinite
from typing import Any, Dict, Optional

from tartiflette import Scalar
from tartiflette.language.ast import BooleanValueNode
from tartiflette.types.exceptions.tartiflette import TartifletteError
from tartiflette.utils.errors import graphql_error_from_nodes


class ScalarBoolean:
    """
    Built-in scalar which handle boolean values.
    """

    def coerce_output(self, value: Any) -> bool:
        """
        Coerce the resolved value for output.
        :param value: value to coerce
        :type value: Any
        :return: the coerced value
        :rtype: bool
        """
        # pylint: disable=no-self-use
        if isinstance(value, bool):
            return value

        try:
            if isfinite(value):
                return bool(value)
        except Exception:  # pylint: disable=broad-except
            pass

        raise TartifletteError(
            f"Boolean cannot represent a non boolean value: < {value} >."
        )

    def coerce_input(self, value: Any) -> bool:
        """
        Coerce the user input from variable value.
        :param value: value to coerce
        :type value: Any
        :return: the coerced value
        :rtype: bool
        """
        # pylint: disable=no-self-use
        if isinstance(value, bool):
            return value

        raise TartifletteError(
            f"Boolean cannot represent a non boolean value: < {value} >."
        )

    def parse_literal(self, ast: "Node") -> bool:
        """
        Coerce the input value from an AST node.
        :param ast: AST node to coerce
        :type ast: Node
        :return: the coerced value
        :rtype: bool
        """
        # pylint: disable=no-self-use
        if isinstance(ast, BooleanValueNode):
            return ast.value

        raise graphql_error_from_nodes(
            f"Boolean cannot represent a non boolean value: {ast}.",
            nodes=[ast],
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
    Scalar("Boolean", schema_name=schema_name)(ScalarBoolean())
    return '''
    """The `Boolean` scalar type represents `true` or `false`."""
    scalar Boolean
    '''
