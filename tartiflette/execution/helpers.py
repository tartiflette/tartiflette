from tartiflette.utils.errors import graphql_error_from_nodes

__all__ = ("get_field_definition", "get_operation_root_type")


def get_field_definition(
    schema: "GraphQLSchema", parent_type: "GraphQLObjectType", field_name: str
) -> "GraphQLField":
    """
    Returns the field corresponding to the parent type and field name.
    :param schema: the GraphQLSchema instance linked to the engine
    :param parent_type: GraphQLObjectType of the field's parent
    :param field_name: field name to retrieve
    :type schema: GraphQLSchema
    :type parent_type: GraphQLObjectType
    :type field_name: str
    :return: the GraphQLField instance
    :rtype: GraphQLField
    """
    try:
        return schema.get_field_by_name(f"{parent_type}.{field_name}")
    except Exception:  # pylint: disable=broad-except
        pass
    return None


def get_operation_root_type(
    schema: "GraphQLSchema", operation: "OperationDefinitionNode"
) -> "GraphQLObjectType":
    """
    Extracts the root type of the operation from the schema.
    :param schema: the GraphQLSchema instance linked to the engine
    :param operation: AST operation definition node from which retrieve the
    root type
    :type schema: GraphQLSchema
    :type operation: OperationDefinitionNode
    :return: the GraphQLObjectType instance related to the operation definition
    :rtype: GraphQLObjectType
    """
    operation_type = operation.operation_type
    if operation_type == "query":
        try:
            return schema.find_type(schema.query_operation_name)
        except KeyError:
            raise graphql_error_from_nodes(
                "Schema does not define the required query root type.",
                nodes=operation,
            )
    if operation_type == "mutation":
        try:
            return schema.find_type(schema.mutation_operation_name)
        except KeyError:
            raise graphql_error_from_nodes(
                "Schema is not configured for mutations.", nodes=operation
            )
    if operation_type == "subscription":
        try:
            return schema.find_type(schema.subscription_operation_name)
        except KeyError:
            raise graphql_error_from_nodes(
                "Schema is not configured for subscriptions.", nodes=operation
            )
    raise graphql_error_from_nodes(
        "Can only have query, mutation and subscription operations.",
        nodes=operation,
    )
