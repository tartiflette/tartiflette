import pytest

from tartiflette import Resolver, create_engine
from tartiflette.types.exceptions import GraphQLError


class CustomError(GraphQLError):
    def __init__(self, message, extensions={}) -> None:
        super().__init__(message=message, extensions=extensions)


_SDL = """
type User {
    name: String
}

type Query {
    viewer: User
    admin: User
}
"""


@pytest.fixture(scope="module")
async def ttftt_engine():
    @Resolver("Query.viewer", schema_name="test_pr155")
    async def resolver_query_viewer(*_, **__):
        raise CustomError(
            "this is an error message", extensions={"code": "custom code"}
        )

    @Resolver("Query.admin", schema_name="test_pr155")
    async def resolver_query_admin(*_, **__):
        raise Exception("this is another error message")

    return await create_engine(sdl=_SDL, schema_name="test_pr155")


@pytest.mark.asyncio
async def test_pr155_custom(ttftt_engine):
    query_viewer = """
    query {
        viewer {
            name
        }
    }
    """

    results = await ttftt_engine.execute(query_viewer)
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
async def test_pr155_normal(ttftt_engine):
    query_admin = """
    query {
        admin {
            name
        }
    }
    """

    results = await ttftt_engine.execute(query_admin)
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
