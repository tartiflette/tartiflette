from datetime import datetime
from typing import Any, Dict, Optional, Union

from tartiflette import Scalar
from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import StringValueNode

from .string import ScalarString


class ScalarDateTime(ScalarString):
    """
    Built-in scalar which handle date time values.
    """

    def coerce_output(self, value: datetime) -> str:
        """
        Coerce the resolved value for output.
        :param value: value to coerce
        :type value: datetime
        :return: the coerced value
        :rtype: str
        """
        # pylint: disable=no-self-use
        try:
            return value.isoformat()
        except Exception:  # pylint: disable=broad-except
            pass
        raise TypeError(f"DateTime cannot represent value: < {value} >.")

    def coerce_input(self, value: str) -> datetime:
        """
        Coerce the user input from variable value.
        :param value: value to coerce
        :type value: str
        :return: the coerced value
        :rtype: datetime
        """
        # pylint: disable=no-self-use
        try:
            result = super().coerce_input(value)
            return datetime.strptime(result, "%Y-%m-%dT%H:%M:%S")
        except Exception:  # pylint: disable=broad-except
            pass
        raise TypeError(f"DateTime cannot represent value: < {value} >.")

    def parse_literal(self, ast: "Node") -> Union[datetime, "UNDEFINED_VALUE"]:
        """
        Coerce the input value from an AST node.
        :param ast: AST node to coerce
        :type ast: Node
        :return: the coerced value
        :rtype: Union[datetime, UNDEFINED_VALUE]
        """
        # pylint: disable=no-self-use
        if not isinstance(ast, StringValueNode):
            return UNDEFINED_VALUE

        try:
            return datetime.strptime(ast.value, "%Y-%m-%dT%H:%M:%S")
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
    Scalar("DateTime", schema_name=schema_name)(ScalarDateTime())
    return '''
    """The `DateTime` scalar type represents a date time object"""
    scalar DateTime
    '''
