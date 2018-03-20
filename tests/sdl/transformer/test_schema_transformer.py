from collections import OrderedDict

import pytest
from lark.lexer import Token
from lark.tree import Tree

from tartiflette.sdl.builder import parse_graphql_sdl_to_ast
from tartiflette.sdl.schema import GraphQLSchema
from tartiflette.sdl.transformers import CleaningTransformer
from tartiflette.sdl.transformers.schema import GraphQLNamedType, \
    GraphQLScalarTypeDefinition, GraphQLUnionTypeDefinition, \
    GraphQLInterfaceTypeDefinition, GraphQLFieldDefinition, \
    GraphQLInputObjectTypeDefinition, GraphQLObjectTypeDefinition, \
    GraphQLArgumentDefinition, GraphQLEnumTypeDefinition, GraphQLEnumValue, \
    Description, Name, GraphQLEnumValueDefinition, GraphQLScalarValue
from tartiflette.sdl.transformers.schema_transformer import \
    SchemaTransformer


@pytest.mark.parametrize("full_sdl,expected_tree", [
    # The `name` rule cleans up the name Token
    (
        """
        \"\"\"
        Date scalar for storing Dates, very convenient
        \"\"\"
        scalar Date
        """,
        [Tree('type_definition', [
            GraphQLScalarTypeDefinition(name=Name("Date"),
                                        description=Description(
                description="\n        Date scalar for storing Dates, "
                            "very convenient\n        "
            )),
        ])],
    ),
    (
        """
        \"\"\"
        DateOrTimne scalar for storing Date or Time, very convenient also
        \"\"\"
        union DateOrTime = Date | Time
        """,
        [Tree('type_definition', [
            GraphQLUnionTypeDefinition(name=Name("DateOrtime"),
                                       types=[
                GraphQLNamedType(name="Date"),
                GraphQLNamedType(name="Time"),
            ], description=Description(
                description="\n        DateOrTimne scalar for storing Date or"
                            " Time, very convenient also\n        "
            )),
        ])],
    ),
    (
        """
        scalar Date
        union DateOrTime = Date | Time
        """,
        [Tree('type_definition', [
            GraphQLScalarTypeDefinition(name=Name("Date")),
        ]),
         Tree('type_definition', [
            GraphQLUnionTypeDefinition(name=Name("DateOrtime"), types=[
                GraphQLNamedType(name="Date"),
                GraphQLNamedType(name="Time"),
            ]),
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
            GraphQLInterfaceTypeDefinition(name=Name("Vehicle"), fields=OrderedDict([
                ("speedInKmh", GraphQLFieldDefinition(
                    name="speedInKmh", gql_type=GraphQLNamedType(name="Float"))),
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
            GraphQLInputObjectTypeDefinition(name=Name("UserProfileInput"),
                                             fields=OrderedDict([
                                                 ("fullName",
                                                  GraphQLArgumentDefinition(
                                                      name=Name("fullName"),
                                                      gql_type=GraphQLNamedType(
                                                          name="String"),
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
            GraphQLObjectTypeDefinition(name=Name("UserProfileInput"),
                                        fields=OrderedDict([
                                            ("modelName",
                                             GraphQLFieldDefinition(
                                                 name="modelName",
                                                 gql_type=GraphQLNamedType(
                                                     name="String"))),
                                            ("speedInKmh",
                                             GraphQLFieldDefinition(
                                                 name="speedInKmh",
                                                 gql_type=GraphQLNamedType(
                                                     name="Float"))),
                                        ]), interfaces=[
                    GraphQLNamedType(name="Vehicle"),
                ]),
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
                GraphQLNamedType(name='RootQuery'),
            ]),
            Tree('mutation_operation_type_definition', [
                Token('MUTATION', 'mutation'),
                GraphQLNamedType(name='RootMutation'),
            ]),
            Tree('subscription_operation_type_definition', [
                Token('SUBSCRIPTION', 'subscription'),
                GraphQLNamedType(name='RootSubscription'),
            ]),
        ])],
    ),
    (
        """
        enum Mode {
            Prod
            Test
            Dev
        }
        """,
        [Tree('type_definition', [
            GraphQLEnumTypeDefinition(name=Name("Mode"), values=[
                GraphQLEnumValueDefinition(key="Prod"),
                GraphQLEnumValueDefinition(key="Test"),
                GraphQLEnumValueDefinition(key="Dev"),
            ]),
        ])],
    ),
])
def test_SchemaTransformer_schema(full_sdl, expected_tree):

    raw_tree = parse_graphql_sdl_to_ast(full_sdl)
    cleaned_tree = CleaningTransformer(full_sdl).transform(raw_tree)
    assert SchemaTransformer(full_sdl, schema=GraphQLSchema()).transform(cleaned_tree) == expected_tree


@pytest.mark.parametrize("full_sdl,expected_tree", [
    (
        """
        type TestObject {
            birthDate(input: Date = "2018"): Date
        }
        """,
        [Tree('type_definition', [
            GraphQLObjectTypeDefinition(
                name=Name("TestObject"),
                fields=OrderedDict([
                    ("birthDate",
                     GraphQLFieldDefinition(
                         name="birthDate",
                         gql_type=GraphQLNamedType(
                             name=Name("Date")),
                         arguments=OrderedDict([
                             ("input", GraphQLArgumentDefinition(
                                 name=Name("input"),
                                 gql_type=GraphQLNamedType(name=Name("Date")),
                                 default_value=GraphQLScalarValue(value="2018"),
                             )),
                        ]))),
                ]),
                interfaces=[]),
        ])],
    ),
])
def test_SchemaTransformer_values(full_sdl, expected_tree):
    raw_tree = parse_graphql_sdl_to_ast(full_sdl)
    cleaned_tree = CleaningTransformer(full_sdl).transform(raw_tree)
    schema_tree = SchemaTransformer(full_sdl, schema=GraphQLSchema()).transform(
        cleaned_tree)
    assert schema_tree == expected_tree

