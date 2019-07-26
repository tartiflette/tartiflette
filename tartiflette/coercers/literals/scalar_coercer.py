from typing import Any, Dict, Optional, Union

from tartiflette.coercers.common import CoercionResult
from tartiflette.coercers.literals.null_and_variable_coercer import (
    null_and_variable_coercer_wrapper,
)
from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.utils.values import is_invalid_value

__all__ = ("scalar_coercer",)


@null_and_variable_coercer_wrapper
async def scalar_coercer(
    node: Union["ValueNode", "VariableNode"],
    ctx: Optional[Any],
    scalar_type: "GraphQLScalarType",
    variables: Optional[Dict[str, Any]] = None,
    path: Optional["Path"] = None,
) -> "CoercionResult":
    """
    Computes the value of a scalar.
    :param node: the AST node to treat
    :param ctx: context passed to the query execution
    :param scalar_type: the GraphQLScalarType instance of the scalar
    :param variables: the variables provided in the GraphQL request
    :param path: the path traveled until this coercer
    :type node: Union[ValueNode, VariableNode]
    :type ctx: Optional[Any]
    :type scalar_type: GraphQLScalarType
    :type variables: Optional[Dict[str, Any]]
    :type path: Optional[Path]
    :return: the computed value
    :rtype: CoercionResult
    """
    # pylint: disable=unused-argument
    try:
        value = scalar_type.parse_literal(node)
        if not is_invalid_value(value):
            return CoercionResult(value=value)
    except Exception:  # pylint: disable=broad-except
        pass
    return CoercionResult(value=UNDEFINED_VALUE)
