from typing import Any, Dict, List, Union

from tartiflette.coercers.outputs.common import complete_object_value
from tartiflette.coercers.outputs.null_coercer import null_coercer_wrapper
from tartiflette.types.object import GraphQLObjectType
from tartiflette.utils.errors import graphql_error_from_nodes

__all__ = ("abstract_coercer",)


def ensure_valid_runtime_type(
    runtime_type_or_name: Union["GraphQLObjectType", str],
    execution_context: "ExecutionContext",
    return_type: "GraphQLAbstractType",
    field_nodes: List["FieldNodes"],
    info: "ResolveInfo",
    result: Any,
) -> "GraphQLObjectType":
    """
    Validates and returns that the filled in runtime type is valid.
    :param runtime_type_or_name: name or GraphQLType of the runtime type
    :param execution_context: instance of the query execution context
    :param return_type: the GraphQLAbstractType instance of the object
    :param field_nodes: AST nodes related to the coerced field
    :param info: information related to the execution and the resolved field
    :param result: result to treat
    :type runtime_type_or_name: Union[GraphQLObjectType, str]
    :type execution_context: ExecutionContext
    :type return_type: GraphQLAbstractType
    :type field_nodes: List[FieldNode]
    :type info: ResolveInfo
    :type result: Any
    :return: the GraphQLObjectType representing the runtime type
    :rtype: GraphQLObjectType
    """
    if isinstance(runtime_type_or_name, str):
        try:
            runtime_type = execution_context.schema.find_type(
                runtime_type_or_name
            )
        except KeyError:
            runtime_type = runtime_type_or_name
    else:
        runtime_type = runtime_type_or_name

    if not isinstance(runtime_type, GraphQLObjectType):
        raise graphql_error_from_nodes(
            f"Abstract type < {return_type.name} > must resolve to an object "
            "type at runtime for field "
            f"< {info.parent_type.name}.{info.field_name} > with value "
            f"< {result} >, received < {runtime_type} >. "
            f"Either the < {return_type.name} > type should implements a "
            "< @TypeResolver > or the "
            f"< {info.parent_type.name}.{info.field_name} > field resolver "
            "should implement a `type_resolver` attribute.",
            nodes=field_nodes,
        )

    if not return_type.is_possible_type(runtime_type):
        raise graphql_error_from_nodes(
            f"Runtime object type < {runtime_type.name} > is not a possible "
            f"type for < {return_type.name} >.",
            nodes=field_nodes,
        )
    return runtime_type


@null_coercer_wrapper
async def abstract_coercer(
    result: Any,
    info: "ResolveInfo",
    execution_context: "ExecutionContext",
    field_nodes: List["FieldNode"],
    path: "Path",
    abstract_type: "GraphQLAbstractType",
) -> Dict[str, Any]:
    """
    Computes the value of an abstract type.
    :param result: resolved value
    :param info: information related to the execution and the resolved field
    :param execution_context: instance of the query execution context
    :param field_nodes: AST nodes related to the resolved field
    :param path: the path traveled until this resolver
    :param abstract_type: the GraphQLAbstractType instance of the object
    :type result: Any
    :type info: ResolveInfo
    :type execution_context: ExecutionContext
    :type field_nodes: List[FieldNode]
    :type path: Path
    :type abstract_type: GraphQLAbstractType
    :return: the computed value
    :rtype: Dict[str, Any]
    """
    # pylint: disable=unused-argument
    type_resolver = abstract_type.get_type_resolver(
        f"{info.parent_type.name}.{info.field_name}",
        execution_context.schema.default_type_resolver,
    )

    return await complete_object_value(
        result,
        info,
        execution_context,
        field_nodes,
        path,
        ensure_valid_runtime_type(
            type_resolver(
                result, execution_context.context, info, abstract_type
            ),
            execution_context,
            abstract_type,
            field_nodes,
            info,
            result,
        ),
    )
