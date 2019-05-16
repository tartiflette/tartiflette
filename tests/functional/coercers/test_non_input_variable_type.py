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


# TODO: unskip this test once `validate_document` function has been implemented
@pytest.mark.skip(
    reason="Will handled by the `validate_document` function which isn't implemented yet."
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
                        "message": "Variable < $aParam > expected value of "
                        "type < MyType > which cannot be used as "
                        "an input type.",
                        "path": None,
                        "locations": [{"column": 29, "line": 2}],
                    }
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
                        "message": "Variable < $aParam > expected value of "
                        "type < UnionType > which cannot be used "
                        "as an input type.",
                        "path": None,
                        "locations": [{"column": 29, "line": 2}],
                    }
                ],
            },
        ),
    ],
)
async def test_non_input_variable_type(ttftt_engine, query, expected):
    assert await ttftt_engine.execute(query) == expected
