import pytest

from tartiflette.engine import Engine
from tartiflette.resolver import Resolver


@Resolver("Query.viewer", schema_name="test_issue82")
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
    schema_name="test_issue82",
)


@pytest.mark.asyncio
async def test_issue82():
    query = """
    query {
        viewer {
            name
            ...UndefinedFragment
        }
    }
    """

    results = await _TTFTT_ENGINE.execute(query)

    assert results == {
        "data": None,
        "errors": [
            {
                "message": "Undefined fragment < UndefinedFragment >.",
                "path": None,
                "locations": [{"line": 5, "column": 13}],
            }
        ],
    }
