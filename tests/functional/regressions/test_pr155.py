import pytest

from tartiflette import Resolver, TartifletteError


class CustomError(TartifletteError):
    def __init__(self, message, extensions=None) -> None:
        super().__init__(message=message, extensions=extensions)


SDL = """
type User {
    name: String
}

type Query {
    viewer: User
    admin: User
}
"""


def bakery(schema_name):
    @Resolver("Query.viewer", schema_name=schema_name)
    async def resolver_query_viewer(*_, **__):
        raise CustomError(
            "this is an error message", extensions={"code": "custom code"}
        )

    @Resolver("Query.admin", schema_name=schema_name)
    async def resolver_query_admin(*_, **__):
        raise Exception("this is another error message")


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(sdl=SDL, bakery=bakery)
async def test_pr155_custom(schema_stack):
    assert await schema_stack.execute(
        """
            query {
                viewer {
                    name
                }
            }
            """
    ) == {
        "data": {"viewer": None},
        "errors": [
            {
                "message": "this is an error message",
                "path": ["viewer"],
                "locations": [{"line": 3, "column": 17}],
                "extensions": {"code": "custom code"},
            }
        ],
    }


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(sdl=SDL, bakery=bakery)
async def test_pr155_normal(schema_stack):
    assert await schema_stack.execute(
        """
            query {
                admin {
                    name
                }
            }
            """
    ) == {
        "data": {"admin": None},
        "errors": [
            {
                "message": "this is another error message",
                "path": ["admin"],
                "locations": [{"line": 3, "column": 17}],
            }
        ],
    }
