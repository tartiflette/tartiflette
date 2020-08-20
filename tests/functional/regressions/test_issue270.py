import pytest

from tartiflette import Resolver


def bakery(schema_name):
    @Resolver("Mutation.mutateFloat", schema_name=schema_name)
    async def resolver_test(pr, args, ctx, info, **kwargs):
        return {"bingo": f"{args['aFloat']}"}


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
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
    bakery=bakery,
)
@pytest.mark.parametrize(
    "query,variables,expected",
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
                        "message": "Variable < $var > got invalid value < True >; Expected type < Float >; Float cannot represent non numeric value: < True >.",
                        "path": None,
                        "locations": [{"line": 1, "column": 10}],
                    }
                ],
            },
        ),
    ],
)
async def test_issue270(schema_stack, query, variables, expected):
    assert await schema_stack.execute(query, variables=variables) == expected
