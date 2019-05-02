from collections import namedtuple

import pytest

from tartiflette import Resolver
from tartiflette.executors.types import Info

GQLTypeMock = namedtuple("GQLTypeMock", ["name", "coerce_value"])


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query, expected, typee, varis",
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
    query, expected, typee, varis, clean_registry
):
    from tartiflette.engine import Engine

    @Resolver("Query.a")
    async def a_resolver(_, arguments, __, info: Info):
        return {"iam": info.query_field.name, "args": arguments}

    ttftt = Engine(
        """
    type Args{
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
        % (typee, typee)
    )

    results = await ttftt.execute(
        query, context={}, variables=varis, operation_name="LOL"
    )

    assert results == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query, expected, varis",
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
                        "locations": [{"column": 23, "line": 2}],
                        "message": "Variable < $xid > of required type < Int! > was not provided.",
                        "path": None,
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
                        "locations": [{"column": 23, "line": 2}],
                        "message": "Variable < $xid > got invalid value < RE >; Expected type < Int >; Int cannot represent non-integer value: < RE >",
                        "path": None,
                    }
                ],
            },
            {"xid": "RE"},
        ),
        (
            """
            query LOL($xid: [Int]) {
                a(xid: $xid) { iam }
            }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "locations": [{"column": 23, "line": 2}],
                        "message": "Variable < $xid > got invalid value < RE "
                        ">; Expected type < Int > at value[0]; "
                        "Int cannot represent non-integer value: "
                        "< R >",
                        "path": None,
                    },
                    {
                        "locations": [{"column": 23, "line": 2}],
                        "message": "Variable < $xid > got invalid value < RE "
                        ">; Expected type < Int > at value[1]; "
                        "Int cannot represent non-integer value: "
                        "< E >",
                        "path": None,
                    },
                ],
            },
            {"xid": "RE"},
        ),
        (
            """
            query LOL($xid: [Int]) {
                a(xid: $xid) { iam }
            }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "locations": [{"column": 23, "line": 2}],
                        "message": "Variable < $xid > got invalid value < ['RE'] >; Expected type < Int > at value[0]; Int cannot represent non-integer value: < RE >",
                        "path": None,
                    }
                ],
            },
            {"xid": ["RE"]},
        ),
    ],
)
async def test_issue21_exceptquery(query, expected, varis, clean_registry):
    from tartiflette.engine import Engine

    @Resolver("Query.a")
    async def a_resolver(_, arguments, __, info: Info):
        return {"iam": info.query_field.name, "args": arguments}

    ttftt = Engine(
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
    """
    )

    assert await ttftt.execute(query, context={}, variables=varis) == expected
