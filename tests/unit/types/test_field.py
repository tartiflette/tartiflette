from collections import OrderedDict

from tartiflette.types.field import GraphQLField
from tartiflette.resolver.factory import default_resolver

from tests.unit.utils import call_with_mocked_resolver_factory


def test_graphql_field_init():
    field = GraphQLField(
        name="Name",
        gql_type="Test",
        arguments=OrderedDict([("test", 42), ("another", 24)]),
        description="description",
    )

    assert field.name == "Name"
    assert field.gql_type == "Test"
    assert field.arguments == OrderedDict([("test", 42), ("another", 24)])
    assert field.resolver._func is default_resolver
    assert field.description == "description"


def test_graphql_field_repr(fixture_mocked_get_resolver_executor):
    field = call_with_mocked_resolver_factory(
        GraphQLField,
        name="Name",
        gql_type="Test",
        arguments=OrderedDict([("test", 42), ("another", 24)]),
        description="description",
        directives=None,
    )

    assert (
        field.__repr__() == "GraphQLField(name='Name', gql_type='Test', "
        "arguments=OrderedDict([('test', 42), "
        "('another', 24)]), resolver=%s, "
        "description='description', directives=[])"
        % fixture_mocked_get_resolver_executor()
    )


def test_graphql_argument_eq(mocked_resolver_factory):
    field = GraphQLField(
        name="Name",
        gql_type="Test",
        arguments=OrderedDict([("test", 42), ("another", 24)]),
        description="description",
    )

    ## Same
    assert field == field
    assert field == GraphQLField(
        name="Name",
        gql_type="Test",
        arguments=OrderedDict([("test", 42), ("another", 24)]),
        description="description",
    )
    # Currently we ignore the description in comparing
    assert field == GraphQLField(
        name="Name",
        gql_type="Test",
        arguments=OrderedDict([("test", 42), ("another", 24)]),
    )

    ## Different
    assert field != GraphQLField(
        name="Name",
        gql_type="Test",
        arguments=OrderedDict(
            [
                ("another", 24),
                ("test", 42),
                # We reversed the order of arguments
            ]
        ),
    )
    assert field != GraphQLField(
        name="Name", gql_type="Test", arguments=OrderedDict()
    )
    assert field != GraphQLField(
        name="Name",
        gql_type="NotTest",
        arguments=OrderedDict([("test", 42), ("another", 24)]),
    )
    assert field != GraphQLField(
        name="OtherName",
        gql_type="Test",
        arguments=OrderedDict([("test", 42), ("another", 24)]),
    )
