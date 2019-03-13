import pytest

from tartiflette.engine import Engine
from tartiflette.resolver import Resolver
from tartiflette.types.exceptions import GraphQLError


class CustomError(GraphQLError):
    def __init__(self, message, extensions={}) -> None:
        super().__init__(message=message, extensions=extensions)


@Resolver("Query.viewer", schema_name="test_pr155")
async def resolver_query_viewer(*_, **__):
    raise CustomError(
        "this is an error message", extensions={"code": "custom code"}
    )


@Resolver("Query.admin", schema_name="test_pr155")
async def resolver_query_admin(*_, **__):
    raise Exception("this is another error message")


_TTFTT_ENGINE = Engine(
    """
    type User {
        name: String
    }

    type Query {
        viewer: User
        admin: User
    }
    """,
    schema_name="test_pr155",
)


@pytest.mark.asyncio
async def test_pr155_custom():
    query_viewer = """
    query {
        viewer {
            name
        }
    }
    """

    results = await _TTFTT_ENGINE.execute(query_viewer)
    assert results == {
        "data": {"viewer": None},
        "errors": [
            {
                "message": "this is an error message",
                "path": ["viewer"],
                "locations": [{"line": 3, "column": 9}],
                "extensions": {"code": "custom code"},
            }
        ],
    }


@pytest.mark.asyncio
async def test_pr155_normal():
    query_admin = """
    query {
        admin {
            name
        }
    }
    """

    results = await _TTFTT_ENGINE.execute(query_admin)
    assert results == {
        "data": {"admin": None},
        "errors": [
            {
                "message": "this is another error message",
                "path": ["admin"],
                "locations": [{"line": 3, "column": 9}],
            }
        ],
    }
