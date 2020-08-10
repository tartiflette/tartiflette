from typing import Optional

from tartiflette.types.enum import GraphQLEnumType
from tartiflette.types.input_object import GraphQLInputObjectType
from tartiflette.types.interface import GraphQLInterfaceType
from tartiflette.types.list import GraphQLList
from tartiflette.types.non_null import GraphQLNonNull
from tartiflette.types.object import GraphQLObjectType
from tartiflette.types.scalar import GraphQLScalarType
from tartiflette.types.type import GraphQLType
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
    "is_output_type",
    "is_abstract_type",
    "is_composite_type",
    "is_leaf_type",
    "is_interface_type",
    "is_object_type",
    "is_required_input_field",
)


def get_wrapped_type(
    graphql_type: Optional["GraphQLType"],
) -> Optional["GraphQLType"]:
    """
    Unwraps the GraphQL type and to return the inner type.
    :param graphql_type: schema type to unwrap
    :type graphql_type: Optional["GraphQLType"]
    :return: the unwrapped inner schema type
    :rtype: Optional["GraphQLType"]
    """
    if graphql_type is None:
        return None

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
    if not isinstance(graphql_type, GraphQLType):
        return False

    return isinstance(
        graphql_type,
        (GraphQLScalarType, GraphQLEnumType, GraphQLInputObjectType),
    ) or (
        graphql_type.is_wrapping_type
        and is_input_type(graphql_type.wrapped_type)
    )


def is_output_type(graphql_type: "GraphQLType") -> bool:
    """
    Determines whether or not the "GraphQLType" is an output type.
    :param graphql_type: schema type to test
    :type graphql_type: GraphQLType
    :return: whether or not the "GraphQLType" is an output type.
    :rtype: bool
    """
    if not isinstance(graphql_type, GraphQLType):
        return False

    return isinstance(
        graphql_type,
        (
            GraphQLScalarType,
            GraphQLObjectType,
            GraphQLInterfaceType,
            GraphQLUnionType,
            GraphQLEnumType,
        ),
    ) or (
        graphql_type.is_wrapping_type
        and is_output_type(graphql_type.wrapped_type)
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


def is_composite_type(graphql_type: "GraphQLType") -> bool:
    """
    Determines whether or not the "GraphQLType" is an composite type.
    :param graphql_type: schema type to test
    :type graphql_type: GraphQLType
    :return: whether or not the "GraphQLType" is an composite type.
    :rtype: bool
    """
    return isinstance(
        graphql_type,
        (GraphQLObjectType, GraphQLInterfaceType, GraphQLUnionType),
    )


def is_leaf_type(graphql_type: "GraphQLType") -> bool:
    """
    Determines whether or not the "GraphQLType" is a leaf type.
    :param graphql_type: schema type to test
    :type graphql_type: GraphQLType
    :return: whether or not the "GraphQLType" is a leaf type.
    :rtype: bool
    """
    return isinstance(graphql_type, (GraphQLScalarType, GraphQLEnumType))


def is_interface_type(graphql_type: "GraphQLType") -> bool:
    """
    Determines whether or not the "GraphQLType" is an interface type.
    :param graphql_type: schema type to test
    :type graphql_type: GraphQLType
    :return: whether or not the "GraphQLType" is an interface type.
    :rtype: bool
    """
    return isinstance(graphql_type, GraphQLInterfaceType)


def is_object_type(graphql_type: "GraphQLType") -> bool:
    """
    Determines whether or not the "GraphQLType" is an object type.
    :param graphql_type: schema type to test
    :type graphql_type: GraphQLType
    :return: whether or not the "GraphQLType" is an object type.
    :rtype: bool
    """
    return isinstance(graphql_type, GraphQLObjectType)


def is_required_input_field(field: "GraphQLInputField") -> bool:
    """
    Determines whether or not the input field is required.
    :param field: input field to test
    :type field: GraphQLInputField
    :return: whether or not the input field is required
    :rtype: bool
    """
    return is_non_null_type(field.graphql_type) and field.default_value is None
