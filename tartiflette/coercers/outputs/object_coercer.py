from typing import Any, Dict, List

from tartiflette.coercers.outputs.common import complete_object_value
from tartiflette.coercers.outputs.null_coercer import null_coercer_wrapper

__all__ = ("object_coercer",)


@null_coercer_wrapper
async def object_coercer(
    result: Any,
    info: "ResolveInfo",
    execution_context: "ExecutionContext",
    field_nodes: List["FieldNode"],
    path: "Path",
    object_type: "GraphQLObjectType",
) -> Dict[str, Any]:
    """
    Computes the value of an object.
    :param result: resolved value
    :param info: information related to the execution and the resolved field
    :param execution_context: instance of the query execution context
    :param field_nodes: AST nodes related to the resolved field
    :param path: the path traveled until this resolver
    :param object_type: the GraphQLObjectType instance of the object
    :type result: Any
    :type info: ResolveInfo
    :type execution_context: ExecutionContext
    :type field_nodes: List[FieldNode]
    :type path: Path
    :type object_type: GraphQLObjectType
    :return: the computed value
    :rtype: Dict[str, Any]
    """
    # pylint: disable=unused-argument
    return await complete_object_value(
        result, info, execution_context, field_nodes, path, object_type
    )
