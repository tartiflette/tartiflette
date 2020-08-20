import pytest

from tartiflette import Resolver, create_schema_with_operationers
from tests.schema_stack import SchemaStack


@pytest.fixture(scope="module")
async def schema_stack():
    @Resolver("Query.viewer", schema_name="test_issue76")
    async def resolver_query_viewer(*_, **__):
        return {
            "viewer": {
                "name": "N1",
                "stats": {"views": {"total": 1, "K": 2, "C": 3}},
            }
        }

    schema, execute, subscribe = await create_schema_with_operationers(
        """
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
        """,
        name="test_issue76",
    )
    return SchemaStack("test_issue76", schema, execute, subscribe)


@pytest.mark.asyncio
async def test_issue76_raw(schema_stack):
    assert (
        await schema_stack.execute(
            """
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
        )
        == {
            "data": None,
            "errors": [
                {
                    "message": "Cannot query field < unknownField4 > on type < UserStatsViews >.",
                    "path": None,
                    "locations": [{"line": 8, "column": 21}],
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
                    "locations": [{"line": 10, "column": 19}],
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
                    "locations": [{"line": 12, "column": 17}],
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
                    "locations": [{"line": 14, "column": 15}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.3.1",
                        "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                    },
                },
            ],
        }
    )


@pytest.mark.asyncio
async def test_issue76_fragment(schema_stack):
    assert (
        await schema_stack.execute(
            """
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
        )
        == {
            "data": None,
            "errors": [
                {
                    "message": "Cannot query field < unknownField4 > on type < UserStatsViews >.",
                    "path": None,
                    "locations": [{"line": 4, "column": 15}],
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
                    "locations": [{"line": 11, "column": 15}],
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
                    "locations": [{"line": 19, "column": 15}],
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
                    "locations": [{"line": 26, "column": 15}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.3.1",
                        "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                    },
                },
            ],
        }
    )


@pytest.mark.asyncio
async def test_issue76_another_order(schema_stack):
    assert (
        await schema_stack.execute(
            """
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
        )
        == {
            "data": None,
            "errors": [
                {
                    "message": "Cannot query field < unknownField3 > on type < UserStats >.",
                    "path": None,
                    "locations": [{"line": 6, "column": 19}],
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
                    "locations": [{"line": 9, "column": 21}],
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
                    "locations": [{"line": 14, "column": 17}],
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
                    "locations": [{"line": 18, "column": 15}],
                    "extensions": {
                        "spec": "June 2018",
                        "rule": "5.3.1",
                        "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                    },
                },
            ],
        }
    )
