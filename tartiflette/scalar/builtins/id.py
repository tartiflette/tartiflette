from typing import Any, Dict, Optional, Union

from tartiflette import Scalar
from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import IntValueNode, StringValueNode
from tartiflette.utils.values import is_integer


class ScalarID:
    """
    Built-in scalar which handle ID values.
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

        if is_integer(value):
            return str(int(value))

        raise TypeError(f"ID cannot represent value: < {value} >.")

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

        if is_integer(value):
            return str(int(value))

        raise TypeError(f"ID cannot represent value: < {value} >.")

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
            ast.value
            if isinstance(ast, (StringValueNode, IntValueNode))
            else UNDEFINED_VALUE
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
    Scalar("ID", schema_name=schema_name)(ScalarID())
    return '''
    """The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID."""
    scalar ID
    '''
