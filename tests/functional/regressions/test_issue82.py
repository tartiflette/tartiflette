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
async def test_issue82(schema_stack):
    assert await schema_stack.execute(
        """
            query {
                viewer {
                    name
                    ...UndefinedFragment
                }
            }
            """
    ) == {
        "data": None,
        "errors": [
            {
                "message": "Unknown fragment < UndefinedFragment >.",
                "path": None,
                "locations": [{"line": 5, "column": 24}],
                "extensions": {
                    "spec": "June 2018",
                    "rule": "5.5.2.1",
                    "tag": "fragment-spread-target-defined",
                    "details": "https://spec.graphql.org/June2018/#sec-Fragment-spread-target-defined",
                },
            }
        ],
    }
