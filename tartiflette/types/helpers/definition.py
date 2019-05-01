from tartiflette.types.enum import GraphQLEnumType
from tartiflette.types.input_object import GraphQLInputObjectType
from tartiflette.types.interface import GraphQLInterfaceType
from tartiflette.types.list import GraphQLList
from tartiflette.types.non_null import GraphQLNonNull
from tartiflette.types.object import GraphQLObjectType
from tartiflette.types.scalar import GraphQLScalarType
from tartiflette.types.union import GraphQLUnionType


def get_named_type(schema_type):
    """
    TODO:
    :param schema_type: TODO:
    :type schema_type: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    unwrapped_type = schema_type
    while is_wrapping_type(unwrapped_type):
        unwrapped_type = schema_type.gql_type
    return unwrapped_type


def is_scalar_type(schema_type):
    """
    TODO:
    :param schema_type: TODO:
    :type schema_type: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    return isinstance(schema_type, GraphQLScalarType)


def is_enum_type(schema_type):
    """
    TODO:
    :param schema_type: TODO:
    :type schema_type: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    return isinstance(schema_type, GraphQLEnumType)


def is_input_object_type(schema_type):
    """
    TODO:
    :param schema_type: TODO:
    :type schema_type: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    return isinstance(schema_type, GraphQLInputObjectType)


def is_list_type(schema_type):
    """
    TODO:
    :param schema_type: TODO:
    :type schema_type: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    return isinstance(schema_type, GraphQLList)


def is_non_null_type(schema_type):
    """
    TODO:
    :param schema_type: TODO:
    :type schema_type: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    return isinstance(schema_type, GraphQLNonNull)


def is_wrapping_type(schema_type):
    """
    TODO:
    :param schema_type: TODO:
    :type schema_type: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    return isinstance(schema_type, (GraphQLList, GraphQLNonNull))


def is_input_type(schema_type):
    """
    TODO:
    :param schema_type: TODO:
    :type schema_type: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    return isinstance(
        schema_type,
        (GraphQLScalarType, GraphQLEnumType, GraphQLInputObjectType),
    ) or (is_wrapping_type(schema_type) and is_input_type(schema_type.ofType))


def is_abstract_type(schema_type: "GraphQLType") -> bool:
    """
    Determines if a GraphQLType is an abstract type.
    :param schema_type: schema type to check
    :type schema_type: GraphQLType
    :return: whether or not the schema type is an abstract type
    :rtype: bool
    """
    return isinstance(schema_type, (GraphQLInterfaceType, GraphQLUnionType))


def is_leaf_type(schema_type):
    """
    TODO:
    :param schema_type: TODO:
    :type schema_type: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    return isinstance(schema_type, (GraphQLScalarType, GraphQLEnumType))


def is_object_type(schema_type):
    """
    TODO:
    :param schema_type: TODO:
    :type schema_type: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    return isinstance(schema_type, GraphQLObjectType)
