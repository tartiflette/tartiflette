import pytest

from tartiflette import Resolver, create_engine

_SDL = """
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
"""


@pytest.fixture(scope="module")
async def ttftt_engine():
    @Resolver("Query.aField", schema_name="test_non_input_variable_type")
    async def resolver_query_a_field(parent, args, ctx, info):
        return {"field": "value"}

    return await create_engine(
        sdl=_SDL, schema_name="test_non_input_variable_type"
    )


@pytest.mark.asyncio
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
                        "message": "Variable aParam cannot be non-input type MyType.",
                        "path": None,
                        "locations": [{"line": 2, "column": 20}],
                        "extensions": {
                            "rule": "5.8.2",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Variables-Are-Input-Types",
                            "tag": "variables-are-input-types",
                        },
                    },
                    {
                        "message": "Field aField of type MyType must have a selection of subfields.",
                        "path": ["aField"],
                        "locations": [{"line": 2, "column": 39}],
                        "extensions": {
                            "rule": "5.3.3",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Leaf-Field-Selections",
                            "tag": "leaf-field-selections",
                        },
                    },
                    {
                        "message": "Can't use < $aParam / MyType > for type < String >.",
                        "path": ["aField"],
                        "locations": [
                            {"line": 2, "column": 20},
                            {"line": 2, "column": 54},
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
            query ($aParam: UnionType) { aField(aParam: $aParam) }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable aParam cannot be non-input type UnionType.",
                        "path": None,
                        "locations": [{"line": 2, "column": 20}],
                        "extensions": {
                            "rule": "5.8.2",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Variables-Are-Input-Types",
                            "tag": "variables-are-input-types",
                        },
                    },
                    {
                        "message": "Field aField of type MyType must have a selection of subfields.",
                        "path": ["aField"],
                        "locations": [{"line": 2, "column": 42}],
                        "extensions": {
                            "rule": "5.3.3",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Leaf-Field-Selections",
                            "tag": "leaf-field-selections",
                        },
                    },
                    {
                        "message": "Can't use < $aParam / UnionType > for type < String >.",
                        "path": ["aField"],
                        "locations": [
                            {"line": 2, "column": 20},
                            {"line": 2, "column": 57},
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
async def test_non_input_variable_type(ttftt_engine, query, expected):
    assert await ttftt_engine.execute(query) == expected
