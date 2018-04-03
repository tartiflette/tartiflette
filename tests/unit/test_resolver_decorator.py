from unittest.mock import Mock

from tartiflette.sdl.builder import build_graphql_schema_from_sdl
from tartiflette.resolver_decorator import Resolver
from tartiflette.schema import GraphQLSchema


def test_resolver_decorator():
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
    
    type RootQuery {
        defaultField: Int
    }
    
    # Query has been replaced by RootQuery as entrypoint
    type Query {
        nonDefaultField: String 
    }
    
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

    mock_one = Mock()
    mock_two = Mock()

    @Resolver("Test.field", schema=generated_schema)
    def func_field_resolver(*args, **kwargs):
        mock_one()
        return

    @Resolver("RootQuery.defaultField", schema=generated_schema)
    def func_default_resolver(*args, **kwargs):
        mock_two()
        return

    assert generated_schema.get_field_by_name('Test.field').resolver == func_field_resolver
    assert mock_one.called is False
    assert generated_schema.get_field_by_name('RootQuery.defaultField').resolver == func_default_resolver
    assert mock_two.called is False


