from tartiflette.types.interface import GraphQLInterfaceType
from tartiflette.types.union import GraphQLUnionType


def is_abstract_type(schema_type: "GraphQLType") -> bool:
    """
    Determines if a GraphQLType is an abstract type.
    :param schema_type: schema type to check
    :type schema_type: GraphQLType
    :return: whether or not the schema type is an abstract type
    :rtype: bool
    """
    return isinstance(schema_type, (GraphQLInterfaceType, GraphQLUnionType))
