import pytest

from tartiflette import Resolver, create_engine


@pytest.fixture(scope="module", name="ttftt_engine")
async def ttftt_engine_fixture():
    sdl = """
enum AnEnum {
    AValue
}

input AnInput {
    AField: String
}

type Query {
    simpleParameterField(i: Int, f: Float, s: String, e: AnEnum, input: AnInput): String
    nonNullParameterField(i: Int!, f: Float!, s: String!, e: AnEnum!, input: AnInput!): String
    listParameterField(i: [Int], f: [Float], s: [String], e: [AnEnum], input: [AnInput]): String
    listOfNonNullParameterField(i: [Int!], f: [Float!], s: [String!], e: [AnEnum!], input: [AnInput!]): String
    nonNullListParameterField(i: [Int]!, f: [Float]!, s: [String]!, e: [AnEnum]!, input: [AnInput]!): String
    nonNullListOfNonNullParameterField(i: [Int!]!, f: [Float!]!, s: [String!]!, e: [AnEnum!]!, input: [AnInput!]!): String
}
"""

    @Resolver(
        "Query.simpleParameterField",
        schema_name="test_validators_all_variable_usages_are_allowed",
    )
    @Resolver(
        "Query.nonNullParameterField",
        schema_name="test_validators_all_variable_usages_are_allowed",
    )
    @Resolver(
        "Query.listParameterField",
        schema_name="test_validators_all_variable_usages_are_allowed",
    )
    @Resolver(
        "Query.listOfNonNullParameterField",
        schema_name="test_validators_all_variable_usages_are_allowed",
    )
    @Resolver(
        "Query.nonNullListParameterField",
        schema_name="test_validators_all_variable_usages_are_allowed",
    )
    @Resolver(
        "Query.nonNullListOfNonNullParameterField",
        schema_name="test_validators_all_variable_usages_are_allowed",
    )
    async def resolver(_pr, args, _ctx, _info):
        return str(args)

    return await create_engine(
        sdl, schema_name="test_validators_all_variable_usages_are_allowed"
    )


@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
            query($i: Int, $f: Float, $s: String, $e: AnEnum, $input: AnInput) {
                simpleParameterField(i: $i, f: $f, s:$s, e:$e, input: $input)
                nonNullParameterField(i: $i, f: $f, s:$s, e:$e, input: $input)
                listParameterField(i: $i, f: $f, s:$s, e:$e, input: $input)
                listOfNonNullParameterField(i: $i, f: $f, s:$s, e:$e, input: $input)
                nonNullListParameterField(i: $i, f: $f, s:$s, e:$e, input: $input)
                nonNullListOfNonNullParameterField(i: $i, f: $f, s:$s, e:$e, input: $input)
            }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Can't use < $i / Int > for type < Int! >.",
                        "path": ["nonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 19},
                            {"line": 4, "column": 42},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $f / Float > for type < Float! >.",
                        "path": ["nonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 28},
                            {"line": 4, "column": 49},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $s / String > for type < String! >.",
                        "path": ["nonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 39},
                            {"line": 4, "column": 55},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $e / AnEnum > for type < AnEnum! >.",
                        "path": ["nonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 51},
                            {"line": 4, "column": 61},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $input / AnInput > for type < AnInput! >.",
                        "path": ["nonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 63},
                            {"line": 4, "column": 72},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $i / Int > for type < [Int] >.",
                        "path": ["listParameterField"],
                        "locations": [
                            {"line": 2, "column": 19},
                            {"line": 5, "column": 39},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $f / Float > for type < [Float] >.",
                        "path": ["listParameterField"],
                        "locations": [
                            {"line": 2, "column": 28},
                            {"line": 5, "column": 46},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $s / String > for type < [String] >.",
                        "path": ["listParameterField"],
                        "locations": [
                            {"line": 2, "column": 39},
                            {"line": 5, "column": 52},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $e / AnEnum > for type < [AnEnum] >.",
                        "path": ["listParameterField"],
                        "locations": [
                            {"line": 2, "column": 51},
                            {"line": 5, "column": 58},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $input / AnInput > for type < [AnInput] >.",
                        "path": ["listParameterField"],
                        "locations": [
                            {"line": 2, "column": 63},
                            {"line": 5, "column": 69},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $i / Int > for type < [Int!] >.",
                        "path": ["listOfNonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 19},
                            {"line": 6, "column": 48},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $f / Float > for type < [Float!] >.",
                        "path": ["listOfNonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 28},
                            {"line": 6, "column": 55},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $s / String > for type < [String!] >.",
                        "path": ["listOfNonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 39},
                            {"line": 6, "column": 61},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $e / AnEnum > for type < [AnEnum!] >.",
                        "path": ["listOfNonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 51},
                            {"line": 6, "column": 67},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $input / AnInput > for type < [AnInput!] >.",
                        "path": ["listOfNonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 63},
                            {"line": 6, "column": 78},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $i / Int > for type < [Int]! >.",
                        "path": ["nonNullListParameterField"],
                        "locations": [
                            {"line": 2, "column": 19},
                            {"line": 7, "column": 46},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $f / Float > for type < [Float]! >.",
                        "path": ["nonNullListParameterField"],
                        "locations": [
                            {"line": 2, "column": 28},
                            {"line": 7, "column": 53},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $s / String > for type < [String]! >.",
                        "path": ["nonNullListParameterField"],
                        "locations": [
                            {"line": 2, "column": 39},
                            {"line": 7, "column": 59},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $e / AnEnum > for type < [AnEnum]! >.",
                        "path": ["nonNullListParameterField"],
                        "locations": [
                            {"line": 2, "column": 51},
                            {"line": 7, "column": 65},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $input / AnInput > for type < [AnInput]! >.",
                        "path": ["nonNullListParameterField"],
                        "locations": [
                            {"line": 2, "column": 63},
                            {"line": 7, "column": 76},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $i / Int > for type < [Int!]! >.",
                        "path": ["nonNullListOfNonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 19},
                            {"line": 8, "column": 55},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $f / Float > for type < [Float!]! >.",
                        "path": ["nonNullListOfNonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 28},
                            {"line": 8, "column": 62},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $s / String > for type < [String!]! >.",
                        "path": ["nonNullListOfNonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 39},
                            {"line": 8, "column": 68},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $e / AnEnum > for type < [AnEnum!]! >.",
                        "path": ["nonNullListOfNonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 51},
                            {"line": 8, "column": 74},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $input / AnInput > for type < [AnInput!]! >.",
                        "path": ["nonNullListOfNonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 63},
                            {"line": 8, "column": 85},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                ],
            },
        ),
        (
            """
            query($i: Int!, $f: Float!, $s: String!, $e: AnEnum!, $input: AnInput!) {
                simpleParameterField(i: $i, f: $f, s:$s, e:$e, input: $input)
                nonNullParameterField(i: $i, f: $f, s:$s, e:$e, input: $input)
                listParameterField(i: $i, f: $f, s:$s, e:$e, input: $input)
                listOfNonNullParameterField(i: $i, f: $f, s:$s, e:$e, input: $input)
                nonNullListParameterField(i: $i, f: $f, s:$s, e:$e, input: $input)
                nonNullListOfNonNullParameterField(i: $i, f: $f, s:$s, e:$e, input: $input)
            }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Can't use < $i / Int! > for type < [Int] >.",
                        "path": ["listParameterField"],
                        "locations": [
                            {"line": 2, "column": 19},
                            {"line": 5, "column": 39},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $f / Float! > for type < [Float] >.",
                        "path": ["listParameterField"],
                        "locations": [
                            {"line": 2, "column": 29},
                            {"line": 5, "column": 46},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $s / String! > for type < [String] >.",
                        "path": ["listParameterField"],
                        "locations": [
                            {"line": 2, "column": 41},
                            {"line": 5, "column": 52},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $e / AnEnum! > for type < [AnEnum] >.",
                        "path": ["listParameterField"],
                        "locations": [
                            {"line": 2, "column": 54},
                            {"line": 5, "column": 58},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $input / AnInput! > for type < [AnInput] >.",
                        "path": ["listParameterField"],
                        "locations": [
                            {"line": 2, "column": 67},
                            {"line": 5, "column": 69},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $i / Int! > for type < [Int!] >.",
                        "path": ["listOfNonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 19},
                            {"line": 6, "column": 48},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $f / Float! > for type < [Float!] >.",
                        "path": ["listOfNonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 29},
                            {"line": 6, "column": 55},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $s / String! > for type < [String!] >.",
                        "path": ["listOfNonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 41},
                            {"line": 6, "column": 61},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $e / AnEnum! > for type < [AnEnum!] >.",
                        "path": ["listOfNonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 54},
                            {"line": 6, "column": 67},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $input / AnInput! > for type < [AnInput!] >.",
                        "path": ["listOfNonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 67},
                            {"line": 6, "column": 78},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $i / Int! > for type < [Int]! >.",
                        "path": ["nonNullListParameterField"],
                        "locations": [
                            {"line": 2, "column": 19},
                            {"line": 7, "column": 46},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $f / Float! > for type < [Float]! >.",
                        "path": ["nonNullListParameterField"],
                        "locations": [
                            {"line": 2, "column": 29},
                            {"line": 7, "column": 53},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $s / String! > for type < [String]! >.",
                        "path": ["nonNullListParameterField"],
                        "locations": [
                            {"line": 2, "column": 41},
                            {"line": 7, "column": 59},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $e / AnEnum! > for type < [AnEnum]! >.",
                        "path": ["nonNullListParameterField"],
                        "locations": [
                            {"line": 2, "column": 54},
                            {"line": 7, "column": 65},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $input / AnInput! > for type < [AnInput]! >.",
                        "path": ["nonNullListParameterField"],
                        "locations": [
                            {"line": 2, "column": 67},
                            {"line": 7, "column": 76},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $i / Int! > for type < [Int!]! >.",
                        "path": ["nonNullListOfNonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 19},
                            {"line": 8, "column": 55},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $f / Float! > for type < [Float!]! >.",
                        "path": ["nonNullListOfNonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 29},
                            {"line": 8, "column": 62},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $s / String! > for type < [String!]! >.",
                        "path": ["nonNullListOfNonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 41},
                            {"line": 8, "column": 68},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $e / AnEnum! > for type < [AnEnum!]! >.",
                        "path": ["nonNullListOfNonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 54},
                            {"line": 8, "column": 74},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $input / AnInput! > for type < [AnInput!]! >.",
                        "path": ["nonNullListOfNonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 67},
                            {"line": 8, "column": 85},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                ],
            },
        ),
        (
            """
            query($i: [Int!], $f: [Float!], $s: [String!], $e: [AnEnum!], $input: [AnInput!]) {
                simpleParameterField(i: $i, f: $f, s:$s, e:$e, input: $input)
                nonNullParameterField(i: $i, f: $f, s:$s, e:$e, input: $input)
                listParameterField(i: $i, f: $f, s:$s, e:$e, input: $input)
                listOfNonNullParameterField(i: $i, f: $f, s:$s, e:$e, input: $input)
                nonNullListParameterField(i: $i, f: $f, s:$s, e:$e, input: $input)
                nonNullListOfNonNullParameterField(i: $i, f: $f, s:$s, e:$e, input: $input)
            }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Can't use < $i / [Int!] > for type < Int >.",
                        "path": ["simpleParameterField"],
                        "locations": [
                            {"line": 2, "column": 19},
                            {"line": 3, "column": 41},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $f / [Float!] > for type < Float >.",
                        "path": ["simpleParameterField"],
                        "locations": [
                            {"line": 2, "column": 31},
                            {"line": 3, "column": 48},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $s / [String!] > for type < String >.",
                        "path": ["simpleParameterField"],
                        "locations": [
                            {"line": 2, "column": 45},
                            {"line": 3, "column": 54},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $e / [AnEnum!] > for type < AnEnum >.",
                        "path": ["simpleParameterField"],
                        "locations": [
                            {"line": 2, "column": 60},
                            {"line": 3, "column": 60},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $input / [AnInput!] > for type < AnInput >.",
                        "path": ["simpleParameterField"],
                        "locations": [
                            {"line": 2, "column": 75},
                            {"line": 3, "column": 71},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $i / [Int!] > for type < Int! >.",
                        "path": ["nonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 19},
                            {"line": 4, "column": 42},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $f / [Float!] > for type < Float! >.",
                        "path": ["nonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 31},
                            {"line": 4, "column": 49},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $s / [String!] > for type < String! >.",
                        "path": ["nonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 45},
                            {"line": 4, "column": 55},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $e / [AnEnum!] > for type < AnEnum! >.",
                        "path": ["nonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 60},
                            {"line": 4, "column": 61},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $input / [AnInput!] > for type < AnInput! >.",
                        "path": ["nonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 75},
                            {"line": 4, "column": 72},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $i / [Int!] > for type < [Int]! >.",
                        "path": ["nonNullListParameterField"],
                        "locations": [
                            {"line": 2, "column": 19},
                            {"line": 7, "column": 46},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $f / [Float!] > for type < [Float]! >.",
                        "path": ["nonNullListParameterField"],
                        "locations": [
                            {"line": 2, "column": 31},
                            {"line": 7, "column": 53},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $s / [String!] > for type < [String]! >.",
                        "path": ["nonNullListParameterField"],
                        "locations": [
                            {"line": 2, "column": 45},
                            {"line": 7, "column": 59},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $e / [AnEnum!] > for type < [AnEnum]! >.",
                        "path": ["nonNullListParameterField"],
                        "locations": [
                            {"line": 2, "column": 60},
                            {"line": 7, "column": 65},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $input / [AnInput!] > for type < [AnInput]! >.",
                        "path": ["nonNullListParameterField"],
                        "locations": [
                            {"line": 2, "column": 75},
                            {"line": 7, "column": 76},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $i / [Int!] > for type < [Int!]! >.",
                        "path": ["nonNullListOfNonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 19},
                            {"line": 8, "column": 55},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $f / [Float!] > for type < [Float!]! >.",
                        "path": ["nonNullListOfNonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 31},
                            {"line": 8, "column": 62},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $s / [String!] > for type < [String!]! >.",
                        "path": ["nonNullListOfNonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 45},
                            {"line": 8, "column": 68},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $e / [AnEnum!] > for type < [AnEnum!]! >.",
                        "path": ["nonNullListOfNonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 60},
                            {"line": 8, "column": 74},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $input / [AnInput!] > for type < [AnInput!]! >.",
                        "path": ["nonNullListOfNonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 75},
                            {"line": 8, "column": 85},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                ],
            },
        ),
        (
            """
            query($i: [Int!]!, $f: [Float!]!, $s: [String!]!, $e: [AnEnum!]!, $input: [AnInput!]!) {
                simpleParameterField(i: $i, f: $f, s:$s, e:$e, input: $input)
                nonNullParameterField(i: $i, f: $f, s:$s, e:$e, input: $input)
                listParameterField(i: $i, f: $f, s:$s, e:$e, input: $input)
                listOfNonNullParameterField(i: $i, f: $f, s:$s, e:$e, input: $input)
                nonNullListParameterField(i: $i, f: $f, s:$s, e:$e, input: $input)
                nonNullListOfNonNullParameterField(i: $i, f: $f, s:$s, e:$e, input: $input)
            }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Can't use < $i / [Int!]! > for type < Int >.",
                        "path": ["simpleParameterField"],
                        "locations": [
                            {"line": 2, "column": 19},
                            {"line": 3, "column": 41},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $f / [Float!]! > for type < Float >.",
                        "path": ["simpleParameterField"],
                        "locations": [
                            {"line": 2, "column": 32},
                            {"line": 3, "column": 48},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $s / [String!]! > for type < String >.",
                        "path": ["simpleParameterField"],
                        "locations": [
                            {"line": 2, "column": 47},
                            {"line": 3, "column": 54},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $e / [AnEnum!]! > for type < AnEnum >.",
                        "path": ["simpleParameterField"],
                        "locations": [
                            {"line": 2, "column": 63},
                            {"line": 3, "column": 60},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $input / [AnInput!]! > for type < AnInput >.",
                        "path": ["simpleParameterField"],
                        "locations": [
                            {"line": 2, "column": 79},
                            {"line": 3, "column": 71},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $i / [Int!]! > for type < Int! >.",
                        "path": ["nonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 19},
                            {"line": 4, "column": 42},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $f / [Float!]! > for type < Float! >.",
                        "path": ["nonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 32},
                            {"line": 4, "column": 49},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $s / [String!]! > for type < String! >.",
                        "path": ["nonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 47},
                            {"line": 4, "column": 55},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $e / [AnEnum!]! > for type < AnEnum! >.",
                        "path": ["nonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 63},
                            {"line": 4, "column": 61},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $input / [AnInput!]! > for type < AnInput! >.",
                        "path": ["nonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 79},
                            {"line": 4, "column": 72},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                ],
            },
        ),
        (
            """
            query($i: [Int]!, $f: [Float]!, $s: [String]!, $e: [AnEnum]!, $input: [AnInput]!) {
                simpleParameterField(i: $i, f: $f, s:$s, e:$e, input: $input)
                nonNullParameterField(i: $i, f: $f, s:$s, e:$e, input: $input)
                listParameterField(i: $i, f: $f, s:$s, e:$e, input: $input)
                listOfNonNullParameterField(i: $i, f: $f, s:$s, e:$e, input: $input)
                nonNullListParameterField(i: $i, f: $f, s:$s, e:$e, input: $input)
                nonNullListOfNonNullParameterField(i: $i, f: $f, s:$s, e:$e, input: $input)
            }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Can't use < $i / [Int]! > for type < Int >.",
                        "path": ["simpleParameterField"],
                        "locations": [
                            {"line": 2, "column": 19},
                            {"line": 3, "column": 41},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $f / [Float]! > for type < Float >.",
                        "path": ["simpleParameterField"],
                        "locations": [
                            {"line": 2, "column": 31},
                            {"line": 3, "column": 48},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $s / [String]! > for type < String >.",
                        "path": ["simpleParameterField"],
                        "locations": [
                            {"line": 2, "column": 45},
                            {"line": 3, "column": 54},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $e / [AnEnum]! > for type < AnEnum >.",
                        "path": ["simpleParameterField"],
                        "locations": [
                            {"line": 2, "column": 60},
                            {"line": 3, "column": 60},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $input / [AnInput]! > for type < AnInput >.",
                        "path": ["simpleParameterField"],
                        "locations": [
                            {"line": 2, "column": 75},
                            {"line": 3, "column": 71},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $i / [Int]! > for type < Int! >.",
                        "path": ["nonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 19},
                            {"line": 4, "column": 42},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $f / [Float]! > for type < Float! >.",
                        "path": ["nonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 31},
                            {"line": 4, "column": 49},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $s / [String]! > for type < String! >.",
                        "path": ["nonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 45},
                            {"line": 4, "column": 55},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $e / [AnEnum]! > for type < AnEnum! >.",
                        "path": ["nonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 60},
                            {"line": 4, "column": 61},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $input / [AnInput]! > for type < AnInput! >.",
                        "path": ["nonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 75},
                            {"line": 4, "column": 72},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $i / [Int]! > for type < [Int!] >.",
                        "path": ["listOfNonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 19},
                            {"line": 6, "column": 48},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $f / [Float]! > for type < [Float!] >.",
                        "path": ["listOfNonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 31},
                            {"line": 6, "column": 55},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $s / [String]! > for type < [String!] >.",
                        "path": ["listOfNonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 45},
                            {"line": 6, "column": 61},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $e / [AnEnum]! > for type < [AnEnum!] >.",
                        "path": ["listOfNonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 60},
                            {"line": 6, "column": 67},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $input / [AnInput]! > for type < [AnInput!] >.",
                        "path": ["listOfNonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 75},
                            {"line": 6, "column": 78},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $i / [Int]! > for type < [Int!]! >.",
                        "path": ["nonNullListOfNonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 19},
                            {"line": 8, "column": 55},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $f / [Float]! > for type < [Float!]! >.",
                        "path": ["nonNullListOfNonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 31},
                            {"line": 8, "column": 62},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $s / [String]! > for type < [String!]! >.",
                        "path": ["nonNullListOfNonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 45},
                            {"line": 8, "column": 68},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $e / [AnEnum]! > for type < [AnEnum!]! >.",
                        "path": ["nonNullListOfNonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 60},
                            {"line": 8, "column": 74},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $input / [AnInput]! > for type < [AnInput!]! >.",
                        "path": ["nonNullListOfNonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 75},
                            {"line": 8, "column": 85},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                ],
            },
        ),
        (
            """
            query($i: [Int], $f: [Float], $s: [String], $e: [AnEnum], $input: [AnInput]) {
                simpleParameterField(i: $i, f: $f, s:$s, e:$e, input: $input)
                nonNullParameterField(i: $i, f: $f, s:$s, e:$e, input: $input)
                listParameterField(i: $i, f: $f, s:$s, e:$e, input: $input)
                listOfNonNullParameterField(i: $i, f: $f, s:$s, e:$e, input: $input)
                nonNullListParameterField(i: $i, f: $f, s:$s, e:$e, input: $input)
                nonNullListOfNonNullParameterField(i: $i, f: $f, s:$s, e:$e, input: $input)
            }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Can't use < $i / [Int] > for type < Int >.",
                        "path": ["simpleParameterField"],
                        "locations": [
                            {"line": 2, "column": 19},
                            {"line": 3, "column": 41},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $f / [Float] > for type < Float >.",
                        "path": ["simpleParameterField"],
                        "locations": [
                            {"line": 2, "column": 30},
                            {"line": 3, "column": 48},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $s / [String] > for type < String >.",
                        "path": ["simpleParameterField"],
                        "locations": [
                            {"line": 2, "column": 43},
                            {"line": 3, "column": 54},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $e / [AnEnum] > for type < AnEnum >.",
                        "path": ["simpleParameterField"],
                        "locations": [
                            {"line": 2, "column": 57},
                            {"line": 3, "column": 60},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $input / [AnInput] > for type < AnInput >.",
                        "path": ["simpleParameterField"],
                        "locations": [
                            {"line": 2, "column": 71},
                            {"line": 3, "column": 71},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $i / [Int] > for type < Int! >.",
                        "path": ["nonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 19},
                            {"line": 4, "column": 42},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $f / [Float] > for type < Float! >.",
                        "path": ["nonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 30},
                            {"line": 4, "column": 49},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $s / [String] > for type < String! >.",
                        "path": ["nonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 43},
                            {"line": 4, "column": 55},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $e / [AnEnum] > for type < AnEnum! >.",
                        "path": ["nonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 57},
                            {"line": 4, "column": 61},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $input / [AnInput] > for type < AnInput! >.",
                        "path": ["nonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 71},
                            {"line": 4, "column": 72},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $i / [Int] > for type < [Int!] >.",
                        "path": ["listOfNonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 19},
                            {"line": 6, "column": 48},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $f / [Float] > for type < [Float!] >.",
                        "path": ["listOfNonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 30},
                            {"line": 6, "column": 55},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $s / [String] > for type < [String!] >.",
                        "path": ["listOfNonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 43},
                            {"line": 6, "column": 61},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $e / [AnEnum] > for type < [AnEnum!] >.",
                        "path": ["listOfNonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 57},
                            {"line": 6, "column": 67},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $input / [AnInput] > for type < [AnInput!] >.",
                        "path": ["listOfNonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 71},
                            {"line": 6, "column": 78},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $i / [Int] > for type < [Int]! >.",
                        "path": ["nonNullListParameterField"],
                        "locations": [
                            {"line": 2, "column": 19},
                            {"line": 7, "column": 46},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $f / [Float] > for type < [Float]! >.",
                        "path": ["nonNullListParameterField"],
                        "locations": [
                            {"line": 2, "column": 30},
                            {"line": 7, "column": 53},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $s / [String] > for type < [String]! >.",
                        "path": ["nonNullListParameterField"],
                        "locations": [
                            {"line": 2, "column": 43},
                            {"line": 7, "column": 59},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $e / [AnEnum] > for type < [AnEnum]! >.",
                        "path": ["nonNullListParameterField"],
                        "locations": [
                            {"line": 2, "column": 57},
                            {"line": 7, "column": 65},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $input / [AnInput] > for type < [AnInput]! >.",
                        "path": ["nonNullListParameterField"],
                        "locations": [
                            {"line": 2, "column": 71},
                            {"line": 7, "column": 76},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $i / [Int] > for type < [Int!]! >.",
                        "path": ["nonNullListOfNonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 19},
                            {"line": 8, "column": 55},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $f / [Float] > for type < [Float!]! >.",
                        "path": ["nonNullListOfNonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 30},
                            {"line": 8, "column": 62},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $s / [String] > for type < [String!]! >.",
                        "path": ["nonNullListOfNonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 43},
                            {"line": 8, "column": 68},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $e / [AnEnum] > for type < [AnEnum!]! >.",
                        "path": ["nonNullListOfNonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 57},
                            {"line": 8, "column": 74},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                    {
                        "message": "Can't use < $input / [AnInput] > for type < [AnInput!]! >.",
                        "path": ["nonNullListOfNonNullParameterField"],
                        "locations": [
                            {"line": 2, "column": 71},
                            {"line": 8, "column": 85},
                        ],
                        "extensions": {
                            "rule": "5.8.5",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed",
                            "tag": "all-variable-usages-are-allowed",
                        },
                    },
                ],
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_validators_all_variable_usages_are_allowed(
    query, expected, ttftt_engine
):
    assert await ttftt_engine.execute(query) == expected
