from typing import Any, Dict, Optional, Union

from tartiflette import Scalar
from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import StringValueNode


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
        return str(value)

    def coerce_input(self, value: Any) -> str:
        """
        Coerce the user input from variable value.
        :param value: value to coerce
        :type value: Any
        :return: the coerced value
        :rtype: str
        """
        # pylint: disable=no-self-use
        if not isinstance(value, str):
            raise TypeError(
                f"String cannot represent a non string value: < {value} >."
            )
        return value

    def parse_literal(self, ast: "Node") -> Union[str, "UNDEFINED_VALUE"]:
        """
        Coerce the input value from an AST node.
        :param ast: AST node to coerce
        :type ast: Node
        :return: the coerced value
        :rtype: Union[str, UNDEFINED_VALUE]
        """
        # pylint: disable=no-self-use
        return (
            ast.value if isinstance(ast, StringValueNode) else UNDEFINED_VALUE
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
