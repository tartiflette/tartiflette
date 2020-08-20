import pytest

from tartiflette import Resolver


def bakery(schema_name):
    @Resolver("Query.simpleParameterField", schema_name=schema_name)
    @Resolver("Query.nonNullParameterField", schema_name=schema_name)
    @Resolver("Query.listParameterField", schema_name=schema_name)
    @Resolver("Query.listOfNonNullParameterField", schema_name=schema_name)
    @Resolver("Query.nonNullListParameterField", schema_name=schema_name)
    @Resolver(
        "Query.nonNullListOfNonNullParameterField", schema_name=schema_name
    )
    async def resolve_stringify(_pr, args, _ctx, _info):
        return str(args)


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl="""
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
    """,
    bakery=bakery,
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
                        "message": "Variable < $i > of type < Int > used in position expecting type < Int! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 19},
                            {"line": 4, "column": 42},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $f > of type < Float > used in position expecting type < Float! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 28},
                            {"line": 4, "column": 49},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $s > of type < String > used in position expecting type < String! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 39},
                            {"line": 4, "column": 55},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $e > of type < AnEnum > used in position expecting type < AnEnum! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 51},
                            {"line": 4, "column": 61},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $input > of type < AnInput > used in position expecting type < AnInput! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 63},
                            {"line": 4, "column": 72},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $i > of type < Int > used in position expecting type < [Int] >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 19},
                            {"line": 5, "column": 39},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $f > of type < Float > used in position expecting type < [Float] >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 28},
                            {"line": 5, "column": 46},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $s > of type < String > used in position expecting type < [String] >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 39},
                            {"line": 5, "column": 52},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $e > of type < AnEnum > used in position expecting type < [AnEnum] >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 51},
                            {"line": 5, "column": 58},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $input > of type < AnInput > used in position expecting type < [AnInput] >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 63},
                            {"line": 5, "column": 69},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $i > of type < Int > used in position expecting type < [Int!] >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 19},
                            {"line": 6, "column": 48},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $f > of type < Float > used in position expecting type < [Float!] >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 28},
                            {"line": 6, "column": 55},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $s > of type < String > used in position expecting type < [String!] >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 39},
                            {"line": 6, "column": 61},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $e > of type < AnEnum > used in position expecting type < [AnEnum!] >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 51},
                            {"line": 6, "column": 67},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $input > of type < AnInput > used in position expecting type < [AnInput!] >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 63},
                            {"line": 6, "column": 78},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $i > of type < Int > used in position expecting type < [Int]! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 19},
                            {"line": 7, "column": 46},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $f > of type < Float > used in position expecting type < [Float]! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 28},
                            {"line": 7, "column": 53},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $s > of type < String > used in position expecting type < [String]! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 39},
                            {"line": 7, "column": 59},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $e > of type < AnEnum > used in position expecting type < [AnEnum]! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 51},
                            {"line": 7, "column": 65},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $input > of type < AnInput > used in position expecting type < [AnInput]! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 63},
                            {"line": 7, "column": 76},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $i > of type < Int > used in position expecting type < [Int!]! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 19},
                            {"line": 8, "column": 55},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $f > of type < Float > used in position expecting type < [Float!]! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 28},
                            {"line": 8, "column": 62},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $s > of type < String > used in position expecting type < [String!]! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 39},
                            {"line": 8, "column": 68},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $e > of type < AnEnum > used in position expecting type < [AnEnum!]! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 51},
                            {"line": 8, "column": 74},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $input > of type < AnInput > used in position expecting type < [AnInput!]! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 63},
                            {"line": 8, "column": 85},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
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
                        "message": "Variable < $i > of type < Int! > used in position expecting type < [Int] >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 19},
                            {"line": 5, "column": 39},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $f > of type < Float! > used in position expecting type < [Float] >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 29},
                            {"line": 5, "column": 46},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $s > of type < String! > used in position expecting type < [String] >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 41},
                            {"line": 5, "column": 52},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $e > of type < AnEnum! > used in position expecting type < [AnEnum] >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 54},
                            {"line": 5, "column": 58},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $input > of type < AnInput! > used in position expecting type < [AnInput] >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 67},
                            {"line": 5, "column": 69},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $i > of type < Int! > used in position expecting type < [Int!] >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 19},
                            {"line": 6, "column": 48},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $f > of type < Float! > used in position expecting type < [Float!] >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 29},
                            {"line": 6, "column": 55},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $s > of type < String! > used in position expecting type < [String!] >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 41},
                            {"line": 6, "column": 61},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $e > of type < AnEnum! > used in position expecting type < [AnEnum!] >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 54},
                            {"line": 6, "column": 67},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $input > of type < AnInput! > used in position expecting type < [AnInput!] >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 67},
                            {"line": 6, "column": 78},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $i > of type < Int! > used in position expecting type < [Int]! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 19},
                            {"line": 7, "column": 46},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $f > of type < Float! > used in position expecting type < [Float]! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 29},
                            {"line": 7, "column": 53},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $s > of type < String! > used in position expecting type < [String]! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 41},
                            {"line": 7, "column": 59},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $e > of type < AnEnum! > used in position expecting type < [AnEnum]! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 54},
                            {"line": 7, "column": 65},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $input > of type < AnInput! > used in position expecting type < [AnInput]! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 67},
                            {"line": 7, "column": 76},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $i > of type < Int! > used in position expecting type < [Int!]! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 19},
                            {"line": 8, "column": 55},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $f > of type < Float! > used in position expecting type < [Float!]! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 29},
                            {"line": 8, "column": 62},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $s > of type < String! > used in position expecting type < [String!]! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 41},
                            {"line": 8, "column": 68},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $e > of type < AnEnum! > used in position expecting type < [AnEnum!]! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 54},
                            {"line": 8, "column": 74},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $input > of type < AnInput! > used in position expecting type < [AnInput!]! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 67},
                            {"line": 8, "column": 85},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
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
                        "message": "Variable < $i > of type < [Int!] > used in position expecting type < Int >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 19},
                            {"line": 3, "column": 41},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $f > of type < [Float!] > used in position expecting type < Float >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 31},
                            {"line": 3, "column": 48},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $s > of type < [String!] > used in position expecting type < String >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 45},
                            {"line": 3, "column": 54},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $e > of type < [AnEnum!] > used in position expecting type < AnEnum >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 60},
                            {"line": 3, "column": 60},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $input > of type < [AnInput!] > used in position expecting type < AnInput >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 75},
                            {"line": 3, "column": 71},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $i > of type < [Int!] > used in position expecting type < Int! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 19},
                            {"line": 4, "column": 42},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $f > of type < [Float!] > used in position expecting type < Float! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 31},
                            {"line": 4, "column": 49},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $s > of type < [String!] > used in position expecting type < String! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 45},
                            {"line": 4, "column": 55},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $e > of type < [AnEnum!] > used in position expecting type < AnEnum! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 60},
                            {"line": 4, "column": 61},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $input > of type < [AnInput!] > used in position expecting type < AnInput! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 75},
                            {"line": 4, "column": 72},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $i > of type < [Int!] > used in position expecting type < [Int]! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 19},
                            {"line": 7, "column": 46},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $f > of type < [Float!] > used in position expecting type < [Float]! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 31},
                            {"line": 7, "column": 53},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $s > of type < [String!] > used in position expecting type < [String]! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 45},
                            {"line": 7, "column": 59},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $e > of type < [AnEnum!] > used in position expecting type < [AnEnum]! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 60},
                            {"line": 7, "column": 65},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $input > of type < [AnInput!] > used in position expecting type < [AnInput]! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 75},
                            {"line": 7, "column": 76},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $i > of type < [Int!] > used in position expecting type < [Int!]! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 19},
                            {"line": 8, "column": 55},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $f > of type < [Float!] > used in position expecting type < [Float!]! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 31},
                            {"line": 8, "column": 62},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $s > of type < [String!] > used in position expecting type < [String!]! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 45},
                            {"line": 8, "column": 68},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $e > of type < [AnEnum!] > used in position expecting type < [AnEnum!]! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 60},
                            {"line": 8, "column": 74},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $input > of type < [AnInput!] > used in position expecting type < [AnInput!]! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 75},
                            {"line": 8, "column": 85},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
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
                        "message": "Variable < $i > of type < [Int!]! > used in position expecting type < Int >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 19},
                            {"line": 3, "column": 41},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $f > of type < [Float!]! > used in position expecting type < Float >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 32},
                            {"line": 3, "column": 48},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $s > of type < [String!]! > used in position expecting type < String >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 47},
                            {"line": 3, "column": 54},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $e > of type < [AnEnum!]! > used in position expecting type < AnEnum >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 63},
                            {"line": 3, "column": 60},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $input > of type < [AnInput!]! > used in position expecting type < AnInput >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 79},
                            {"line": 3, "column": 71},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $i > of type < [Int!]! > used in position expecting type < Int! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 19},
                            {"line": 4, "column": 42},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $f > of type < [Float!]! > used in position expecting type < Float! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 32},
                            {"line": 4, "column": 49},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $s > of type < [String!]! > used in position expecting type < String! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 47},
                            {"line": 4, "column": 55},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $e > of type < [AnEnum!]! > used in position expecting type < AnEnum! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 63},
                            {"line": 4, "column": 61},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $input > of type < [AnInput!]! > used in position expecting type < AnInput! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 79},
                            {"line": 4, "column": 72},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
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
                        "message": "Variable < $i > of type < [Int]! > used in position expecting type < Int >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 19},
                            {"line": 3, "column": 41},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $f > of type < [Float]! > used in position expecting type < Float >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 31},
                            {"line": 3, "column": 48},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $s > of type < [String]! > used in position expecting type < String >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 45},
                            {"line": 3, "column": 54},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $e > of type < [AnEnum]! > used in position expecting type < AnEnum >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 60},
                            {"line": 3, "column": 60},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $input > of type < [AnInput]! > used in position expecting type < AnInput >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 75},
                            {"line": 3, "column": 71},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $i > of type < [Int]! > used in position expecting type < Int! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 19},
                            {"line": 4, "column": 42},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $f > of type < [Float]! > used in position expecting type < Float! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 31},
                            {"line": 4, "column": 49},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $s > of type < [String]! > used in position expecting type < String! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 45},
                            {"line": 4, "column": 55},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $e > of type < [AnEnum]! > used in position expecting type < AnEnum! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 60},
                            {"line": 4, "column": 61},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $input > of type < [AnInput]! > used in position expecting type < AnInput! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 75},
                            {"line": 4, "column": 72},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $i > of type < [Int]! > used in position expecting type < [Int!] >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 19},
                            {"line": 6, "column": 48},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $f > of type < [Float]! > used in position expecting type < [Float!] >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 31},
                            {"line": 6, "column": 55},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $s > of type < [String]! > used in position expecting type < [String!] >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 45},
                            {"line": 6, "column": 61},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $e > of type < [AnEnum]! > used in position expecting type < [AnEnum!] >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 60},
                            {"line": 6, "column": 67},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $input > of type < [AnInput]! > used in position expecting type < [AnInput!] >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 75},
                            {"line": 6, "column": 78},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $i > of type < [Int]! > used in position expecting type < [Int!]! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 19},
                            {"line": 8, "column": 55},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $f > of type < [Float]! > used in position expecting type < [Float!]! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 31},
                            {"line": 8, "column": 62},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $s > of type < [String]! > used in position expecting type < [String!]! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 45},
                            {"line": 8, "column": 68},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $e > of type < [AnEnum]! > used in position expecting type < [AnEnum!]! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 60},
                            {"line": 8, "column": 74},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $input > of type < [AnInput]! > used in position expecting type < [AnInput!]! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 75},
                            {"line": 8, "column": 85},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
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
                        "message": "Variable < $i > of type < [Int] > used in position expecting type < Int >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 19},
                            {"line": 3, "column": 41},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $f > of type < [Float] > used in position expecting type < Float >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 30},
                            {"line": 3, "column": 48},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $s > of type < [String] > used in position expecting type < String >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 43},
                            {"line": 3, "column": 54},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $e > of type < [AnEnum] > used in position expecting type < AnEnum >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 57},
                            {"line": 3, "column": 60},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $input > of type < [AnInput] > used in position expecting type < AnInput >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 71},
                            {"line": 3, "column": 71},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $i > of type < [Int] > used in position expecting type < Int! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 19},
                            {"line": 4, "column": 42},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $f > of type < [Float] > used in position expecting type < Float! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 30},
                            {"line": 4, "column": 49},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $s > of type < [String] > used in position expecting type < String! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 43},
                            {"line": 4, "column": 55},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $e > of type < [AnEnum] > used in position expecting type < AnEnum! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 57},
                            {"line": 4, "column": 61},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $input > of type < [AnInput] > used in position expecting type < AnInput! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 71},
                            {"line": 4, "column": 72},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $i > of type < [Int] > used in position expecting type < [Int!] >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 19},
                            {"line": 6, "column": 48},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $f > of type < [Float] > used in position expecting type < [Float!] >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 30},
                            {"line": 6, "column": 55},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $s > of type < [String] > used in position expecting type < [String!] >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 43},
                            {"line": 6, "column": 61},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $e > of type < [AnEnum] > used in position expecting type < [AnEnum!] >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 57},
                            {"line": 6, "column": 67},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $input > of type < [AnInput] > used in position expecting type < [AnInput!] >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 71},
                            {"line": 6, "column": 78},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $i > of type < [Int] > used in position expecting type < [Int]! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 19},
                            {"line": 7, "column": 46},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $f > of type < [Float] > used in position expecting type < [Float]! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 30},
                            {"line": 7, "column": 53},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $s > of type < [String] > used in position expecting type < [String]! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 43},
                            {"line": 7, "column": 59},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $e > of type < [AnEnum] > used in position expecting type < [AnEnum]! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 57},
                            {"line": 7, "column": 65},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $input > of type < [AnInput] > used in position expecting type < [AnInput]! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 71},
                            {"line": 7, "column": 76},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $i > of type < [Int] > used in position expecting type < [Int!]! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 19},
                            {"line": 8, "column": 55},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $f > of type < [Float] > used in position expecting type < [Float!]! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 30},
                            {"line": 8, "column": 62},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $s > of type < [String] > used in position expecting type < [String!]! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 43},
                            {"line": 8, "column": 68},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $e > of type < [AnEnum] > used in position expecting type < [AnEnum!]! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 57},
                            {"line": 8, "column": 74},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                    {
                        "message": "Variable < $input > of type < [AnInput] > used in position expecting type < [AnInput!]! >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 71},
                            {"line": 8, "column": 85},
                        ],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.5",
                            "tag": "all-variable-usages-are-allowed",
                            "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                        },
                    },
                ],
            },
        ),
    ],
)
async def test_validators_all_variable_usages_are_allowed(
    schema_stack, query, expected
):
    assert await schema_stack.execute(query) == expected
