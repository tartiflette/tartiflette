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
    from tartiflette import create_engine

    @Resolver("Query.a")
    async def a_resolver(_, arguments, __, info: Info):
        return {"iam": info.query_field.name, "args": arguments}

    ttftt = await create_engine(
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
                        "message": "Variable < xid > is not known",
                        "locations": [],
                        "path": None,
                    },
                    {
                        "message": "Variable < xid > is not known",
                        "locations": [],
                        "path": None,
                    },
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
                        "message": "Given value for < xid > is not type < <class 'int'> >",
                        "locations": [{"column": 23, "line": 2}],
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
                        "message": "Expecting List for < xid > values",
                        "locations": [{"column": 23, "line": 2}],
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
                        "message": "Given value for < xid > is not type < <class 'int'> >",
                        "locations": [{"column": 23, "line": 2}],
                        "path": None,
                    }
                ],
            },
            {"xid": ["RE"]},
        ),
    ],
)
async def test_issue21_exceptquery(query, expected, varis, clean_registry):
    from tartiflette import create_engine

    @Resolver("Query.a")
    async def a_resolver(_, arguments, __, info: Info):
        return {"iam": info.query_field.name, "args": arguments}

    ttftt = await create_engine(
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
