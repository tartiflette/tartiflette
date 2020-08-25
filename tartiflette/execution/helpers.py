__all__ = ("get_field_definition",)


def get_field_definition(
    schema: "GraphQLSchema", parent_type: "GraphQLObjectType", field_name: str
) -> "GraphQLField":
    """
    Returns the field corresponding to the parent type and field name.
    :param schema: the GraphQLSchema instance linked to the SDL
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
