import asyncio

from typing import Any, AsyncIterable, Callable, Dict, List, Optional, Union

from tartiflette.coercers.arguments import coerce_arguments
from tartiflette.coercers.common import Path
from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.execution.collect import collect_fields
from tartiflette.execution.context import build_execution_context
from tartiflette.execution.helpers import get_field_definition
from tartiflette.execution.types import build_resolve_info
from tartiflette.utils.errors import extract_exceptions_from_results
from tartiflette.utils.values import is_invalid_value

__all__ = (
    "resolve_field",
    "execute_fields",
    "execute",
    "create_source_event_stream",
)


async def resolve_field(
    execution_context: "ExecutionContext",
    parent_type: "GraphQLObjectType",
    source: Any,
    field_nodes: List["FieldNode"],
    path: "Path",
    is_introspection_context: bool = False,
) -> Any:
    """
    Resolves the field on the given source object. In particular, this
    figures out the value that the field returns by calling its resolve
    function, then calls completeValue to complete promises, serialize scalars,
    or execute the sub-selection-set for objects.
    :param execution_context: instance of the query execution context
    :param parent_type: GraphQLObjectType of the field's parent
    :param source: default root value or field parent value
    :param field_nodes: AST nodes related to the resolved field
    :param path: the path traveled until this resolver
    :param is_introspection_context: determines whether or not the resolved
    field is in a context of an introspection query
    :type execution_context: ExecutionContext
    :type parent_type: GraphQLObjectType
    :type source: Any
    :type field_nodes: List[FieldNode]
    :type path: Path
    :type is_introspection_context: bool
    :return: the computed field value
    :rtype: Any
    """
    field_node = field_nodes[0]
    field_name = field_node.name.value

    field_definition = get_field_definition(
        execution_context.schema, parent_type, field_name
    )
    if field_definition is None:
        return UNDEFINED_VALUE

    return await field_definition.resolver(
        execution_context,
        parent_type,
        source,
        field_nodes,
        path,
        is_introspection_context,
    )


async def execute_fields_serially(
    execution_context: "ExecutionContext",
    parent_type: "GraphQLObjectType",
    source_value: Any,
    path: Optional["Path"],
    fields: Dict[str, List["FieldNode"]],
) -> Dict[str, Any]:
    """
    Implements the "Evaluating selection sets" section of the spec for "write"
    mode.
    :param execution_context: instance of the query execution context
    :param parent_type: GraphQLObjectType of the field's parent
    :param source_value: default root value or field parent value
    :param path: the path traveled until this resolver
    :param fields: dictionary of collected fields
    :type execution_context: ExecutionContext
    :type parent_type: GraphQLObjectType
    :type source_value: Any
    :type path: Optional[Path]
    :type fields: Dict[str, List[FieldNode]]
    :return: the computed fields value
    :rtype: Dict[str, Any]
    """
    results = {}
    for entry_key, field_nodes in fields.items():
        result = await resolve_field(
            execution_context,
            parent_type,
            source_value,
            field_nodes,
            Path(path, entry_key),
        )
        if not is_invalid_value(result):
            results[entry_key] = result
    return results


async def execute_fields(
    execution_context: "ExecutionContext",
    parent_type: "GraphQLObjectType",
    source_value: Any,
    path: Optional["Path"],
    fields: Dict[str, List["FieldNode"]],
    is_introspection_context: bool = False,
) -> Dict[str, Any]:
    """
    Implements the "Evaluating selection sets" section of the spec for "read"
    mode.
    :param execution_context: instance of the query execution context
    :param parent_type: GraphQLObjectType of the field's parent
    :param source_value: default root value or field parent value
    :param path: the path traveled until this resolver
    :param fields: dictionary of collected fields
    :param is_introspection_context: determines whether or not the resolved
    field is in a context of an introspection query
    :type execution_context: ExecutionContext
    :type parent_type: GraphQLObjectType
    :type source_value: Any
    :type path: Optional[Path]
    :type fields: Dict[str, List[FieldNode]]
    :type is_introspection_context: bool
    :return: the computed fields value
    :rtype: Dict[str, Any]
    """

    results = await asyncio.gather(
        *[
            resolve_field(
                execution_context,
                parent_type,
                source_value,
                field_nodes,
                Path(path, entry_key),
                is_introspection_context,
            )
            for entry_key, field_nodes in fields.items()
        ],
        return_exceptions=True,
    )

    exceptions = extract_exceptions_from_results(results)
    if exceptions:
        raise exceptions

    return {
        entry_key: result
        for entry_key, result in zip(fields, results)
        if not is_invalid_value(result)
    }


async def execute_operation(
    execution_context: "ExecutionContext",
    operation: "OperationDefinitionNode",
    root_value: Optional[Any],
) -> Optional[Dict[str, Any]]:
    """
    Implements the "Evaluating operations" section of the spec.
    :param execution_context: instance of the query execution context
    :param operation: AST operation definition node to execute
    :param root_value: default value for root fields
    :type execution_context: ExecutionContext
    :type operation: OperationDefinitionNode
    :type root_value: Optional[Any]
    :return: Optional[Dict[str, Any]]
    :rtype: the computed value
    """
    operation_root_type = execution_context.schema.get_operation_root_type(
        operation
    )

    fields = await collect_fields(
        execution_context, operation_root_type, operation.selection_set
    )

    try:
        return await (
            execute_fields_serially(
                execution_context,
                operation_root_type,
                root_value,
                None,
                fields,
            )
            if operation.operation_type == "mutation"
            else execute_fields(
                execution_context,
                operation_root_type,
                root_value,
                None,
                fields,
            )
        )
    except Exception as e:  # pylint: disable=broad-except
        execution_context.add_error(e)
        return None


async def execute(
    schema: "GraphQLSchema",
    document: "DocumentNode",
    response_builder: Callable,
    root_value: Optional[Any],
    context: Optional[Any],
    variables: Optional[Dict[str, Any]],
    operation_name: Optional[str],
) -> Dict[str, Any]:
    """
    Runs the execution of the executable operation.
    :param schema: the GraphQLSchema instance linked to the engine
    :param document: the DocumentNode instance linked to the GraphQL request
    :param response_builder: callable in charge of returning the formatted
    GraphQL response
    :param root_value: an initial value corresponding to the root type being
    executed
    :param context: value that can contain everything you need and that will be
    accessible from the resolvers
    :param variables: the variables provided in the GraphQL request
    :param operation_name: the operation name to execute
    :type schema: GraphQLSchema
    :type document: DocumentNode
    :type response_builder: Callable
    :type root_value: Optional[Any]
    :type context: Optional[Any]
    :type variables: Optional[Dict[str, Any]]
    :type operation_name: str
    :return: the GraphQL response linked to the operation execution
    :rtype: Dict[str, Any]
    """
    execution_context, errors = await build_execution_context(
        schema, document, root_value, context, variables, operation_name
    )

    if errors:
        return await response_builder(errors=errors)

    data = await execute_operation(
        execution_context, execution_context.operation, root_value
    )
    return await response_builder(data=data, errors=execution_context.errors)


async def create_source_event_stream(
    schema: "GraphQLSchema",
    document: "DocumentNode",
    response_builder: Callable,
    root_value: Optional[Any],
    context: Optional[Any],
    variables: Optional[Dict[str, Any]],
    operation_name: Optional[str],
) -> Union[AsyncIterable[Dict[str, Any]], Dict[str, Any]]:
    """
    Resolves the subscription source event stream.
    :param schema: the GraphQLSchema instance linked to the engine
    :param document: the DocumentNode instance linked to the GraphQL request
    :param response_builder: callable in charge of returning the formatted
    GraphQL response
    :param root_value: an initial value corresponding to the root type being
    executed
    :param context: value that can contain everything you need and that will be
    accessible from the resolvers
    :param variables: the variables provided in the GraphQL request
    :param operation_name: the operation name to execute
    :type schema: GraphQLSchema
    :type document: DocumentNode
    :type response_builder: Callable
    :type root_value: Optional[Any]
    :type context: Optional[Any]
    :type variables: Optional[Dict[str, Any]]
    :type operation_name: str
    :return: an error or an async iterable
    :rtype: Union[AsyncIterable[Dict[str, Any]], Dict[str, Any]]
    """
    # pylint: disable=too-many-locals
    execution_context, errors = await build_execution_context(
        schema, document, root_value, context, variables, operation_name
    )

    if errors:
        return await response_builder(errors=errors)

    operation_root_type = schema.get_operation_root_type(
        execution_context.operation
    )

    fields = await collect_fields(
        execution_context,
        operation_root_type,
        execution_context.operation.selection_set,
    )

    response_name = list(fields.keys())[0]
    field_nodes = fields[response_name]
    field_name = field_nodes[0].name.value
    field_definition = get_field_definition(
        schema, operation_root_type, field_name
    )

    if not field_definition:
        raise Exception(
            f"The subscription field < {field_name} > is not defined."
        )

    if not field_definition.subscribe:
        raise Exception(
            "Can't execute a subscription query on a field which doesn't "
            "provide a source event stream with < @Subscription >."
        )

    info = build_resolve_info(
        execution_context,
        field_definition,
        field_nodes,
        operation_root_type,
        Path(None, response_name),
    )

    return field_definition.subscribe(
        root_value,
        await coerce_arguments(
            field_definition.arguments,
            field_nodes[0],
            execution_context.variable_values,
            execution_context.context,
        ),
        execution_context.context,
        info,
    )
