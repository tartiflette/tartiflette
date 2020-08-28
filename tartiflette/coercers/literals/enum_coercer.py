from typing import Any, Dict, Optional, Union

from tartiflette.coercers.common import CoercionResult
from tartiflette.coercers.literals.null_and_variable_coercer import (
    null_and_variable_coercer_wrapper,
)
from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import EnumValueNode

__all__ = ("enum_coercer",)


@null_and_variable_coercer_wrapper
async def enum_coercer(
    parent_node: Union["VariableDefinitionNode", "InputValueDefinitionNode"],
    node: Union["ValueNode", "VariableNode"],
    ctx: Optional[Any],
    enum_type: "GraphQLEnumType",
    variables: Optional[Dict[str, Any]] = None,
    path: Optional["Path"] = None,
) -> "CoercionResult":
    """
    Computes the value of an enum.
    :param parent_node: the root parent AST node
    :param node: the AST node to treat
    :param ctx: context passed to the query execution
    :param enum_type: the GraphQLEnumType instance of the enum
    :param variables: the variables provided in the GraphQL request
    :param path: the path traveled until this coercer
    :type parent_node: Union[VariableDefinitionNode, InputValueDefinitionNode]
    :type node: Union[ValueNode, VariableNode]
    :type ctx: Optional[Any]
    :type enum_type: GraphQLEnumType
    :type variables: Optional[Dict[str, Any]]
    :type path: Optional[Path]
    :return: the computed value
    :rtype: CoercionResult
    """
    # pylint: disable=unused-argument
    if not isinstance(node, EnumValueNode):
        return CoercionResult(value=UNDEFINED_VALUE)

    try:
        enum_value = enum_type.get_value(node.value)
        return CoercionResult(
            value=await enum_value.literal_coercer(
                parent_node, enum_value.definition, node.value, ctx
            )
        )
    except KeyError:
        pass
    return CoercionResult(value=UNDEFINED_VALUE)
