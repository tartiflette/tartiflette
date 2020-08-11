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
                "message": "Cannot query field < unknownField4 > on type < UserStatsViews >.",
                "path": None,
                "locations": [{"line": 8, "column": 13}],
                "extensions": {
                    "spec": "June 2018",
                    "rule": "5.3.1",
                    "tag": "field-selections-on-objects-interfaces-and-unions-types",
                    "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                },
            },
            {
                "message": "Cannot query field < unknownField3 > on type < UserStats >.",
                "path": None,
                "locations": [{"line": 10, "column": 11}],
                "extensions": {
                    "spec": "June 2018",
                    "rule": "5.3.1",
                    "tag": "field-selections-on-objects-interfaces-and-unions-types",
                    "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                },
            },
            {
                "message": "Cannot query field < unknownField2 > on type < User >.",
                "path": None,
                "locations": [{"line": 12, "column": 9}],
                "extensions": {
                    "spec": "June 2018",
                    "rule": "5.3.1",
                    "tag": "field-selections-on-objects-interfaces-and-unions-types",
                    "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                },
            },
            {
                "message": "Cannot query field < unknownField1 > on type < Query >.",
                "path": None,
                "locations": [{"line": 14, "column": 7}],
                "extensions": {
                    "spec": "June 2018",
                    "rule": "5.3.1",
                    "tag": "field-selections-on-objects-interfaces-and-unions-types",
                    "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
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
                "message": "Cannot query field < unknownField4 > on type < UserStatsViews >.",
                "path": None,
                "locations": [{"line": 4, "column": 7}],
                "extensions": {
                    "spec": "June 2018",
                    "rule": "5.3.1",
                    "tag": "field-selections-on-objects-interfaces-and-unions-types",
                    "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                },
            },
            {
                "message": "Cannot query field < unknownField3 > on type < UserStats >.",
                "path": None,
                "locations": [{"line": 11, "column": 7}],
                "extensions": {
                    "spec": "June 2018",
                    "rule": "5.3.1",
                    "tag": "field-selections-on-objects-interfaces-and-unions-types",
                    "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                },
            },
            {
                "message": "Cannot query field < unknownField2 > on type < User >.",
                "path": None,
                "locations": [{"line": 19, "column": 7}],
                "extensions": {
                    "spec": "June 2018",
                    "rule": "5.3.1",
                    "tag": "field-selections-on-objects-interfaces-and-unions-types",
                    "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                },
            },
            {
                "message": "Cannot query field < unknownField1 > on type < Query >.",
                "path": None,
                "locations": [{"line": 26, "column": 7}],
                "extensions": {
                    "spec": "June 2018",
                    "rule": "5.3.1",
                    "tag": "field-selections-on-objects-interfaces-and-unions-types",
                    "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
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
                "message": "Cannot query field < unknownField3 > on type < UserStats >.",
                "path": None,
                "locations": [{"line": 6, "column": 11}],
                "extensions": {
                    "spec": "June 2018",
                    "rule": "5.3.1",
                    "tag": "field-selections-on-objects-interfaces-and-unions-types",
                    "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                },
            },
            {
                "message": "Cannot query field < unknownField4 > on type < UserStatsViews >.",
                "path": None,
                "locations": [{"line": 9, "column": 13}],
                "extensions": {
                    "spec": "June 2018",
                    "rule": "5.3.1",
                    "tag": "field-selections-on-objects-interfaces-and-unions-types",
                    "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                },
            },
            {
                "message": "Cannot query field < unknownField2 > on type < User >.",
                "path": None,
                "locations": [{"line": 14, "column": 9}],
                "extensions": {
                    "spec": "June 2018",
                    "rule": "5.3.1",
                    "tag": "field-selections-on-objects-interfaces-and-unions-types",
                    "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                },
            },
            {
                "message": "Cannot query field < unknownField1 > on type < Query >.",
                "path": None,
                "locations": [{"line": 18, "column": 7}],
                "extensions": {
                    "spec": "June 2018",
                    "rule": "5.3.1",
                    "tag": "field-selections-on-objects-interfaces-and-unions-types",
                    "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                },
            },
        ],
    }
