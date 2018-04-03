from tartiflette.types.union import GraphQLUnionType


def test_graphql_union_init():
    union = GraphQLUnionType(name="Name", gql_types=[
        "First",
        "Second",
    ], description="description")

    assert union.name == "Name"
    assert union.gql_types == ["First", "Second"]
    assert union.description == "description"


def test_graphql_union_repr():
    union = GraphQLUnionType(name="Name", gql_types=[
        "First",
        "Second",
    ], description="description")

    assert union.__repr__() == "GraphQLUnionType(name='Name', " \
                               "gql_types=['First', 'Second'], " \
                                "description='description')"
    assert union == eval(repr(union))


def test_graphql_union_eq():
    union = GraphQLUnionType(name="Name", gql_types=[
        "First",
        "Second",
    ], description="description")

    ## Same
    assert union == union
    assert union == GraphQLUnionType(name="Name", gql_types=[
        "First",
        "Second",
    ], description="description")
    # Currently we ignore the description in comparing
    assert union == GraphQLUnionType(name="Name", gql_types=[
        "First",
        "Second",
    ])

    ## Different
    assert union != GraphQLUnionType(name="Name", gql_types=[
        "Second",
        "First",
        # We changed the order of types
    ])

    assert union != GraphQLUnionType(name="OtherName", gql_types=[
        "First",
        "Second",
    ])

