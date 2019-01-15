from tartiflette.types.non_null import GraphQLNonNull


def test_graphql_non_null_init():
    non_null = GraphQLNonNull(gql_type="Name", description="description")

    assert non_null.gql_type == "Name"
    assert non_null.description == "description"


def test_graphql_non_null_repr():
    non_null = GraphQLNonNull(gql_type="Name", description="description")

    assert (
        non_null.__repr__() == "GraphQLNonNull(gql_type='Name', "
        "description='description')"
    )
    assert non_null == eval(repr(non_null))


def test_graphql_non_null_eq():
    non_null = GraphQLNonNull(gql_type="Name", description="description")

    ## Same
    assert non_null == non_null
    assert non_null == GraphQLNonNull(
        gql_type="Name", description="description"
    )
    # Currently we ignore the description in comparing
    assert non_null == GraphQLNonNull(gql_type="Name")

    ## Different
    assert non_null != GraphQLNonNull(gql_type="OtherName")


def test_graphql_non_null_nested_repr():
    non_null = GraphQLNonNull(gql_type="Name", description="description")

    assert (
        non_null.__repr__() == "GraphQLNonNull(gql_type='Name', "
        "description='description')"
    )
    assert non_null == eval(repr(non_null))

    # Test nested types
    non_null = GraphQLNonNull(
        gql_type=GraphQLNonNull(gql_type="Name"), description="description"
    )

    assert (
        non_null.__repr__() == "GraphQLNonNull(gql_type="
        "GraphQLNonNull(gql_type='Name', description=None), "
        "description='description')"
    )
    assert non_null == eval(repr(non_null))
