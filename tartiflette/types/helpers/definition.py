from tartiflette.types.enum import GraphQLEnumType
from tartiflette.types.input_object import GraphQLInputObjectType
from tartiflette.types.interface import GraphQLInterfaceType
from tartiflette.types.list import GraphQLList
from tartiflette.types.non_null import GraphQLNonNull
from tartiflette.types.object import GraphQLObjectType
from tartiflette.types.scalar import GraphQLScalarType
from tartiflette.types.union import GraphQLUnionType

__all__ = (
    "get_wrapped_type",
    "is_scalar_type",
    "is_enum_type",
    "is_input_object_type",
    "is_list_type",
    "is_non_null_type",
    "is_wrapping_type",
    "is_input_type",
    "is_abstract_type",
    "is_leaf_type",
    "is_object_type",
)


def get_wrapped_type(graphql_type: "GraphQLType") -> "GraphQLType":
    """
    Unwraps the GraphQL type and to return the inner type.
    :param graphql_type: schema type to unwrap
    :type graphql_type: GraphQLType
    :return: the unwrapped inner schema type
    :rtype: GraphQLType
    """
    inner_type = graphql_type
    while inner_type.is_wrapping_type:
        inner_type = inner_type.wrapped_type
    return inner_type


def is_scalar_type(graphql_type: "GraphQLType") -> bool:
    """
    Determines whether or not the "GraphQLType" is a scalar type.
    :param graphql_type: schema type to test
    :type graphql_type: GraphQLType
    :return: whether or not the "GraphQLType" is a scalar type.
    :rtype: bool
    """
    return isinstance(graphql_type, GraphQLScalarType)


def is_enum_type(graphql_type: "GraphQLType") -> bool:
    """
    Determines whether or not the "GraphQLType" is an enum type.
    :param graphql_type: schema type to test
    :type graphql_type: GraphQLType
    :return: whether or not the "GraphQLType" is an enum type.
    :rtype: bool
    """
    return isinstance(graphql_type, GraphQLEnumType)


def is_input_object_type(graphql_type: "GraphQLType") -> bool:
    """
    Determines whether or not the "GraphQLType" is an input object type.
    :param graphql_type: schema type to test
    :type graphql_type: GraphQLType
    :return: whether or not the "GraphQLType" is an input object type.
    :rtype: bool
    """
    return isinstance(graphql_type, GraphQLInputObjectType)


def is_list_type(graphql_type: "GraphQLType") -> bool:
    """
    Determines whether or not the "GraphQLType" is a list type.
    :param graphql_type: schema type to test
    :type graphql_type: GraphQLType
    :return: whether or not the "GraphQLType" is a list type.
    :rtype: bool
    """
    return isinstance(graphql_type, GraphQLList)


def is_non_null_type(graphql_type: "GraphQLType") -> bool:
    """
    Determines whether or not the "GraphQLType" is a non null type.
    :param graphql_type: schema type to test
    :type graphql_type: GraphQLType
    :return: whether or not the "GraphQLType" is a non null type.
    :rtype: bool
    """
    return isinstance(graphql_type, GraphQLNonNull)


def is_wrapping_type(graphql_type: "GraphQLType") -> bool:
    """
    Determines whether or not the "GraphQLType" is either a list or non null
    type.
    :param graphql_type: schema type to test
    :type graphql_type: GraphQLType
    :return: whether or not the "GraphQLType" is either a list or non null
    type.
    :rtype: bool
    """
    return isinstance(graphql_type, (GraphQLList, GraphQLNonNull))


def is_input_type(graphql_type: "GraphQLType") -> bool:
    """
    Determines whether or not the "GraphQLType" is an input type.
    :param graphql_type: schema type to test
    :type graphql_type: GraphQLType
    :return: whether or not the "GraphQLType" is an input type.
    :rtype: bool
    """
    return isinstance(
        graphql_type,
        (GraphQLScalarType, GraphQLEnumType, GraphQLInputObjectType),
    ) or (
        graphql_type.is_wrapping_type
        and is_input_type(graphql_type.wrapped_type)
    )


def is_abstract_type(graphql_type: "GraphQLType") -> bool:
    """
    Determines whether or not the "GraphQLType" is an abstract type.
    :param graphql_type: schema type to test
    :type graphql_type: GraphQLType
    :return: whether or not the "GraphQLType" is an abstract type.
    :rtype: bool
    """
    return isinstance(graphql_type, (GraphQLInterfaceType, GraphQLUnionType))


def is_leaf_type(graphql_type: "GraphQLType") -> bool:
    """
    Determines whether or not the "GraphQLType" is a leaf type.
    :param graphql_type: schema type to test
    :type graphql_type: GraphQLType
    :return: whether or not the "GraphQLType" is a leaf type.
    :rtype: bool
    """
    return isinstance(graphql_type, (GraphQLScalarType, GraphQLEnumType))


def is_object_type(graphql_type: "GraphQLType") -> bool:
    """
    Determines whether or not the "GraphQLType" is an object type.
    :param graphql_type: schema type to test
    :type graphql_type: GraphQLType
    :return: whether or not the "GraphQLType" is an object type.
    :rtype: bool
    """
    return isinstance(graphql_type, GraphQLObjectType)
