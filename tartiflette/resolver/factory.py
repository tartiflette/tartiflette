from typing import Any, Callable, List, Union

from tartiflette.coercers.arguments import coerce_arguments
from tartiflette.coercers.outputs.common import complete_value_catching_error
from tartiflette.execution.types import build_resolve_info
from tartiflette.types.helpers.get_directive_instances import (
    compute_directive_nodes,
)
from tartiflette.utils.directives import (
    introspection_directives_executor,
    wraps_with_directives,
)

__all__ = ("resolve_field",)


async def resolve_field_value_or_error(
    execution_context: "ExecutionContext",
    field_definition: "GraphQLField",
    field_nodes: List["FieldNode"],
    resolver: Callable,
    source: Any,
    info: "ResolveInfo",
) -> Union[Exception, Any]:
    """
    Coerce the field's arguments and then try to resolve the field.
    :param execution_context: instance of the query execution context
    :param field_definition: GraphQLField instance of the resolved field
    :param field_nodes: AST nodes related to the resolved field
    :param resolver: callable to use to resolve the field
    :param source: default root value or field parent value
    :param info: information related to the execution and the resolved field
    :type execution_context: ExecutionContext
    :type field_definition: GraphQLField
    :type field_nodes: List[FieldNode]
    :type resolver: Callable
    :type source: Any
    :type info: ResolveInfo
    :return: the resolved field value
    :rtype: Union[Exception, Any]
    """
    # pylint: disable=too-many-locals
    try:
        computed_directives = []
        for field_node in field_nodes:
            computed_directives.extend(
                compute_directive_nodes(
                    execution_context.schema,
                    field_node.directives,
                    execution_context.variable_values,
                )
            )

        if computed_directives:
            resolver = wraps_with_directives(
                directives_definition=computed_directives,
                directive_hooks=["on_field_execution"],
                func=resolver,
                is_resolver=True,
                with_default=True,
            )

        result = await resolver(
            source,
            await coerce_arguments(
                field_definition.arguments,
                field_nodes[0],
                execution_context.variable_values,
                execution_context.context,
                coercer=field_definition.arguments_coercer,
            ),
            execution_context.context,
            info,
            context_coercer=execution_context.context,
        )
        if info.is_introspection:
            return await introspection_directives_executor(
                result,
                execution_context.context,
                info,
                context_coercer=execution_context.context,
            )
        return result
    except Exception as e:  # pylint: disable=broad-except
        return e


async def resolve_field(
    execution_context: "ExecutionContext",
    parent_type: "GraphQLObjectType",
    source: Any,
    field_nodes: List["FieldNode"],
    path: "Path",
    is_introspection_context: bool,
    field_definition: "GraphQLField",
    resolver: Callable,
    output_coercer: Callable,
) -> Any:
    """
    Resolves the field value and coerce it before returning it.
    :param execution_context: instance of the query execution context
    :param parent_type: GraphQLObjectType of the field's parent
    :param source: default root value or field parent value
    :param field_nodes: AST nodes related to the resolved field
    :param path: the path traveled until this resolver
    :param field_definition: GraphQLField instance of the resolved field
    :param resolver: callable to use to resolve the field
    :param output_coercer: callable to use to coerce the resolved field value
    :param is_introspection_context: determines whether or not the resolved
    field is in a context of an introspection query
    :type execution_context: ExecutionContext
    :type parent_type: GraphQLObjectType
    :type source: Any
    :type field_nodes: List[FieldNode]
    :type path: Path
    :type field_definition: GraphQLField
    :type resolver: Callable
    :type output_coercer: Callable
    :type is_introspection_context: bool
    :return: the coerced resolved field value
    :rtype: Any
    """
    # pylint: disable=too-many-arguments
    info = build_resolve_info(
        execution_context,
        field_definition,
        field_nodes,
        parent_type,
        path,
        is_introspection_context,
    )

    return await complete_value_catching_error(
        await resolve_field_value_or_error(
            execution_context,
            field_definition,
            field_nodes,
            resolver,
            source,
            info,
        ),
        info,
        execution_context,
        field_nodes,
        path,
        field_definition.graphql_type,
        output_coercer,
    )
