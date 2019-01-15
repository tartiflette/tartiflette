import pytest

from tartiflette.engine import Engine
from tartiflette.resolver import Resolver


@Resolver("Query.viewer", schema_name="test_issue79")
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
    schema_name="test_issue79",
)


@pytest.mark.asyncio
async def test_issue79():
    query = """
    fragment UnknownFields on UnknownType {
        name
    }
    
    query {
        viewer {
            ...UnknownFields
        }
    }
    """

    results = await _TTFTT_ENGINE.execute(query)

    assert results == {
        "data": None,
        "errors": [
            {
                "message": "Unknown type < UnknownType >.",
                "path": None,
                "locations": [
                    {"line": 2, "column": 5}
                ]
            },
            {
                "message": "Undefined fragment < UnknownFields >.",
                "path": None,
                "locations": [
                    {"line": 8, "column": 13}
                ]
            }
        ]
    }
