from typing import Any, Callable, Dict, Optional

import pytest

from tartiflette import Directive, Resolver, create_engine
from tests.functional.utils import is_expected

_SDL = """
directive @testdire(
  if: Boolean! = false
  ifs: [Boolean!]
  conditions: [Boolean!]!
  list: [Boolean]!
) on FIELD

type Cat {
  name: String!
  doesKnowCommand(catCommand: String!): Boolean!
}

type Query {
  cat(
    id: Int!
    name: String
    isSold: Boolean! = false
  ) : Cat
  cats(
    ids: [Int!]!
    names: [String!]
  ) : [Cat]
}
"""


@pytest.fixture(scope="module")
async def ttftt_engine():
    @Directive("testdire", schema_name="test_issue101")
    class Test101Directive:
        @staticmethod
        async def on_field_execution(
            directive_args: Dict[str, Any],
            next_resolver: Callable,
            parent: Optional[Any],
            args: Dict[str, Any],
            ctx: Optional[Any],
            info: "ResolveInfo",
        ) -> Any:
            return await next_resolver(parent, args, ctx, info)

    @Resolver("Query.cat", schema_name="test_issue101")
    async def resolve_query_cat(parent, args, ctx, info):
        return {"name": "Cat"}

    @Resolver("Query.cats", schema_name="test_issue101")
    async def resolve_query_cats(parent, args, ctx, info):
        return [{"name": "Cat"}]

    @Resolver("Cat.doesKnowCommand", schema_name="test_issue101")
    async def resolve_cat_does_know_command(parent, args, ctx, info):
        return True

    return await create_engine(_SDL, schema_name="test_issue101")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query,expected",
    [
        # Missing required argument on root field
        (
            """
            query {
              cat {
                name
              }
              cats {
                name
              }
            }
            """,
            {
                "data": {"cat": None, "cats": None},
                "errors": [
                    {
                        "message": "Argument < ids > of required type < [Int!]! > was not provided.",
                        "path": ["cats"],
                        "locations": [{"line": 6, "column": 15}],
                    },
                    {
                        "message": "Argument < id > of required type < Int! > was not provided.",
                        "path": ["cat"],
                        "locations": [{"line": 3, "column": 15}],
                    },
                ],
            },
        ),
        (
            """
            query {
              ... on Query {
                cat {
                  name
                }
                cats {
                  name
                }
              }
            }
            """,
            {
                "data": {"cat": None, "cats": None},
                "errors": [
                    {
                        "message": "Argument < id > of required type < Int! > was not provided.",
                        "path": ["cat"],
                        "locations": [{"line": 4, "column": 17}],
                    },
                    {
                        "message": "Argument < ids > of required type < [Int!]! > was not provided.",
                        "path": ["cats"],
                        "locations": [{"line": 7, "column": 17}],
                    },
                ],
            },
        ),
        (
            """
            fragment QueryFields on Query {
              cat {
                name
              }
              cats {
                name
              }
            }
            query {
              ...QueryFields
            }
            """,
            {
                "data": {"cat": None, "cats": None},
                "errors": [
                    {
                        "message": "Argument < ids > of required type < [Int!]! > was not provided.",
                        "path": ["cats"],
                        "locations": [{"line": 6, "column": 15}],
                    },
                    {
                        "message": "Argument < id > of required type < Int! > was not provided.",
                        "path": ["cat"],
                        "locations": [{"line": 3, "column": 15}],
                    },
                ],
            },
        ),
        (
            """
            fragment QueryFields on Query {
              ... on Query {
                cat {
                  name
                }
                cats {
                  name
                }
              }
            }
            query {
              ...QueryFields
            }
            """,
            {
                "data": {"cat": None, "cats": None},
                "errors": [
                    {
                        "message": "Argument < ids > of required type < [Int!]! > was not provided.",
                        "path": ["cats"],
                        "locations": [{"line": 7, "column": 17}],
                    },
                    {
                        "message": "Argument < id > of required type < Int! > was not provided.",
                        "path": ["cat"],
                        "locations": [{"line": 4, "column": 17}],
                    },
                ],
            },
        ),
        # Missing required argument on nested field
        (
            """
            query {
              cat(id: 1) {
                doesKnowCommand
              }
            }
            """,
            {
                "data": {"cat": None},
                "errors": [
                    {
                        "message": "Argument < catCommand > of required type < String! > was not provided.",
                        "path": ["cat", "doesKnowCommand"],
                        "locations": [{"line": 4, "column": 17}],
                    }
                ],
            },
        ),
        (
            """
            query {
              ... on Query {
                cat(id: 1) {
                  doesKnowCommand
                }
              }
            }
            """,
            {
                "data": {"cat": None},
                "errors": [
                    {
                        "message": "Argument < catCommand > of required type < String! > was not provided.",
                        "path": ["cat", "doesKnowCommand"],
                        "locations": [{"line": 5, "column": 19}],
                    }
                ],
            },
        ),
        (
            """
            fragment QueryFields on Query {
              cat(id: 1) {
                doesKnowCommand
              }
            }
            query {
              ...QueryFields
            }
            """,
            {
                "data": {"cat": None},
                "errors": [
                    {
                        "message": "Argument < catCommand > of required type < String! > was not provided.",
                        "path": ["cat", "doesKnowCommand"],
                        "locations": [{"line": 4, "column": 17}],
                    }
                ],
            },
        ),
        (
            """
            fragment QueryFields on Query {
              ... on Query {
                cat(id: 1) {
                  doesKnowCommand
                }
              }
            }
            query {
              ...QueryFields
            }
            """,
            {
                "data": {"cat": None},
                "errors": [
                    {
                        "message": "Argument < catCommand > of required type < String! > was not provided.",
                        "path": ["cat", "doesKnowCommand"],
                        "locations": [{"line": 5, "column": 19}],
                    }
                ],
            },
        ),
        (
            """
            fragment CatFields on Cat {
              ... on Cat {
                doesKnowCommand
              }
            }

            fragment QueryFields on Query {
              ... on Query {
                cat(id: 1) {
                  ...CatFields
                }
              }
            }

            query {
              ...QueryFields
            }
            """,
            {
                "data": {"cat": None},
                "errors": [
                    {
                        "message": "Argument < catCommand > of required type < String! > was not provided.",
                        "path": ["cat", "doesKnowCommand"],
                        "locations": [{"line": 4, "column": 17}],
                    }
                ],
            },
        ),
        # Missing required argument on root directive
        (
            """
            query {
              cat(id: 1) @testdire {
                name
              }
            }
            """,
            {
                "data": {"cat": None},
                "errors": [
                    {
                        "message": "Argument < conditions > of required type < [Boolean!]! > was not provided.",
                        "path": ["cat"],
                        "locations": [{"line": 3, "column": 26}],
                    },
                    {
                        "message": "Argument < list > of required type < [Boolean]! > was not provided.",
                        "path": ["cat"],
                        "locations": [{"line": 3, "column": 26}],
                    },
                ],
            },
        ),
        (
            """
            query {
              ... on Query {
                cat(id: 1) @testdire {
                  name
                }
              }
            }
            """,
            {
                "data": {"cat": None},
                "errors": [
                    {
                        "message": "Argument < conditions > of required type < [Boolean!]! > was not provided.",
                        "path": ["cat"],
                        "locations": [{"line": 4, "column": 28}],
                    },
                    {
                        "message": "Argument < list > of required type < [Boolean]! > was not provided.",
                        "path": ["cat"],
                        "locations": [{"line": 4, "column": 28}],
                    },
                ],
            },
        ),
        (
            """
            fragment QueryFields on Query {
              cat(id: 1) @testdire {
                name
              }
            }
            query {
              ...QueryFields
            }
            """,
            {
                "data": {"cat": None},
                "errors": [
                    {
                        "message": "Argument < conditions > of required type < [Boolean!]! > was not provided.",
                        "path": ["cat"],
                        "locations": [{"line": 3, "column": 26}],
                    },
                    {
                        "message": "Argument < list > of required type < [Boolean]! > was not provided.",
                        "path": ["cat"],
                        "locations": [{"line": 3, "column": 26}],
                    },
                ],
            },
        ),
        (
            """
            fragment QueryFields on Query {
              ... on Query {
                cat(id: 1) @testdire {
                  name
                }
              }
            }
            query {
              ...QueryFields
            }
            """,
            {
                "data": {"cat": None},
                "errors": [
                    {
                        "message": "Argument < conditions > of required type < [Boolean!]! > was not provided.",
                        "path": ["cat"],
                        "locations": [{"line": 4, "column": 28}],
                    },
                    {
                        "message": "Argument < list > of required type < [Boolean]! > was not provided.",
                        "path": ["cat"],
                        "locations": [{"line": 4, "column": 28}],
                    },
                ],
            },
        ),
        # Missing required argument on nested directive
        (
            """
            query {
              cat(id: 1) {
                doesKnowCommand(catCommand: "JUMP") @testdire
              }
            }
            """,
            {
                "data": {"cat": None},
                "errors": [
                    {
                        "message": "Argument < conditions > of required type < [Boolean!]! > was not provided.",
                        "path": ["cat", "doesKnowCommand"],
                        "locations": [{"line": 4, "column": 53}],
                    },
                    {
                        "message": "Argument < list > of required type < [Boolean]! > was not provided.",
                        "path": ["cat", "doesKnowCommand"],
                        "locations": [{"line": 4, "column": 53}],
                    },
                ],
            },
        ),
        (
            """
            query {
              ... on Query {
                cat(id: 1) {
                  doesKnowCommand(catCommand: "JUMP") @testdire
                }
              }
            }
            """,
            {
                "data": {"cat": None},
                "errors": [
                    {
                        "message": "Argument < conditions > of required type < [Boolean!]! > was not provided.",
                        "path": ["cat", "doesKnowCommand"],
                        "locations": [{"line": 5, "column": 55}],
                    },
                    {
                        "message": "Argument < list > of required type < [Boolean]! > was not provided.",
                        "path": ["cat", "doesKnowCommand"],
                        "locations": [{"line": 5, "column": 55}],
                    },
                ],
            },
        ),
        (
            """
            fragment QueryFields on Query {
              cat(id: 1) {
                doesKnowCommand(catCommand: "JUMP") @testdire
              }
            }
            query {
              ...QueryFields
            }
            """,
            {
                "data": {"cat": None},
                "errors": [
                    {
                        "message": "Argument < conditions > of required type < [Boolean!]! > was not provided.",
                        "path": ["cat", "doesKnowCommand"],
                        "locations": [{"line": 4, "column": 53}],
                    },
                    {
                        "message": "Argument < list > of required type < [Boolean]! > was not provided.",
                        "path": ["cat", "doesKnowCommand"],
                        "locations": [{"line": 4, "column": 53}],
                    },
                ],
            },
        ),
        (
            """
            fragment QueryFields on Query {
              ... on Query {
                cat(id: 1) {
                  doesKnowCommand(catCommand: "JUMP") @testdire
                }
              }
            }
            query {
              ...QueryFields
            }
            """,
            {
                "data": {"cat": None},
                "errors": [
                    {
                        "message": "Argument < conditions > of required type < [Boolean!]! > was not provided.",
                        "path": ["cat", "doesKnowCommand"],
                        "locations": [{"line": 5, "column": 55}],
                    },
                    {
                        "message": "Argument < list > of required type < [Boolean]! > was not provided.",
                        "path": ["cat", "doesKnowCommand"],
                        "locations": [{"line": 5, "column": 55}],
                    },
                ],
            },
        ),
        (
            """
            fragment CatFields on Cat {
              ... on Cat {
                doesKnowCommand(catCommand: "JUMP") @testdire
              }
            }

            fragment QueryFields on Query {
              ... on Query {
                cat(id: 1) {
                  ...CatFields
                }
              }
            }

            query {
              ...QueryFields
            }
            """,
            {
                "data": {"cat": None},
                "errors": [
                    {
                        "message": "Argument < conditions > of required type < [Boolean!]! > was not provided.",
                        "path": ["cat", "doesKnowCommand"],
                        "locations": [{"line": 4, "column": 53}],
                    },
                    {
                        "message": "Argument < list > of required type < [Boolean]! > was not provided.",
                        "path": ["cat", "doesKnowCommand"],
                        "locations": [{"line": 4, "column": 53}],
                    },
                ],
            },
        ),
        # Missing both field & directive arguments
        (
            """
            fragment CatFields on Cat {
              ... on Cat {
                doesKnowCommand
              }
            }

            fragment QueryFields on Query {
              ... on Query {
                cat(id: 1) @testdire {
                  ...CatFields
                }
              }
            }

            query {
              ...QueryFields
            }
            """,
            {
                "data": {"cat": None},
                "errors": [
                    {
                        "message": "Argument < conditions > of required type < [Boolean!]! > was not provided.",
                        "path": ["cat"],
                        "locations": [{"line": 10, "column": 28}],
                    },
                    {
                        "message": "Argument < list > of required type < [Boolean]! > was not provided.",
                        "path": ["cat"],
                        "locations": [{"line": 10, "column": 28}],
                    },
                ],
            },
        ),
    ],
)
async def test_issue101(ttftt_engine, query, expected):
    is_expected(await ttftt_engine.execute(query), expected)
