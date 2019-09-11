from typing import Any, Callable, Dict, Optional, Union

from tartiflette.coercers.common import CoercionResult
from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import NullValueNode, VariableNode
from tartiflette.utils.values import is_invalid_value

__all__ = ("null_and_variable_coercer_wrapper",)


def null_and_variable_coercer_wrapper(coercer: Callable) -> Callable:
    """
    Factorization of the treatment making it possible to coerce a NullValueNode
    or a VariableNode.
    :param coercer: the pre-computed coercer to use on the value if not a
    NullValueNode neither a VariableNode
    :type coercer: Callable
    :return: the wrapped coercer
    :rtype: Callable
    """

    async def wrapper(
        parent_node: Union[
            "VariableDefinitionNode", "InputValueDefinitionNode"
        ],
        node: "Node",
        ctx: Optional[Any],
        variables: Optional[Dict[str, Any]] = None,
        is_non_null_type: bool = False,
        **kwargs,
    ) -> "CoercionResult":
        """
        Computes the value if null or variable.
        :param parent_node: the root parent AST node
        :param node: the AST node to treat
        :param ctx: context passed to the query execution
        :param variables: the variables provided in the GraphQL request
        :param is_non_null_type: determines whether or not the value is
        nullable
        :type parent_node: Union[VariableDefinitionNode, InputValueDefinitionNode]
        :type node: Union[ValueNode, VariableNode]
        :type ctx: Optional[Any]
        :type variables: Optional[Dict[str, Any]]
        :type is_non_null_type: bool
        :return: the computed value
        :rtype: CoercionResult
        """
        if not node:
            return CoercionResult(value=UNDEFINED_VALUE)

        if isinstance(node, NullValueNode):
            return CoercionResult(value=None)

        if isinstance(node, VariableNode):
            if not variables:
                return CoercionResult(value=UNDEFINED_VALUE)

            value = variables.get(node.name.value, UNDEFINED_VALUE)
            if is_invalid_value(value) or (value is None and is_non_null_type):
                return CoercionResult(value=UNDEFINED_VALUE)
            return CoercionResult(value=value)

        return await coercer(
            parent_node, node, ctx, variables=variables, **kwargs
        )

    return wrapper
