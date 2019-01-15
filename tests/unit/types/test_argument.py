from tartiflette.types.argument import GraphQLArgument


def test_graphql_argument_init():
    arg = GraphQLArgument(
        name="Name",
        gql_type="Test",
        default_value=42,
        description="description",
    )

    assert arg.name == "Name"
    assert arg.gql_type == "Test"
    assert arg.default_value == 42
    assert arg.description == "description"


def test_graphql_argument_repr():
    arg = GraphQLArgument(
        name="Name",
        gql_type="Test",
        default_value=42,
        description="description",
    )

    assert (
        arg.__repr__() == "GraphQLArgument(name='Name', gql_type='Test', "
        "default_value=42, description='description')"
    )
    assert arg == eval(repr(arg))


def test_graphql_argument_eq():
    arg = GraphQLArgument(
        name="Name",
        gql_type="Test",
        default_value=42,
        description="description",
    )

    ## Same
    assert arg == arg
    assert arg == GraphQLArgument(
        name="Name",
        gql_type="Test",
        default_value=42,
        description="description",
    )
    # Currently we ignore the description in comparing
    assert arg == GraphQLArgument(
        name="Name", gql_type="Test", default_value=42
    )
    ## Different
    assert arg != GraphQLArgument(
        name="Name", gql_type="Test", default_value=24
    )
    assert arg != GraphQLArgument(name="Name", gql_type="Test")
    assert arg != GraphQLArgument(
        name="Name", gql_type="NotTest", default_value=42
    )
    assert arg != GraphQLArgument(
        name="OtherName", gql_type="Test", default_value=42
    )
