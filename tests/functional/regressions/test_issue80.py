import pytest

from tartiflette import Resolver


def bakery(schema_name):
    @Resolver("Query.viewer", schema_name=schema_name)
    async def resolver_query_viewer(*_, **__):
        return {"name": "N1"}


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl="""
    type User {
        name: String
    }

    type Query {
        viewer: User
    }
    """,
    bakery=bakery,
)
async def test_issue80(schema_stack):
    assert await schema_stack.execute(
        """
            fragment UserFields on User {
                name
            }

            query {
                viewer {
                    name
                }
            }
            """
    ) == {
        "data": None,
        "errors": [
            {
                "message": "Fragment < UserFields > is never used.",
                "path": None,
                "locations": [{"line": 2, "column": 13}],
                "extensions": {
                    "spec": "June 2018",
                    "rule": "5.5.1.4",
                    "tag": "fragment-must-be-used",
                    "details": "https://spec.graphql.org/June2018/#sec-Fragments-Must-Be-Used",
                },
            }
        ],
    }
