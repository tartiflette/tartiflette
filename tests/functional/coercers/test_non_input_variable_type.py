import pytest

from tartiflette import Resolver


def bakery(schema_name):
    @Resolver("Query.aField", schema_name=schema_name)
    async def resolver_query_a_field(parent, args, ctx, info):
        return {"field": "value"}


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl="""
    type MyType {
      field: String
    }

    type AnotherType {
      field: String
    }

    union UnionType = MyType | AnotherType

    type Query {
      aField(aParam: String): MyType
    }
    """,
    bakery=bakery,
)
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
            query ($aParam: MyType) { aField(aParam: $aParam) }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < aParam > cannot be non-input type < MyType >.",
                        "path": None,
                        "locations": [{"line": 2, "column": 29}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.2",
                            "tag": "variables-are-input-types",
                            "details": "https://spec.graphql.org/June2018/#sec-Variables-Are-Input-Types",
                        },
                    },
                    {
                        "message": "Field < aField > of type < MyType > must have a selection of subfields. Did you mean < aField { ... } >?",
                        "path": None,
                        "locations": [{"line": 2, "column": 39}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.3.3",
                            "tag": "leaf-field-selections",
                            "details": "https://spec.graphql.org/June2018/#sec-Leaf-Field-Selections",
                        },
                    },
                    {
                        "message": "Variable < $aParam > of type < MyType > used in position expecting type < String >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 20},
                            {"line": 2, "column": 54},
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
            query ($aParam: UnionType) { aField(aParam: $aParam) }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < aParam > cannot be non-input type < UnionType >.",
                        "path": None,
                        "locations": [{"line": 2, "column": 29}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.8.2",
                            "tag": "variables-are-input-types",
                            "details": "https://spec.graphql.org/June2018/#sec-Variables-Are-Input-Types",
                        },
                    },
                    {
                        "message": "Field < aField > of type < MyType > must have a selection of subfields. Did you mean < aField { ... } >?",
                        "path": None,
                        "locations": [{"line": 2, "column": 42}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.3.3",
                            "tag": "leaf-field-selections",
                            "details": "https://spec.graphql.org/June2018/#sec-Leaf-Field-Selections",
                        },
                    },
                    {
                        "message": "Variable < $aParam > of type < UnionType > used in position expecting type < String >.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 20},
                            {"line": 2, "column": 57},
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
async def test_non_input_variable_type(schema_stack, query, expected):
    assert await schema_stack.execute(query) == expected
