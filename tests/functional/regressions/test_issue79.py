import pytest

from tartiflette import Resolver, create_engine


@Resolver("Query.viewer", schema_name="test_issue79")
async def resolver_query_viewer(*_, **__):
    return {"name": "N1"}


_SDL = """
type User {
    name: String
}

type Query {
    viewer: User
}
"""


@pytest.fixture(scope="module")
async def ttftt_engine():
    return await create_engine(sdl=_SDL, schema_name="test_issue79")


@pytest.mark.asyncio
async def test_issue79(ttftt_engine):
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

    results = await ttftt_engine.execute(query)

    assert results == {
        "data": None,
        "errors": [
            {
                "message": "Field name doesn't exist on UnknownType",
                "path": ["name"],
                "locations": [{"line": 3, "column": 9}],
                "extensions": {
                    "rule": "5.3.1",
                    "spec": "June 2018",
                    "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                    "tag": "field-selections-on-objects-interfaces-and-unions-types",
                },
            },
            {
                "message": "Unknown type UnknownType.",
                "path": None,
                "locations": [{"line": 2, "column": 5}],
                "extensions": {
                    "rule": "5.5.1.2",
                    "spec": "June 2018",
                    "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Fragment-Spread-Type-Existence",
                    "tag": "fragment-spread-type-existence",
                },
            },
        ],
    }
