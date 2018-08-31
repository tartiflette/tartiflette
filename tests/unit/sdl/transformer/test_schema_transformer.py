from collections import OrderedDict

import pytest
from lark.lexer import Token
from lark.tree import Tree

from tartiflette.sdl.builder import parse_graphql_sdl_to_ast
from tartiflette.schema import GraphQLSchema
from tartiflette.sdl.transformers.cleaning_transformer import (
    CleaningTransformer
)
from tartiflette.sdl.transformers.schema_transformer import (
    SchemaTransformer,
    SchemaNode,
)
from tartiflette.types.argument import GraphQLArgument
from tartiflette.types.directive import GraphQLDirective
from tartiflette.types.enum import GraphQLEnumType, GraphQLEnumValue
from tartiflette.types.field import GraphQLField
from tartiflette.types.input_object import GraphQLInputObjectType
from tartiflette.types.interface import GraphQLInterfaceType
from tartiflette.types.object import GraphQLObjectType
from tartiflette.types.scalar import GraphQLScalarType
from tartiflette.types.union import GraphQLUnionType

from tests.unit.utils import call_with_mocked_resolver_factory


@pytest.mark.parametrize(
    "full_sdl,expected_tree",
    [
        (
            """
        \"\"\"
        Date scalar for storing Dates, very convenient
        \"\"\"
        scalar Date
        """,
            [
                Tree(
                    "type_definition",
                    [
                        call_with_mocked_resolver_factory(
                            GraphQLScalarType,
                            name="Date",
                            description="\n        Date scalar for "
                            "storing Dates, "
                            "very convenient\n        ",
                        )
                    ],
                )
            ],
        ),
        (
            """
        \"\"\"
        DateOrTime scalar for storing Date or Time, very convenient also
        \"\"\"
        union DateOrTime = Date | Time
        """,
            [
                Tree(
                    "type_definition",
                    [
                        call_with_mocked_resolver_factory(
                            GraphQLUnionType,
                            name="DateOrTime",
                            gql_types=["Date", "Time"],
                            description="\n        DateOrTime scalar for "
                            "storing Date or Time, very "
                            "convenient also\n        ",
                        )
                    ],
                )
            ],
        ),
        (
            """
        scalar Date
        union DateOrTime = Date | Time
        """,
            [
                Tree(
                    "type_definition",
                    [
                        call_with_mocked_resolver_factory(
                            GraphQLScalarType, name="Date"
                        )
                    ],
                ),
                Tree(
                    "type_definition",
                    [
                        call_with_mocked_resolver_factory(
                            GraphQLUnionType,
                            name="DateOrTime",
                            gql_types=["Date", "Time"],
                        )
                    ],
                ),
            ],
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
            [
                Tree(
                    "type_definition",
                    [
                        call_with_mocked_resolver_factory(
                            GraphQLInterfaceType,
                            name="Vehicle",
                            fields=OrderedDict(
                                [
                                    (
                                        "speedInKmh",
                                        call_with_mocked_resolver_factory(
                                            GraphQLField,
                                            name="speedInKmh",
                                            gql_type="Float",
                                        ),
                                    )
                                ]
                            ),
                        )
                    ],
                )
            ],
        ),
        (
            """
        input UserProfileInput {
            fullName: String
        }
        """,
            [
                Tree(
                    "type_definition",
                    [
                        call_with_mocked_resolver_factory(
                            GraphQLInputObjectType,
                            name="UserProfileInput",
                            fields=OrderedDict(
                                [
                                    (
                                        "fullName",
                                        call_with_mocked_resolver_factory(
                                            GraphQLArgument,
                                            name="fullName",
                                            gql_type="String",
                                        ),
                                    )
                                ]
                            ),
                        )
                    ],
                )
            ],
        ),
        (
            """
        type Car implements Vehicle {
            modelName: String
            speedInKmh: Float
        }
        """,
            [
                Tree(
                    "type_definition",
                    [
                        call_with_mocked_resolver_factory(
                            GraphQLObjectType,
                            name="Car",
                            fields=OrderedDict(
                                [
                                    (
                                        "modelName",
                                        call_with_mocked_resolver_factory(
                                            GraphQLField,
                                            name="modelName",
                                            gql_type="String",
                                        ),
                                    ),
                                    (
                                        "speedInKmh",
                                        call_with_mocked_resolver_factory(
                                            GraphQLField,
                                            name="speedInKmh",
                                            gql_type="Float",
                                        ),
                                    ),
                                ]
                            ),
                            interfaces=["Vehicle"],
                        )
                    ],
                )
            ],
        ),
        (
            """
        schema {
            query: RootQuery
            mutation: RootMutation
            subscription: RootSubscription
        }
        """,
            [
                Tree(
                    "schema_definition",
                    [
                        Token("SCHEMA", "schema"),
                        Tree(
                            "query_operation_type_definition",
                            [
                                Token("QUERY", "query"),
                                SchemaNode(
                                    type="named_type", value="RootQuery"
                                ),
                            ],
                        ),
                        Tree(
                            "mutation_operation_type_definition",
                            [
                                Token("MUTATION", "mutation"),
                                SchemaNode(
                                    type="named_type", value="RootMutation"
                                ),
                            ],
                        ),
                        Tree(
                            "subscription_operation_type_definition",
                            [
                                Token("SUBSCRIPTION", "subscription"),
                                SchemaNode(
                                    type="named_type", value="RootSubscription"
                                ),
                            ],
                        ),
                    ],
                )
            ],
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
            [
                Tree(
                    "type_definition",
                    [
                        call_with_mocked_resolver_factory(GraphQLEnumType,
                            name="Mode",
                            values=[
                                call_with_mocked_resolver_factory(GraphQLEnumValue,
                                    value="Prod",
                                    description="\n            Used "
                                    "for any production "
                                    "system\n           "
                                    " ",
                                ),
                                call_with_mocked_resolver_factory(GraphQLEnumValue,value="Test"),
                                call_with_mocked_resolver_factory(GraphQLEnumValue,value="Dev"),
                            ],
                            description="\n        The enum Mode is "
                            "used to switch environments.\n        ",
                        )
                    ],
                )
            ],
        ),
        (
            """
        \"\"\"
        This is a description of the directive.
        \"\"\"
        directive @deprecated(firstArg: Int, anotherArg: InputType) on SCHEMA | FIELD_DEFINITION
        """,
            [
                Tree(
                    "directive_definition",
                    [
                        call_with_mocked_resolver_factory(GraphQLDirective,
                            name="deprecated",
                            on=["SCHEMA", "FIELD_DEFINITION"],
                            arguments=OrderedDict(
                                [
                                    (
                                        "firstArg",
                                        call_with_mocked_resolver_factory(GraphQLArgument,
                                            name="firstArg", gql_type="Int"
                                        ),
                                    ),
                                    (
                                        "anotherArg",
                                        call_with_mocked_resolver_factory(GraphQLArgument,
                                            name="anotherArg",
                                            gql_type="InputType",
                                        ),
                                    ),
                                ]
                            ),
                            description="\n        This is a description of the directive.\n        ",
                        )
                    ],
                )
            ],
        ),
    ],
)
def test_SchemaTransformer_schema(full_sdl, expected_tree, mocked_resolver_factory):
    raw_tree = parse_graphql_sdl_to_ast(full_sdl)
    cleaned_tree = CleaningTransformer(full_sdl).transform(raw_tree)
    assert (
        SchemaTransformer(full_sdl, schema=GraphQLSchema()).transform(
            cleaned_tree
        )
        == expected_tree
    )


@pytest.mark.parametrize(
    "full_sdl,expected_tree",
    [
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
            [
                Tree(
                    "type_definition",
                    [
                        call_with_mocked_resolver_factory(GraphQLObjectType,
                            name="TestObject",
                            fields=OrderedDict(
                                [
                                    (
                                        "birthDate",
                                        call_with_mocked_resolver_factory(
                                            GraphQLField,
                                            name="birthDate",
                                            gql_type="Date",
                                            arguments=OrderedDict(
                                                [
                                                    (
                                                        "input",
                                                        call_with_mocked_resolver_factory(GraphQLArgument,
                                                            name="input",
                                                            gql_type="Date",
                                                            default_value="2018",
                                                        ),
                                                    )
                                                ]
                                            ),
                                        ),
                                    )
                                ]
                            ),
                            interfaces=None,
                        )
                    ],
                )
            ],
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
            [
                Tree(
                    "type_definition",
                    [
                        call_with_mocked_resolver_factory(GraphQLObjectType,
                            name="Car",
                            fields=OrderedDict(
                                [
                                    (
                                        "modelName",
                                        call_with_mocked_resolver_factory(
                                            GraphQLField,
                                            name="modelName",
                                            arguments=OrderedDict(
                                                [
                                                    (
                                                        "arg",
                                                        call_with_mocked_resolver_factory(GraphQLArgument,
                                                            name="arg",
                                                            gql_type="Int",
                                                            default_value=42,
                                                        ),
                                                    )
                                                ]
                                            ),
                                            gql_type="String",
                                        ),
                                    ),
                                    (
                                        "speedInKmh",
                                        call_with_mocked_resolver_factory(
                                            GraphQLField,
                                            name="speedInKmh",
                                            arguments=OrderedDict(
                                                [
                                                    (
                                                        "cplx",
                                                        call_with_mocked_resolver_factory(GraphQLArgument,
                                                            name="cplx",
                                                            gql_type="InputObject",
                                                            default_value={
                                                                "stuff": 32,
                                                                "nested": {
                                                                    "about": "Inc.",
                                                                    "lst": [
                                                                        "Various",
                                                                        "Fields",
                                                                    ],
                                                                },
                                                            },
                                                        ),
                                                    )
                                                ]
                                            ),
                                            gql_type="Float",
                                        ),
                                    ),
                                ]
                            ),
                        )
                    ],
                )
            ],
        ),
    ],
)
def test_SchemaTransformer_values(full_sdl, expected_tree, mocked_resolver_factory):
    raw_tree = parse_graphql_sdl_to_ast(full_sdl)
    cleaned_tree = CleaningTransformer(full_sdl).transform(raw_tree)
    schema_tree = SchemaTransformer(
        full_sdl, schema=GraphQLSchema()
    ).transform(cleaned_tree)
    assert schema_tree == expected_tree
