from collections import namedtuple

import pytest

from tartiflette import Resolver, create_schema_with_operators

GQLTypeMock = namedtuple("GQLTypeMock", ["name", "coerce_value"])


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query,expected,output_type,variables",
    [
        (
            """
            query LOL($xid: Int) {
                a(xid: $xid) { iam args { xid }}
            }
            """,
            {"data": {"a": {"iam": "a", "args": {"xid": 45}}}},
            "Int",
            {"xid": 45},
        ),
        (
            """
            query LOL {
                a(xid: "RE") { iam args { xid }}
            }
            """,
            {"data": {"a": {"iam": "a", "args": {"xid": "RE"}}}},
            "String",
            {},
        ),
        (
            """
            query LOL($xid: Int = 56) {
                a(xid: $xid) { iam args { xid }}
            }
            """,
            {"data": {"a": {"iam": "a", "args": {"xid": 56}}}},
            "Int",
            {},
        ),
        (
            """
            query LOL($xid: [Int]) {
                a(xid: $xid) { iam args { xid }}
            }
            """,
            {"data": {"a": {"iam": "a", "args": {"xid": [1, 6]}}}},
            "[Int]",
            {"xid": [1, 6]},
        ),
        (
            """
            query LOL($xid: Int) {
                a(xid: $xid) { iam args { xid }}
            }
            """,
            {"data": {"a": {"iam": "a", "args": {"xid": None}}}},
            "Int",
            {},
        ),
    ],
)
async def test_issue21_okayquery(
    query, expected, output_type, variables, random_schema_name
):
    @Resolver("Query.a", schema_name=random_schema_name)
    async def a_resolver(_, arguments, __, info: "ResolveInfo"):
        return {"iam": info.field_name, "args": arguments}

    _, execute, __ = await create_schema_with_operators(
        """
        type Args {
            xid: %s
        }

        type Obj {
            iam: String
            args: Args
        }

        type Query {
            a(xid: %s): Obj
        }
        """
        % (output_type, output_type),
        name=random_schema_name,
    )

    assert (
        await execute(
            query, context={}, variables=variables, operation_name="LOL"
        )
        == expected
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query,expected,variables",
    [
        (
            """
            query LOL($xid: Int!) {
                a(xid: $xid) { iam }
            }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $xid > of required type < Int! > was not provided.",
                        "path": None,
                        "locations": [{"line": 2, "column": 23}],
                    }
                ],
            },
            {},
        ),
        (
            """
            query LOL($xid: Int) {
                a(xid: $xid) { iam }
            }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $xid > got invalid value < RE >; Expected type < Int >; Int cannot represent non-integer value: < RE >.",
                        "path": None,
                        "locations": [{"line": 2, "column": 23}],
                    }
                ],
            },
            {"xid": "RE"},
        ),
        (
            """
            query LOL($xid: Int) {
                a(xid: $xid) { iam }
            }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $xid > got invalid value < RE >; Expected type < Int >; Int cannot represent non-integer value: < RE >.",
                        "path": None,
                        "locations": [{"line": 2, "column": 23}],
                    }
                ],
            },
            {"xid": "RE"},
        ),
        (
            """
            query LOL($xid: Int) {
                a(xid: $xid) { iam }
            }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $xid > got invalid value < ['RE'] >; Expected type < Int >; Int cannot represent non-integer value: < ['RE'] >.",
                        "path": None,
                        "locations": [{"line": 2, "column": 23}],
                    }
                ],
            },
            {"xid": ["RE"]},
        ),
    ],
)
async def test_issue21_exceptquery(
    query, expected, variables, random_schema_name
):
    @Resolver("Query.a", schema_name=random_schema_name)
    async def a_resolver(_, arguments, __, info: "ResolveInfo"):
        return {"iam": info.field_name, "args": arguments}

    _, execute, __ = await create_schema_with_operators(
        """
        type Args{
            xid: Int
        }

        type Obj {
            iam: String
            args: Args
        }

        type Query {
            a(xid: Int): Obj
        }
        """,
        name=random_schema_name,
    )

    assert await execute(query, context={}, variables=variables) == expected
