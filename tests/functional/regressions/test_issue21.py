from collections import namedtuple
from typing import Any, List
from unittest.mock import Mock
import pytest

from tartiflette.executors.types import Info
from tartiflette.resolver import Resolver

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
        a: Obj
    }
    """
        % typee
    )

    results = await ttftt.execute(query, context={}, variables=varis)

    assert results == expected


from tartiflette.types.exceptions.tartiflette import UnknownVariableException


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query, expected, varis",
    [
        (
            """
            query LOL($xid: Int!) {
                a(xid: $xid)
            }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "< xid > is not known",
                        "locations": [],
                        "path": None,
                    },
                    {
                        "message": "< xid > is not known",
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
                a(xid: $xid)
            }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Given value for < xid > is not type < <class 'int'> >",
                        "locations": [],
                        "path": None,
                    },
                ],
            },
            {"xid": "RE"},
        ),
        (
            """
            query LOL($xid: [Int]) {
                a(xid: $xid)
            }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expecting List for < xid > values",
                        "locations": [],
                        "path": None,
                    },
                ],
            },
            {"xid": "RE"},
        ),
        (
            """
            query LOL($xid: [Int]) {
                a(xid: $xid)
            }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Given value for < xid > is not type < <class 'int'> >",
                        "locations": [],
                        "path": None,
                    },
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
        a: Obj
    }
    """
    )

    assert await ttftt.execute(query, context={}, variables=varis) == expected
