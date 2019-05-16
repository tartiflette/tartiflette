from typing import Any, Optional

from tartiflette.coercers.common import CoercionResult, coercion_error
from tartiflette.coercers.inputs.null_coercer import null_coercer_wrapper

__all__ = ("enum_coercer",)


@null_coercer_wrapper
async def enum_coercer(
    node: "Node",
    value: Any,
    ctx: Optional[Any],
    enum_type: "GraphQLEnumType",
    path: Optional["Path"] = None,
) -> "CoercionResult":
    """
    Computes the value of an enum.
    :param node: the AST node to treat
    :param value: the raw value to compute
    :param ctx: context passed to the query execution
    :param enum_type: the GraphQLEnumType instance of the enum
    :param path: the path traveled until this coercer
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
        return CoercionResult(value=await enum_value.input_coercer(value, ctx))
    except Exception:  # pylint: disable=broad-except
        # TODO: try to compute a suggestion list of valid values depending
        # on the invalid value sent and returns it as error sub message
        return CoercionResult(
            errors=[
                coercion_error(
                    f"Expected type < {enum_type.name} >", node, path
                )
            ]
        )
