from typing import Any, Dict, List, Optional

__all__ = ("build_resolve_info",)


class ResolveInfo:
    """
    Class containing the information related to a resolved field.
    """

    __slots__ = (
        "field_name",
        "field_nodes",
        "return_type",
        "parent_type",
        "path",
        "schema",
        "fragments",
        "root_value",
        "operation",
        "variable_values",
        "is_introspection",
    )

    def __init__(
        self,
        field_name: str,
        field_nodes: List["FieldNodes"],
        return_type: "GraphQLOutputType",
        parent_type: "GraphQLObjectType",
        path: "Path",
        schema: "GraphQLSchema",
        fragments: Dict[str, "FragmentDefinitionNode"],
        root_value: Optional[Any],
        operation: "OperationDefinitionNode",
        variable_values: Optional[Dict[str, Any]],
        is_introspection_context: bool,
    ):
        """
        :param field_name: name of the resolved field
        :param field_nodes: AST nodes related to the resolved field
        :param return_type: GraphQLOutputType instance of the resolved field
        :param parent_type: GraphQLObjectType of the field's parent
        :param path: the path traveled until this field
        :param schema: the GraphQLSchema instance linked to the engine
        :param fragments: a dictionary of fragment definition AST nodes
        contained in the request
        :param root_value: the initial value corresponding to the root type
        being executed
        :param operation: the AST operation definition node to execute
        :param variable_values: the variables provided in the GraphQL request
        :param is_introspection_context: determines whether or not the resolved
        field is in a context of an introspection query
        :type field_name: str
        :type field_nodes: List[FieldNodes]
        :type return_type: GraphQLOutputType
        :type parent_type: GraphQLObjectType
        :type path: Path
        :type schema: GraphQLSchema
        :type fragments: Dict[str, FragmentDefinitionNode]
        :type root_value: Optional[Any]
        :type operation: OperationDefinitionNode
        :type variable_values: Optional[Dict[str, Any]]
        :type is_introspection_context: bool
        """
        # pylint: disable=too-many-arguments,too-many-locals
        self.field_name = field_name
        self.field_nodes = field_nodes
        self.return_type = return_type
        self.parent_type = parent_type
        self.path = path
        self.schema = schema
        self.fragments = fragments
        self.root_value = root_value
        self.operation = operation
        self.variable_values = variable_values
        self.is_introspection: bool = is_introspection_context


def build_resolve_info(
    execution_context: "ExecutionContext",
    field_definition: "GraphQLField",
    field_nodes: List["FieldNode"],
    parent_type: "GraphQLObjectType",
    path: "Path",
    is_introspection_context: bool = False,
) -> "ResolveInfo":
    """
    Builds & returns a ResolveInfo instance.
    :param execution_context: instance of the query execution context
    :param field_definition: GraphQLField instance of the resolved field
    :param field_nodes: AST nodes related to the resolved field
    :param parent_type: GraphQLObjectType of the field's parent
    :param path: the path traveled until this resolver
    :param is_introspection_context: determines whether or not the resolved
    field is in a context of an introspection query
    :type execution_context: ExecutionContext
    :type field_definition: GraphQLField
    :type field_nodes: List[FieldNode]
    :type parent_type: GraphQLObjectType
    :type path: Path
    :type is_introspection_context: bool
    :return: a ResolveInfo instance
    :rtype: ResolveInfo
    """
    return ResolveInfo(
        field_definition.name,
        field_nodes,
        field_definition.graphql_type,
        parent_type,
        path,
        execution_context.schema,
        execution_context.fragments,
        execution_context.root_value,
        execution_context.operation,
        execution_context.variable_values,
        is_introspection_context,
    )
