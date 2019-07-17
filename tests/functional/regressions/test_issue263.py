import pytest

from tartiflette import Resolver, create_engine


@pytest.fixture(scope="module")
async def ttftt_engine():
    @Resolver("Query.aField", schema_name="issue263")
    async def abc(*args, **kwargs):
        return "Yeah"

    return await create_engine(
        sdl="""
type Query {
    aField(ids: [String]): String
}""",
        schema_name="issue263",
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query, varis, expected",
    [
        (
            "query ($ids: [String!]) { aField(ids: $ids) }",
            {},
            {"data": {"aField": "Yeah"}},
        ),
        (
            "query ($ids: [String!]) { aField(ids: $ids) }",
            {"ids": None},
            {"data": {"aField": "Yeah"}},
        ),
        (
            "query ($ids: [String!]) { aField(ids: $ids) }",
            {"ids": ["a", None, "b"]},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Value can't be null or contain a null value",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                    {
                        "message": "Given value for < ids > is not type < <class 'str'> >",
                        "path": None,
                        "locations": [{"line": 1, "column": 8}],
                    },
                ],
            },
        ),
    ],
)
async def test_issue245(ttftt_engine, query, varis, expected):
    assert await ttftt_engine.execute(query, variables=varis) == expected
