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
async def test_issue79(schema_stack):
    assert (
        await schema_stack.execute(
            """
            fragment UnknownFields on UnknownType {
                name
            }

            query {
                viewer {
                    ...UnknownFields
                }
            }
            """
        )
        == {
            "data": None,
            "errors": [
                {
                    "message": "Unknown type < UnknownType >.",
                    "path": None,
                    "locations": [{"line": 2, "column": 39}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.5.1.2",
                        "tag": "fragment-spread-type-existence",
                        "details": "https://spec.graphql.org/June2018/#sec-Fragment-Spread-Type-Existence",
                    },
                }
            ],
        }
    )
