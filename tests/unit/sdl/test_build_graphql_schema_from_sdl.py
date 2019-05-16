from collections import OrderedDict
from unittest.mock import Mock

import pytest


@pytest.mark.asyncio
async def test_build_schema(monkeypatch, clean_registry):
    from tartiflette.resolver.factoryyy import ResolverExecutorFactory
    from tartiflette.engine import _import_builtins

    resolver_excutor = Mock()
    monkeypatch.setattr(
        ResolverExecutorFactory,
        "get_resolver_executor",
        Mock(return_value=resolver_excutor),
    )

    from tartiflette.schema.bakery import SchemaBakery
    from tartiflette.types.argument import GraphQLArgument
    from tartiflette.types.field import GraphQLField
    from tartiflette.types.input_object import GraphQLInputObjectType
    from tartiflette.types.interface import GraphQLInterfaceType
    from tartiflette.types.list import GraphQLList
    from tartiflette.types.non_null import GraphQLNonNull
    from tartiflette.types.object import GraphQLObjectType
    from tartiflette.types.union import GraphQLUnionType

    schema_sdl = """
    schema @enable_cache {
        query: RootQuery
        mutation: RootMutation
        subscription: RootSubscription
    }

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

    # directive @partner(goo: Anything) on ENUM_VALUE

    \"\"\"
    This is a docstring for the Test Object Type.
    \"\"\"
    type Test implements Unknown & Empty{
        \"\"\"
        This is a field description :D
        \"\"\"
        field(input: InputObject): String!
        anotherField: [Int]
        fieldWithDefaultValueArg(test: String = "default"): ID
        simpleField: Date
    }
    """
    _, schema_sdl = await _import_builtins([], schema_sdl, "G")
    _, schema_E = await _import_builtins([], "", "E")
    clean_registry.register_sdl("G", schema_sdl)
    clean_registry.register_sdl("E", schema_E)
    generated_schema = SchemaBakery._preheat("G")
    expected_schema = SchemaBakery._preheat("E")
    expected_schema.query_type = "RootQuery"
    expected_schema.mutation_type = "RootMutation"
    expected_schema.subscription_type = "RootSubscription"

    expected_schema.add_definition(
        GraphQLUnionType(name="Group", gql_types=["Foo", "Bar", "Baz"])
    )
    expected_schema.add_definition(
        GraphQLInterfaceType(
            name="Something",
            fields=OrderedDict(
                oneField=GraphQLField(
                    name="oneField", gql_type=GraphQLList(gql_type="Int")
                ),
                anotherField=GraphQLField(
                    name="anotherField",
                    gql_type=GraphQLList(gql_type="String"),
                ),
                aLastOne=GraphQLField(
                    name="aLastOne",
                    gql_type=GraphQLNonNull(
                        gql_type=GraphQLList(
                            gql_type=GraphQLList(
                                gql_type=GraphQLNonNull(gql_type="Date")
                            )
                        )
                    ),
                ),
            ),
        )
    )
    expected_schema.add_definition(
        GraphQLInputObjectType(
            name="UserInfo",
            fields=OrderedDict(
                [
                    ("name", GraphQLArgument(name="name", gql_type="String")),
                    (
                        "dateOfBirth",
                        GraphQLArgument(
                            name="dateOfBirth",
                            gql_type=GraphQLList(gql_type="Date"),
                        ),
                    ),
                    (
                        "graphQLFan",
                        GraphQLArgument(
                            name="graphQLFan",
                            gql_type=GraphQLNonNull(gql_type="Boolean"),
                        ),
                    ),
                ]
            ),
        )
    )
    expected_schema.add_definition(
        GraphQLObjectType(
            name="Test",
            fields=OrderedDict(
                [
                    (
                        "field",
                        GraphQLField(
                            name="field",
                            gql_type=GraphQLNonNull(gql_type="String"),
                            arguments=OrderedDict(
                                input=GraphQLArgument(
                                    name="input", gql_type="InputObject"
                                )
                            ),
                        ),
                    ),
                    (
                        "anotherField",
                        GraphQLField(
                            name="anotherField",
                            gql_type=GraphQLList(gql_type="Int"),
                        ),
                    ),
                    (
                        "fieldWithDefaultValueArg",
                        GraphQLField(
                            name="fieldWithDefaultValueArg",
                            gql_type="ID",
                            arguments=OrderedDict(
                                test=GraphQLArgument(
                                    name="test",
                                    gql_type="String",
                                    default_value="default",
                                )
                            ),
                        ),
                    ),
                    (
                        "simpleField",
                        GraphQLField(name="simpleField", gql_type="Date"),
                    ),
                ]
            ),
            interfaces=["Unknown", "Empty"],
        )
    )

    assert 5 < len(generated_schema._gql_types)
    assert len(expected_schema._gql_types) == len(generated_schema._gql_types)

    monkeypatch.undo()
