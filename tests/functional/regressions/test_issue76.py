import pytest

from tartiflette import Resolver, create_engine

_SDL = """
type UserStatsViews {
  total: Int
  K: Int
  C: Int
}

type UserStats {
  views: UserStatsViews
}

type User {
  name: String
  stats: UserStats
}

type Query {
  viewer: User
}
"""


@pytest.fixture(scope="module")
async def ttftt_engine():
    @Resolver("Query.viewer", schema_name="test_issue76")
    async def resolver_query_viewer(*_, **__):
        return {
            "viewer": {
                "name": "N1",
                "stats": {"views": {"total": 1, "K": 2, "C": 3}},
            }
        }

    return await create_engine(sdl=_SDL, schema_name="test_issue76")


@pytest.mark.asyncio
async def test_issue76_raw(ttftt_engine):
    query = """
    query {
      viewer {
        name
        stats {
          views {
            total
            unknownField4
          }
          unknownField3
        }
        unknownField2
      }
      unknownField1
    }
    """

    results = await ttftt_engine.execute(query)
    assert results == {
        "data": None,
        "errors": [
            {
                "message": "Field unknownField4 doesn't exist on UserStatsViews",
                "path": ["viewer", "stats", "views", "unknownField4"],
                "locations": [{"line": 8, "column": 13}],
                "extensions": {
                    "rule": "5.3.1",
                    "spec": "June 2018",
                    "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                    "tag": "field-selections-on-objects-interfaces-and-unions-types",
                },
            },
            {
                "message": "Field unknownField3 doesn't exist on UserStats",
                "path": ["viewer", "stats", "unknownField3"],
                "locations": [{"line": 10, "column": 11}],
                "extensions": {
                    "rule": "5.3.1",
                    "spec": "June 2018",
                    "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                    "tag": "field-selections-on-objects-interfaces-and-unions-types",
                },
            },
            {
                "message": "Field unknownField2 doesn't exist on User",
                "path": ["viewer", "unknownField2"],
                "locations": [{"line": 12, "column": 9}],
                "extensions": {
                    "rule": "5.3.1",
                    "spec": "June 2018",
                    "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                    "tag": "field-selections-on-objects-interfaces-and-unions-types",
                },
            },
            {
                "message": "Field unknownField1 doesn't exist on Query",
                "path": ["unknownField1"],
                "locations": [{"line": 14, "column": 7}],
                "extensions": {
                    "rule": "5.3.1",
                    "spec": "June 2018",
                    "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                    "tag": "field-selections-on-objects-interfaces-and-unions-types",
                },
            },
        ],
    }


@pytest.mark.asyncio
async def test_issue76_fragment(ttftt_engine):
    query = """
    fragment UserStatsViewsFields on UserStatsViews {
      total
      unknownField4
    }

    fragment UserStatsFields on UserStats {
      views {
        ...UserStatsViewsFields
      }
      unknownField3
    }

    fragment UserFields on User {
      name
      stats {
        ...UserStatsFields
      }
      unknownField2
    }

    query {
      viewer {
        ...UserFields
      }
      unknownField1
    }
    """

    results = await ttftt_engine.execute(query)
    assert results == {
        "data": None,
        "errors": [
            {
                "message": "Field unknownField4 doesn't exist on UserStatsViews",
                "path": ["unknownField4"],
                "locations": [{"line": 4, "column": 7}],
                "extensions": {
                    "rule": "5.3.1",
                    "spec": "June 2018",
                    "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                    "tag": "field-selections-on-objects-interfaces-and-unions-types",
                },
            },
            {
                "message": "Field unknownField3 doesn't exist on UserStats",
                "path": ["unknownField3"],
                "locations": [{"line": 11, "column": 7}],
                "extensions": {
                    "rule": "5.3.1",
                    "spec": "June 2018",
                    "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                    "tag": "field-selections-on-objects-interfaces-and-unions-types",
                },
            },
            {
                "message": "Field unknownField2 doesn't exist on User",
                "path": ["unknownField2"],
                "locations": [{"line": 19, "column": 7}],
                "extensions": {
                    "rule": "5.3.1",
                    "spec": "June 2018",
                    "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                    "tag": "field-selections-on-objects-interfaces-and-unions-types",
                },
            },
            {
                "message": "Field unknownField1 doesn't exist on Query",
                "path": ["unknownField1"],
                "locations": [{"line": 26, "column": 7}],
                "extensions": {
                    "rule": "5.3.1",
                    "spec": "June 2018",
                    "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                    "tag": "field-selections-on-objects-interfaces-and-unions-types",
                },
            },
        ],
    }


@pytest.mark.asyncio
async def test_issue76_another_order(ttftt_engine):
    query = """
    query {
      viewer {
        name
        stats {
          unknownField3
          views {
            total
            unknownField4
            C
            K
          }
        }
        unknownField2 {
            unknownField5
        }
      }
      unknownField1
    }
    """

    results = await ttftt_engine.execute(query)
    assert results == {
        "data": None,
        "errors": [
            {
                "message": "Field unknownField3 doesn't exist on UserStats",
                "path": ["viewer", "stats", "unknownField3"],
                "locations": [{"line": 6, "column": 11}],
                "extensions": {
                    "rule": "5.3.1",
                    "spec": "June 2018",
                    "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                    "tag": "field-selections-on-objects-interfaces-and-unions-types",
                },
            },
            {
                "message": "Field unknownField4 doesn't exist on UserStatsViews",
                "path": ["viewer", "stats", "views", "unknownField4"],
                "locations": [{"line": 9, "column": 13}],
                "extensions": {
                    "rule": "5.3.1",
                    "spec": "June 2018",
                    "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                    "tag": "field-selections-on-objects-interfaces-and-unions-types",
                },
            },
            {
                "message": "Field unknownField5 doesn't exist on Root",
                "path": ["viewer", "unknownField2", "unknownField5"],
                "locations": [{"line": 15, "column": 13}],
                "extensions": {
                    "rule": "5.3.1",
                    "spec": "June 2018",
                    "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                    "tag": "field-selections-on-objects-interfaces-and-unions-types",
                },
            },
            {
                "message": "Field unknownField2 doesn't exist on User",
                "path": ["viewer", "unknownField2"],
                "locations": [{"line": 14, "column": 9}],
                "extensions": {
                    "rule": "5.3.1",
                    "spec": "June 2018",
                    "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                    "tag": "field-selections-on-objects-interfaces-and-unions-types",
                },
            },
            {
                "message": "Field unknownField1 doesn't exist on Query",
                "path": ["unknownField1"],
                "locations": [{"line": 18, "column": 7}],
                "extensions": {
                    "rule": "5.3.1",
                    "spec": "June 2018",
                    "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                    "tag": "field-selections-on-objects-interfaces-and-unions-types",
                },
            },
        ],
    }
