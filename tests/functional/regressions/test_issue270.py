import json

import pytest

from tartiflette import Resolver, create_engine


@pytest.fixture(scope="module")
async def ttftt_engine():
    @Resolver("Mutation.mutateFloat", schema_name="issue270")
    async def resolver_test(pr, args, ctx, info, **kwargs):
        return {"bingo": f"{args['aFloat']}"}

    return await create_engine(
        sdl="""

        type Payload {
            clientMutationId: String,
            bingo: String
        }

        type Mutation {
            mutateFloat(aFloat: Float): Payload
        }

        type Query {
            bob: String
        }
        """,
        schema_name="issue270",
    )


@pytest.mark.parametrize(
    "query, variables, expected",
    [
        (
            "mutation($var: Float!) { mutateFloat(aFloat: $var){ bingo } } ",
            {"var": 5},
            {"data": {"mutateFloat": {"bingo": "5.0"}}},
        ),
        (
            "mutation($var: Float!) { mutateFloat(aFloat: $var){ bingo } } ",
            {"var": 5.0},
            {"data": {"mutateFloat": {"bingo": "5.0"}}},
        ),
        (
            "mutation($var: Float!) { mutateFloat(aFloat: $var){ bingo } } ",
            {"var": 5.1},
            {"data": {"mutateFloat": {"bingo": "5.1"}}},
        ),
        (
            "mutation($var: Float!) { mutateFloat(aFloat: $var){ bingo } } ",
            {"var": True},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $var > got invalid value < True >; Expected type < Float >; Float cannot represent non numeric value: < True >",
                        "path": None,
                        "locations": [{"column": 10, "line": 1}],
                    }
                ],
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_issue270(query, variables, expected, ttftt_engine):
    assert await ttftt_engine.execute(query, variables=variables) == expected
