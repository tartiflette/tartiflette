import pytest

from tartiflette import Resolver
from tartiflette.engine import Engine

_SDL = """

type bobby {
    c: String
}

type boby {
    b: bobby!
}

type bob {
    a: boby
}

type Query {
    string1: String!
    stringList: [String]
    stringListNonNull: [String]!
    nonNullStringList: [String!]
    nonNullStringListNonNull: [String!]!
    anObject: bob
}

"""


@Resolver("Query.string1", schema_name="test_empty_values")
@Resolver("Query.stringList", schema_name="test_empty_values")
@Resolver("Query.stringListNonNull", schema_name="test_empty_values")
@Resolver("Query.nonNullStringList", schema_name="test_empty_values")
@Resolver("Query.nonNullStringListNonNull", schema_name="test_empty_values")
@Resolver("bobby.c", schema_name="test_empty_values")
@Resolver("boby.b", schema_name="test_empty_values")
async def resolver_x(_pr, _args, _ctx, _info):
    return None


@Resolver("Query.anObject", schema_name="test_empty_values")
@Resolver("bob.a", schema_name="test_empty_values")
async def resolver_y(_pr, _args, _ctx, _info):
    return {}


_ENGINE = Engine(_SDL, schema_name="test_empty_values")


@pytest.mark.asyncio
async def test_empty_values_1():
    assert (
        await _ENGINE.execute(
            """
        query {
            nonNullStringList
            string1
            stringList
            nonNullStringList
            nonNullStringListNonNull
        }
        """
        )
        == {
            "data": None,
            "errors": [
                {
                    "message": "Invalid value (value: None) for field `string1` of type `String!`",
                    "path": ["string1"],
                    "locations": [{"line": 4, "column": 13}],
                },
                {
                    "message": "Invalid value (value: None) for field `nonNullStringListNonNull` of type `[String!]!`",
                    "path": ["nonNullStringListNonNull"],
                    "locations": [{"line": 7, "column": 13}],
                },
            ],
        }
    )


@pytest.mark.asyncio
async def test_empty_values_2():
    assert (
        await _ENGINE.execute(
            """
        query {
            anObject { a {b { c}}}
        }
        """
        )
        == {
            "data": {"anObject": {"a": None}},
            "errors": [
                {
                    "message": "Invalid value (value: None) for field `b` of type `bobby!`",
                    "path": ["anObject", "a", "b"],
                    "locations": [{"line": 3, "column": 27}],
                }
            ],
        }
    )
