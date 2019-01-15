import pytest

from tartiflette.engine import Engine
from tartiflette.resolver import Resolver


@Resolver("Query.viewer", schema_name="test_issue80")
async def resolver_query_viewer(*_, **__):
    return {"name": "N1"}


_TTFTT_ENGINE = Engine(
    """
    type User {
        name: String
    }
    
    type Query {
        viewer: User
    }
    """,
    schema_name="test_issue80",
)


@pytest.mark.asyncio
async def test_issue80():
    query = """
    fragment UserFields on User {
        name
    }
    
    query {
        viewer {
            name
        }
    }
    """

    results = await _TTFTT_ENGINE.execute(query)

    assert results == {
        "data": None,
        "errors": [
            {
                "message": "Fragment < UserFields > is never used.",
                "path": None,
                "locations": [{"line": 2, "column": 5}],
            }
        ],
    }
