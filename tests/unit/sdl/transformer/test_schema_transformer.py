from collections import OrderedDict

import pytest
from lark.lexer import Token
from lark.tree import Tree

from tartiflette.sdl.builder import parse_graphql_sdl_to_ast
from tartiflette.schema import GraphQLSchema
from tartiflette.sdl.transformers.cleaning_transformer import \
    CleaningTransformer
from tartiflette.sdl.transformers.schema_transformer import \
    SchemaTransformer, SchemaNode
from tartiflette.types.argument import GraphQLArgument
from tartiflette.types.enum import GraphQLEnumType, GraphQLEnumValue
from tartiflette.types.field import GraphQLField
from tartiflette.types.input_object import GraphQLInputObjectType
from tartiflette.types.interface import GraphQLInterfaceType
from tartiflette.types.object import GraphQLObjectType
from tartiflette.types.scalar import GraphQLScalarType
from tartiflette.types.union import GraphQLUnionType


@pytest.mark.parametrize("full_sdl,expected_tree", [
    (
        """
        \"\"\"
        Date scalar for storing Dates, very convenient
        \"\"\"
        scalar Date
        """,
        [Tree('type_definition', [
            GraphQLScalarType(name="Date",
                              description="\n        Date scalar for "
                                          "storing Dates, "
                                          "very convenient\n        "
            ),
        ])],
    ),
    (
        """
        \"\"\"
        DateOrTime scalar for storing Date or Time, very convenient also
        \"\"\"
        union DateOrTime = Date | Time
        """,
        [Tree('type_definition', [
            GraphQLUnionType(name="DateOrTime",
                             gql_types=["Date", "Time"],
                             description="\n        DateOrTime scalar for "
                                         "storing Date or Time, very "
                                         "convenient also\n        "),
        ])],
    ),
    (
        """
        scalar Date
        union DateOrTime = Date | Time
        """,
        [Tree('type_definition', [
            GraphQLScalarType(name="Date"),
        ]),
         Tree('type_definition', [
            GraphQLUnionType(name="DateOrTime", gql_types=["Date", "Time"]),
        ])],
    ),
    (
        """
        \"\"\"
        Vehicle interface for any type of entity-moving apparatus
        \"\"\"
        interface Vehicle {
            speedInKmh: Float
        }
        """,
        [Tree('type_definition', [
            GraphQLInterfaceType(name="Vehicle", fields=OrderedDict([
                ("speedInKmh",
                 GraphQLField(name="speedInKmh", gql_type="Float")),
            ])),
        ])],
    ),
    (
        """
        input UserProfileInput {
            fullName: String
        }
        """,
        [Tree('type_definition', [
            GraphQLInputObjectType(name="UserProfileInput",
                                   fields=OrderedDict([
                                       ("fullName",
                                        GraphQLArgument(
                                            name="fullName",
                                            gql_type="String",
                                        )),
                                   ])),
        ])],
    ),
    (
        """
        type Car implements Vehicle {
            modelName: String
            speedInKmh: Float
        }
        """,
        [Tree('type_definition', [
            GraphQLObjectType(name="Car",
                              fields=OrderedDict([
                                  ("modelName",
                                   GraphQLField(
                                       name="modelName",
                                       gql_type="String")),
                                  ("speedInKmh",
                                   GraphQLField(
                                       name="speedInKmh",
                                       gql_type="Float")),
                              ]),
                              interfaces=["Vehicle"]),
        ])],
    ),
    (
        """
        schema {
            query: RootQuery
            mutation: RootMutation
            subscription: RootSubscription
        }
        """,
        [Tree('schema_definition', [
            Token('SCHEMA', 'schema'),
            Tree('query_operation_type_definition', [
                Token('QUERY', 'query'),
                SchemaNode(type='named_type', value='RootQuery'),
            ]),
            Tree('mutation_operation_type_definition', [
                Token('MUTATION', 'mutation'),
                SchemaNode(type='named_type', value='RootMutation'),
            ]),
            Tree('subscription_operation_type_definition', [
                Token('SUBSCRIPTION', 'subscription'),
                SchemaNode(type='named_type', value='RootSubscription'),
            ]),
        ])],
    ),
    (
        """
        \"\"\"
        The enum Mode is used to switch environments.
        \"\"\"
        enum Mode {
            \"\"\"
            Used for any production system
            \"\"\"
            Prod
            Test
            Dev
        }
        """,
        [Tree('type_definition', [
            GraphQLEnumType(name="Mode", values=[
                GraphQLEnumValue(value="Prod", description="\n            Used "
                                                           "for any production "
                                                           "system\n           "
                                                           " "),
                GraphQLEnumValue(value="Test"),
                GraphQLEnumValue(value="Dev"),
            ],
                            description="\n        The enum Mode is "
                                        "used to switch environments.\n        "),
        ])],
    ),
])
def test_SchemaTransformer_schema(full_sdl, expected_tree):

    raw_tree = parse_graphql_sdl_to_ast(full_sdl)
    cleaned_tree = CleaningTransformer(full_sdl).transform(raw_tree)
    assert SchemaTransformer(full_sdl, schema=GraphQLSchema()).transform(cleaned_tree) == expected_tree


@pytest.mark.parametrize("full_sdl,expected_tree", [
    (
        # TODO: A custom scalar, e.g. "Date" could have a default value with
        # a custom format, say 2018-03-21 but because it is not handled
        # by the parser, it will fail. So custom `Scalar`s will need to use
        # default values as strings and do the conversion later on...
        """
        type TestObject {
            birthDate(input: Date = "2018"): Date
        }
        """,
        [Tree('type_definition', [
            GraphQLObjectType(
                name="TestObject",
                fields=OrderedDict([
                    ("birthDate",
                     GraphQLField(
                         name="birthDate",
                         gql_type="Date",
                         arguments=OrderedDict([
                             ("input", GraphQLArgument(
                                 name="input",
                                 gql_type="Date",
                                 default_value="2018",
                             )),
                        ]))),
                ]),
                interfaces=None),
        ])],
    ),
    (
        """
        type Car {
            modelName(arg: Int = 42): String
            speedInKmh(cplx: InputObject = {
                stuff: 32, nested: {
                    about: "Inc.", 
                    lst: [
                        "Various", "Fields"
                    ]
                }
            }): Float
        }
        """,
        [Tree('type_definition', [
            GraphQLObjectType(name="Car",
                              fields=OrderedDict([
                                  ("modelName",
                                   GraphQLField(
                                       name="modelName",
                                       arguments=OrderedDict([("arg", GraphQLArgument(
                                           name="arg", gql_type="Int",
                                           default_value=42,
                                       ))]),
                                       gql_type="String")),
                                  ("speedInKmh",
                                   GraphQLField(
                                       name="speedInKmh",
arguments=OrderedDict([("cplx", GraphQLArgument(
                                           name="cplx", gql_type="InputObject",
                                           default_value={"stuff": 32,
                                                          "nested": {"about": "Inc.",
                                                                     "lst": ["Various", "Fields"]}},
                                       ))]),
                                       gql_type="Float")),
                              ])),
        ])],
    ),
])
def test_SchemaTransformer_values(full_sdl, expected_tree):
    raw_tree = parse_graphql_sdl_to_ast(full_sdl)
    cleaned_tree = CleaningTransformer(full_sdl).transform(raw_tree)
    schema_tree = SchemaTransformer(full_sdl, schema=GraphQLSchema()).transform(
        cleaned_tree)
    assert schema_tree == expected_tree

