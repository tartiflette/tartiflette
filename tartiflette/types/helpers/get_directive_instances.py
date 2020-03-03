from functools import partial
from typing import Any, Callable, Dict, List, Optional

from tartiflette.coercers.arguments import coerce_arguments
from tartiflette.utils.callables import (
    is_valid_async_generator,
    is_valid_coroutine,
)

__all__ = ("compute_directive_nodes",)


def get_callables(implementation: Any) -> Dict[str, Callable]:
    """
    Computes a dictionary of all attribute name that starts with `on_` and are
    linked to a callable.
    :param implementation: the implementation to parse
    :type implementation: Any
    :return: a dictionary of attribute name and callable
    :rtype: Dict[str, Callable]
    """
    return {
        key: getattr(implementation, key)
        for key in dir(implementation)
        if key.startswith("on_")
        and (
            is_valid_coroutine(getattr(implementation, key))
            or is_valid_async_generator(getattr(implementation, key))
        )
    }


def transform_directive(
    directive: "GraphQLDirective", arguments_coercer: Callable
) -> Dict[str, Any]:
    """
    Transforms a directive definition into a dictionary of available callables
    hooks and with default arguments.
    :param directive: the directive definition to transform
    :param arguments_coercer: callable to use to coerce directive arguments
    :type directive: GraphQLDirective
    :type arguments_coercer: Callable
    :return: the transformed directive definition
    :rtype: Dict[str, Any]
    """
    return {
        "callables": get_callables(directive.implementation),
        "arguments_coercer": arguments_coercer,
    }


def compute_directive_nodes(
    schema: "GraphQLSchema",
    directive_nodes: List["DirectiveNode"],
    variable_values: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """
    Computes a list of AST directive node into a list of pre-computed
    directives.
    :param schema: the GraphQLSchema instance linked to the engine
    :param directive_nodes: list of AST directive node to compute
    :param variable_values: the variables provided in the GraphQL request
    :type schema: GraphQLSchema
    :type directive_nodes: List[DirectiveNode]
    :type variable_values: Optional[Dict[str, Any]]
    :return: list of pre-computed directives
    :rtype: List[Dict[str, Any]]
    """
    if not directive_nodes:
        return []

    computed_directives = []
    for directive_node in directive_nodes:
        directive_definition = schema.find_directive(directive_node.name.value)
        computed_directives.append(
            transform_directive(
                directive_definition,
                arguments_coercer=partial(
                    coerce_arguments,
                    argument_definitions=directive_definition.arguments,
                    node=directive_node,
                    variable_values=variable_values or {},
                    coercer=directive_definition.arguments_coercer,
                ),
            )
        )
    return computed_directives
