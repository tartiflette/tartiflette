from datetime import datetime
from typing import Any, Dict, Optional

from tartiflette import Scalar
from tartiflette.language.ast import StringValueNode
from tartiflette.types.exceptions.tartiflette import TartifletteError

from ...utils.errors import graphql_error_from_nodes
from .string import ScalarString


class ScalarDate(ScalarString):
    """
    Built-in scalar which handle date values.
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
            return value.isoformat().split("T")[0]
        except Exception:  # pylint: disable=broad-except
            pass

        raise TartifletteError(f"Date cannot represent value: < {value} >.")

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
            return datetime.strptime(result, "%Y-%m-%d")
        except Exception:  # pylint: disable=broad-except
            pass

        raise TartifletteError(f"Date cannot represent value: < {value} >.")

    def parse_literal(self, ast: "Node") -> datetime:
        """
        Coerce the input value from an AST node.
        :param ast: AST node to coerce
        :type ast: Node
        :return: the coerced value
        :rtype: datetime
        """
        # pylint: disable=no-self-use
        if isinstance(ast, StringValueNode):
            try:
                return datetime.strptime(ast.value, "%Y-%m-%d")
            except Exception:  # pylint: disable=broad-except
                pass

        raise graphql_error_from_nodes(
            f"Date cannot represent value: {ast}.", nodes=[ast],
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
    Scalar("Date", schema_name=schema_name)(ScalarDate())
    return '''
    """The `Date` scalar type represents a date object"""
    scalar Date
    '''
