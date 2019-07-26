from typing import Any, Dict, Union

from tartiflette.language.ast import VariableNode
from tartiflette.utils.values import is_invalid_value

__all__ = ("is_missing_variable",)


def is_missing_variable(
    value_node: Union["ValueNode", "VariableNode"], variables: Dict[str, Any]
) -> bool:
    """
    Determines whether or not the value node is a VariableNode without defined
    value.
    :param value_node: the AST node to treat
    :param variables: the variables provided in the GraphQL request
    :type value_node: Union[ValueNode, VariableNode]
    :type variables: Dict[str, Any]
    :return: whether or not the value node is a VariableNode without defined
    value
    :rtype: bool
    """
    return isinstance(value_node, VariableNode) and (
        not variables
        or value_node.name.value not in variables
        or is_invalid_value(variables[value_node.name.value])
    )
