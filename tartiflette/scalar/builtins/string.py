from typing import Any, Dict, Optional

from tartiflette import Scalar
from tartiflette.language.ast import StringValueNode
from tartiflette.types.exceptions.tartiflette import TartifletteError
from tartiflette.utils.errors import graphql_error_from_nodes


class ScalarString:
    """
    Built-in scalar which handle string values.
    """

    def coerce_output(self, value: Any) -> str:
        """
        Coerce the resolved value for output.
        :param value: value to coerce
        :type value: Any
        :return: the coerced value
        :rtype: str
        """
        # pylint: disable=no-self-use
        if isinstance(value, str):
            return value

        if isinstance(value, bool):
            return "true" if value else "false"

        try:
            # TODO: maybe we shouldn't accepts None, list, dict, exceptions...
            return str(value)
        except Exception:  # pylint: disable=broad-except
            pass

        raise TartifletteError(f"String cannot represent value: < {value} >.")

    def coerce_input(self, value: Any) -> str:
        """
        Coerce the user input from variable value.
        :param value: value to coerce
        :type value: Any
        :return: the coerced value
        :rtype: str
        """
        # pylint: disable=no-self-use
        if isinstance(value, str):
            return value

        raise TartifletteError(
            f"String cannot represent a non string value: < {value} >."
        )

    def parse_literal(self, ast: "Node") -> str:
        """
        Coerce the input value from an AST node.
        :param ast: AST node to coerce
        :type ast: Node
        :return: the coerced value
        :rtype: str
        """
        # pylint: disable=no-self-use
        if isinstance(ast, StringValueNode):
            return ast.value

        raise graphql_error_from_nodes(
            f"String cannot represent a non string value: {ast}.", nodes=[ast],
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
    Scalar("String", schema_name=schema_name)(ScalarString())
    return '''
    """The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text."""
    scalar String
    '''
