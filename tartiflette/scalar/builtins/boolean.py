from typing import Any, Dict, Optional, Union

from tartiflette import Scalar
from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import BooleanValueNode


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
        return bool(value)

    def coerce_input(self, value: Any) -> bool:
        """
        Coerce the user input from variable value.
        :param value: value to coerce
        :type value: Any
        :return: the coerced value
        :rtype: bool
        """
        # pylint: disable=no-self-use
        if not isinstance(value, bool):
            raise TypeError(
                f"Boolean cannot represent a non boolean value: < {value} >."
            )
        return value

    def parse_literal(self, ast: "Node") -> Union[bool, "UNDEFINED_VALUE"]:
        """
        Coerce the input value from an AST node.
        :param ast: AST node to coerce
        :type ast: Node
        :return: the coerced value
        :rtype: Union[bool, UNDEFINED_VALUE]
        """
        # pylint: disable=no-self-use
        return (
            ast.value if isinstance(ast, BooleanValueNode) else UNDEFINED_VALUE
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
