from collections import OrderedDict

from tartiflette.types.field import GraphQLField
from tartiflette.types.interface import GraphQLInterfaceType


def test_graphql_interface_init(mocked_resolver_factory):
    interface = GraphQLInterfaceType(
        name="Name",
        fields=OrderedDict(
            [
                ("test", GraphQLField(name="arg", gql_type="Int")),
                ("another", GraphQLField(name="arg", gql_type="String")),
            ]
        ),
        description="description",
    )

    assert interface.name == "Name"
    assert interface.find_field("test") == GraphQLField(
        name="arg", gql_type="Int"
    )
    assert interface.find_field("another") == GraphQLField(
        name="arg", gql_type="String"
    )
    assert interface.description == "description"


def test_graphql_interface_eq(mocked_resolver_factory):
    interface = GraphQLInterfaceType(
        name="Name",
        fields=OrderedDict(
            [
                ("test", GraphQLField(name="arg", gql_type="Int")),
                ("another", GraphQLField(name="arg", gql_type="String")),
            ]
        ),
        description="description",
    )

    ## Same
    assert interface == interface
    assert interface == GraphQLInterfaceType(
        name="Name",
        fields=OrderedDict(
            [
                ("test", GraphQLField(name="arg", gql_type="Int")),
                ("another", GraphQLField(name="arg", gql_type="String")),
            ]
        ),
        description="description",
    )
    # Currently we ignore the description in comparing
    assert interface == GraphQLInterfaceType(
        name="Name",
        fields=OrderedDict(
            [
                ("test", GraphQLField(name="arg", gql_type="Int")),
                ("another", GraphQLField(name="arg", gql_type="String")),
            ]
        ),
    )

    ## Different
    assert interface != GraphQLInterfaceType(
        name="Name",
        fields=OrderedDict(
            [
                ("another", GraphQLField(name="arg", gql_type="String")),
                ("test", GraphQLField(name="arg", gql_type="Int")),
                # We reversed the order of arguments
            ]
        ),
    )
    assert interface != GraphQLInterfaceType(name="Name", fields=OrderedDict())
    assert interface != GraphQLInterfaceType(
        name="OtherName",
        fields=OrderedDict(
            [
                ("another", GraphQLField(name="arg", gql_type="String")),
                ("test", GraphQLField(name="arg", gql_type="Int")),
                # We reversed the order of arguments
            ]
        ),
    )
