from tartiflette.types.helpers.definition import (
    is_abstract_type,
    is_list_type,
    is_non_null_type,
    is_object_type,
)

__all__ = ("is_type_sub_type_of", "do_types_overlap")


def is_type_sub_type_of(
    schema: "GraphQLSchema",
    maybe_sub_type: "GraphQLType",
    super_type: "GraphQLType",
) -> bool:
    """
    Determines whether or not a type if a possible sub type of the other.
    :param schema: the GraphQLSchema instance linked to the engine
    :param maybe_sub_type: sub type to test
    :param super_type: main type to test
    :type schema: GraphQLType
    :type maybe_sub_type: GraphQLType
    :type super_type: GraphQLType
    :return: whether or not a type if a possible sub type of the other
    :rtype: bool
    """
    if maybe_sub_type is super_type:
        return True

    if is_non_null_type(super_type):
        return (
            is_type_sub_type_of(
                schema, maybe_sub_type.wrapped_type, super_type.wrapped_type
            )
            if is_non_null_type(maybe_sub_type)
            else False
        )

    if is_non_null_type(maybe_sub_type):
        return is_type_sub_type_of(
            schema, maybe_sub_type.wrapped_type, super_type
        )

    if is_list_type(super_type):
        return (
            is_type_sub_type_of(
                schema, maybe_sub_type.wrapped_type, super_type.wrapped_type
            )
            if is_list_type(maybe_sub_type)
            else False
        )

    if is_list_type(maybe_sub_type):
        return False

    return (
        is_abstract_type(super_type)
        and is_object_type(maybe_sub_type)
        and super_type.is_possible_type(maybe_sub_type)
    )


def do_types_overlap(type_a: "GraphQLType", type_b: "GraphQLType") -> bool:
    """
    Determines whether or not the types overlap each other.
    :param type_a: first type to test
    :param type_b: second type to test
    :type type_a: GraphQLType
    :type type_b: GraphQLType
    :return: whether or not the types overlap each other
    :rtype: bool
    """
    if type_a is type_b:
        return True

    if is_abstract_type(type_a):
        if is_abstract_type(type_b):
            return any(
                type_b.is_possible_type(possible_type)
                for possible_type in type_a.possible_types
            )
        return type_a.is_possible_type(type_b)

    return (
        type_b.is_possible_type(type_a) if is_abstract_type(type_b) else False
    )
