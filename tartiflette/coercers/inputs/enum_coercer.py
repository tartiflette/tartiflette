from difflib import get_close_matches
from typing import Any, Optional, Union

from tartiflette.coercers.common import CoercionResult, coercion_error
from tartiflette.coercers.inputs.null_coercer import null_coercer_wrapper
from tartiflette.utils.errors import did_you_mean

__all__ = ("enum_coercer",)


@null_coercer_wrapper
async def enum_coercer(
    parent_node: Union["VariableDefinitionNode", "InputValueDefinitionNode"],
    node: "Node",
    value: Any,
    ctx: Optional[Any],
    enum_type: "GraphQLEnumType",
    path: Optional["Path"] = None,
) -> "CoercionResult":
    """
    Computes the value of an enum.
    :param parent_node: the root parent AST node
    :param node: the AST node to treat
    :param value: the raw value to compute
    :param ctx: context passed to the query execution
    :param enum_type: the GraphQLEnumType instance of the enum
    :param path: the path traveled until this coercer
    :type parent_node: Union[VariableDefinitionNode, InputValueDefinitionNode]
    :type node: Node
    :type value: Any
    :type ctx: Optional[Any]
    :type enum_type: GraphQLEnumType
    :type path: Optional[Path]
    :return: the coercion result
    :rtype: CoercionResult
    """
    try:
        enum_value = enum_type.get_value(value)
        return CoercionResult(
            value=await enum_value.input_coercer(
                parent_node, enum_value.definition, value, ctx
            )
        )
    except Exception:  # pylint: disable=broad-except
        return CoercionResult(
            errors=[
                coercion_error(
                    f"Expected type < {enum_type.name} >",
                    node,
                    path,
                    did_you_mean(
                        get_close_matches(
                            str(value),
                            [enum.value for enum in enum_type.values],
                            n=5,
                        )
                    ),
                )
            ]
        )
