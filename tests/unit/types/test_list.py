from tartiflette.types.list import GraphQLList


def test_graphql_list_init():
    lst = GraphQLList(gql_type="Name", description="description")

    assert lst.gql_type == "Name"
    assert lst.description == "description"


def test_graphql_list_repr():
    lst = GraphQLList(gql_type="Name", description="description")

    assert (
        lst.__repr__() == "GraphQLList(gql_type='Name', "
        "description='description')"
    )
    assert lst == eval(repr(lst))


def test_graphql_list_eq():
    lst = GraphQLList(gql_type="Name", description="description")

    ## Same
    assert lst == lst
    assert lst == GraphQLList(gql_type="Name", description="description")
    # Currently we ignore the description in comparing
    assert lst == GraphQLList(gql_type="Name")

    ## Different
    assert lst != GraphQLList(gql_type="OtherName")


def test_graphql_list_nested_repr():
    lst = GraphQLList(gql_type="Name", description="description")

    assert (
        lst.__repr__() == "GraphQLList(gql_type='Name', "
        "description='description')"
    )
    assert lst == eval(repr(lst))

    # Test nested types
    lst = GraphQLList(
        gql_type=GraphQLList(gql_type="Name"), description="description"
    )

    assert (
        lst.__repr__() == "GraphQLList(gql_type="
        "GraphQLList(gql_type='Name', description=None), "
        "description='description')"
    )
    assert lst == eval(repr(lst))
