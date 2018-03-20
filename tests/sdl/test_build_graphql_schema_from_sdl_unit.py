from collections import OrderedDict

from tartiflette.sdl.builder import build_graphql_schema_from_sdl
from tartiflette.sdl.schema import GraphQLSchema, DefaultGraphQLSchema
from tartiflette.sdl.transformers.schema import GraphQLObjectTypeDefinition, \
    GraphQLNamedType, GraphQLScalarTypeDefinition, \
    GraphQLUnionTypeDefinition, GraphQLInterfaceTypeDefinition, \
    GraphQLFieldDefinition, GraphQLListType, GraphQLNonNullType, \
    GraphQLInputObjectTypeDefinition, GraphQLArgumentDefinition, \
    GraphQLScalarValue, Name


def test_build_schema():
    schema_sdl = """
    schema @enable_cache {
        query: RootQuery
        mutation: RootMutation
        subscription: RootSubscription
    }
    
    scalar Date
    
    union Group = Foo | Bar | Baz
    
    interface Something {
        oneField: [Int]
        anotherField: [String]
        aLastOne: [[Date!]]!
    }
    
    input UserInfo {
        name: String
        dateOfBirth: [Date]
        graphQLFan: Boolean!
    }
    
    # directive @partner(blabla: Truc) on ENUM_VALUE
    
    \"\"\"
    This is a docstring for the Test Object Type.
    \"\"\"
    type Test implements Unknown & Empty @enable_cache {
        \"\"\"
        This is a field description :D
        \"\"\"
        field(input: InputObject): String! @deprecated(reason: "Useless field")
        anotherField: [Int] @something(
            lst: ["about" "stuff"]
            obj: {some: [4, 8, 16], complex: {about: 19.4}, another: EnumVal}
        )
        fieldWithDefaultValueArg(test: String = "default"): ID
        simpleField: Date
    }
    """

    generated_schema = build_graphql_schema_from_sdl(schema_sdl,
                                                     schema=GraphQLSchema())

    expected_schema = GraphQLSchema()
    expected_schema.query_type = GraphQLNamedType(name="RootQuery")
    expected_schema.mutation_type = GraphQLNamedType(name="RootMutation")
    expected_schema.subscription_type = GraphQLNamedType(name="RootSubscription")

    expected_schema.add_definition(GraphQLScalarTypeDefinition(name="Date"))
    expected_schema.add_definition(GraphQLUnionTypeDefinition(name="Group", types=[
        GraphQLNamedType("Foo"),
        GraphQLNamedType("Bar"),
        GraphQLNamedType("Baz"),
    ]))
    expected_schema.add_definition(GraphQLInterfaceTypeDefinition(name="Something", fields=OrderedDict(
        oneField=GraphQLFieldDefinition(name="oneField", gql_type=GraphQLListType(gql_type=GraphQLNamedType(name="Int"))),
        anotherField=GraphQLFieldDefinition(name="anotherField", gql_type=GraphQLListType(gql_type=GraphQLNamedType(name="String"))),
        aLastOne=GraphQLFieldDefinition(name="aLastOne", gql_type=GraphQLNonNullType(gql_type=GraphQLListType(gql_type=GraphQLListType(gql_type=GraphQLNonNullType(gql_type=GraphQLNamedType(name="Date")))))),
    )))
    expected_schema.add_definition(GraphQLInputObjectTypeDefinition(name="UserInfo", fields=OrderedDict(
        name=GraphQLArgumentDefinition(name="name", gql_type=GraphQLNamedType("String")),
        dateOfBirth=GraphQLArgumentDefinition(name="dateOfBirth", gql_type=GraphQLListType(gql_type=GraphQLNamedType(name="Date"))),
        graphQLFan=GraphQLArgumentDefinition(name="graphQLFan", gql_type=GraphQLNonNullType(gql_type=GraphQLNamedType(name="Boolean"))),
    )))
    expected_schema.add_definition(GraphQLObjectTypeDefinition(name="Test", fields=OrderedDict(
        field=GraphQLFieldDefinition(name="field", gql_type=GraphQLNonNullType(gql_type=GraphQLNamedType("String")), arguments=OrderedDict(
            input=GraphQLArgumentDefinition(name="input", gql_type=GraphQLNamedType("InputObject")),
        )),
        anotherField=GraphQLFieldDefinition(name="anotherField", gql_type=GraphQLListType(gql_type=GraphQLNamedType(name="Int"))),
        fieldWithDefaultValueArg=GraphQLFieldDefinition(name="fieldWithDefaultValueArg", gql_type=GraphQLNamedType("ID"), arguments=OrderedDict(
            test=GraphQLArgumentDefinition(name="test", gql_type=GraphQLNamedType("String"), default_value=GraphQLScalarValue(
                value="default")),
        )),
        simpleField=GraphQLFieldDefinition(name="simpleField", gql_type=GraphQLNamedType("Date")),
    ),
                                                               interfaces=[
                                                                   GraphQLNamedType(name="Unknown"),
                                                                   GraphQLNamedType(name="Empty"),
                                                               ]))

    assert expected_schema == generated_schema
    assert len(generated_schema._gql_types) == len(expected_schema._gql_types)
    assert len(DefaultGraphQLSchema._gql_types) == 0
