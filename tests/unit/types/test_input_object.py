from collections import OrderedDict

from tartiflette.types.argument import GraphQLArgument
from tartiflette.types.input_object import GraphQLInputObjectType


def test_graphql_input_object_init():
    input_object = GraphQLInputObjectType(
        name="Name",
        fields=OrderedDict(
            [
                ("test", GraphQLArgument(name="arg", gql_type="Int")),
                ("another", GraphQLArgument(name="arg", gql_type="String")),
            ]
        ),
        description="description",
    )

    assert input_object.name == "Name"
    assert input_object._fields == OrderedDict(
        [
            ("test", GraphQLArgument(name="arg", gql_type="Int")),
            ("another", GraphQLArgument(name="arg", gql_type="String")),
        ]
    )
    assert input_object.description == "description"


def test_graphql_input_object_repr():
    input_object = GraphQLInputObjectType(
        name="Name",
        fields=OrderedDict(
            [
                ("test", GraphQLArgument(name="arg", gql_type="Int")),
                ("another", GraphQLArgument(name="arg", gql_type="String")),
            ]
        ),
        description="description",
    )

    assert (
        input_object.__repr__() == "GraphQLInputObjectType(name='Name', "
        "fields=OrderedDict(["
        "('test', GraphQLArgument(name='arg', gql_type='Int', default_value=None, description=None)), "
        "('another', GraphQLArgument(name='arg', gql_type='String', default_value=None, description=None))"
        "]), description='description')"
    )
    assert input_object == eval(repr(input_object))


def test_graphql_input_object_eq():
    input_object = GraphQLInputObjectType(
        name="Name",
        fields=OrderedDict(
            [
                ("test", GraphQLArgument(name="arg", gql_type="Int")),
                ("another", GraphQLArgument(name="arg", gql_type="String")),
            ]
        ),
        description="description",
    )

    ## Same
    assert input_object == input_object
    assert input_object == GraphQLInputObjectType(
        name="Name",
        fields=OrderedDict(
            [
                ("test", GraphQLArgument(name="arg", gql_type="Int")),
                ("another", GraphQLArgument(name="arg", gql_type="String")),
            ]
        ),
        description="description",
    )
    # Currently we ignore the description in comparing
    assert input_object == GraphQLInputObjectType(
        name="Name",
        fields=OrderedDict(
            [
                ("test", GraphQLArgument(name="arg", gql_type="Int")),
                ("another", GraphQLArgument(name="arg", gql_type="String")),
            ]
        ),
    )

    ## Different
    assert input_object != GraphQLInputObjectType(
        name="Name",
        fields=OrderedDict(
            [
                ("another", GraphQLArgument(name="arg", gql_type="String")),
                ("test", GraphQLArgument(name="arg", gql_type="Int")),
                # We reversed the order of arguments
            ]
        ),
    )
    assert input_object != GraphQLInputObjectType(
        name="Name", fields=OrderedDict()
    )
    assert input_object != GraphQLInputObjectType(
        name="OtherName",
        fields=OrderedDict(
            [
                ("another", GraphQLArgument(name="arg", gql_type="String")),
                ("test", GraphQLArgument(name="arg", gql_type="Int")),
                # We reversed the order of arguments
            ]
        ),
    )
