import pytest

from tartiflette import Engine
from tartiflette.directive import CommonDirective, Directive


@Directive("include", schema_name="test_issue101")
class IncludeDirective(CommonDirective):
    pass


_SDL = """
directive @include(
  if: Boolean! = false
  ifs: [Boolean!]
  conditions: [Boolean!]!
  list: [Boolean]!
) on FIELD_DEFINITION

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


_TTFTT_ENGINE = Engine(_SDL, schema_name="test_issue101")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query,errors",
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
            [
                {
                    "message": "Missing required < id > argument on < cat > field.",
                    "path": None,
                    "locations": [{"line": 3, "column": 15}],
                },
                {
                    "message": "Missing required < ids > argument on < cats > field.",
                    "path": None,
                    "locations": [{"line": 6, "column": 15}],
                },
            ],
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
            [
                {
                    "message": "Missing required < id > argument on < cat > field.",
                    "path": None,
                    "locations": [{"line": 4, "column": 17}],
                },
                {
                    "message": "Missing required < ids > argument on < cats > field.",
                    "path": None,
                    "locations": [{"line": 7, "column": 17}],
                },
            ],
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
            [
                {
                    "message": "Missing required < id > argument on < cat > field.",
                    "path": None,
                    "locations": [{"line": 3, "column": 15}],
                },
                {
                    "message": "Missing required < ids > argument on < cats > field.",
                    "path": None,
                    "locations": [{"line": 6, "column": 15}],
                },
            ],
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
            [
                {
                    "message": "Missing required < id > argument on < cat > field.",
                    "path": None,
                    "locations": [{"line": 4, "column": 17}],
                },
                {
                    "message": "Missing required < ids > argument on < cats > field.",
                    "path": None,
                    "locations": [{"line": 7, "column": 17}],
                },
            ],
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
            [
                {
                    "message": "Missing required < catCommand > argument on < doesKnowCommand > field.",
                    "path": None,
                    "locations": [{"line": 4, "column": 17}],
                }
            ],
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
            [
                {
                    "message": "Missing required < catCommand > argument on < doesKnowCommand > field.",
                    "path": None,
                    "locations": [{"line": 5, "column": 19}],
                }
            ],
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
            [
                {
                    "message": "Missing required < catCommand > argument on < doesKnowCommand > field.",
                    "path": None,
                    "locations": [{"line": 4, "column": 17}],
                }
            ],
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
            [
                {
                    "message": "Missing required < catCommand > argument on < doesKnowCommand > field.",
                    "path": None,
                    "locations": [{"line": 5, "column": 19}],
                }
            ],
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
            [
                {
                    "message": "Missing required < catCommand > argument on < doesKnowCommand > field.",
                    "path": None,
                    "locations": [{"line": 4, "column": 17}],
                }
            ],
        ),
        # Missing required argument on root directive
        (
            """
            query {
              cat(id: 1) @include {
                name
              }
            }
            """,
            [
                {
                    "message": "Missing required < conditions > argument on < @include > directive.",
                    "path": None,
                    "locations": [{"line": 3, "column": 26}],
                },
                {
                    "message": "Missing required < list > argument on < @include > directive.",
                    "path": None,
                    "locations": [{"line": 3, "column": 26}],
                },
            ],
        ),
        (
            """
            query {
              ... on Query {
                cat(id: 1) @include {
                  name
                }
              }
            }
            """,
            [
                {
                    "message": "Missing required < conditions > argument on < @include > directive.",
                    "path": None,
                    "locations": [{"line": 4, "column": 28}],
                },
                {
                    "message": "Missing required < list > argument on < @include > directive.",
                    "path": None,
                    "locations": [{"line": 4, "column": 28}],
                },
            ],
        ),
        (
            """
            fragment QueryFields on Query {
              cat(id: 1) @include {
                name
              }
            }
            query {
              ...QueryFields
            }
            """,
            [
                {
                    "message": "Missing required < conditions > argument on < @include > directive.",
                    "path": None,
                    "locations": [{"line": 3, "column": 26}],
                },
                {
                    "message": "Missing required < list > argument on < @include > directive.",
                    "path": None,
                    "locations": [{"line": 3, "column": 26}],
                },
            ],
        ),
        (
            """
            fragment QueryFields on Query {
              ... on Query {
                cat(id: 1) @include {
                  name
                }
              }
            }
            query {
              ...QueryFields
            }
            """,
            [
                {
                    "message": "Missing required < conditions > argument on < @include > directive.",
                    "path": None,
                    "locations": [{"line": 4, "column": 28}],
                },
                {
                    "message": "Missing required < list > argument on < @include > directive.",
                    "path": None,
                    "locations": [{"line": 4, "column": 28}],
                },
            ],
        ),
        # Missing required argument on nested directive
        (
            """
            query {
              cat(id: 1) {
                doesKnowCommand(catCommand: "JUMP") @include
              }
            }
            """,
            [
                {
                    "message": "Missing required < conditions > argument on < @include > directive.",
                    "path": None,
                    "locations": [{"line": 4, "column": 53}],
                },
                {
                    "message": "Missing required < list > argument on < @include > directive.",
                    "path": None,
                    "locations": [{"line": 4, "column": 53}],
                },
            ],
        ),
        (
            """
            query {
              ... on Query {
                cat(id: 1) {
                  doesKnowCommand(catCommand: "JUMP") @include
                }
              }
            }
            """,
            [
                {
                    "message": "Missing required < conditions > argument on < @include > directive.",
                    "path": None,
                    "locations": [{"line": 5, "column": 55}],
                },
                {
                    "message": "Missing required < list > argument on < @include > directive.",
                    "path": None,
                    "locations": [{"line": 5, "column": 55}],
                },
            ],
        ),
        (
            """
            fragment QueryFields on Query {
              cat(id: 1) {
                doesKnowCommand(catCommand: "JUMP") @include
              }
            }
            query {
              ...QueryFields
            }
            """,
            [
                {
                    "message": "Missing required < conditions > argument on < @include > directive.",
                    "path": None,
                    "locations": [{"line": 4, "column": 53}],
                },
                {
                    "message": "Missing required < list > argument on < @include > directive.",
                    "path": None,
                    "locations": [{"line": 4, "column": 53}],
                },
            ],
        ),
        (
            """
            fragment QueryFields on Query {
              ... on Query {
                cat(id: 1) {
                  doesKnowCommand(catCommand: "JUMP") @include
                }
              }
            }
            query {
              ...QueryFields
            }
            """,
            [
                {
                    "message": "Missing required < conditions > argument on < @include > directive.",
                    "path": None,
                    "locations": [{"line": 5, "column": 55}],
                },
                {
                    "message": "Missing required < list > argument on < @include > directive.",
                    "path": None,
                    "locations": [{"line": 5, "column": 55}],
                },
            ],
        ),
        (
            """
            fragment CatFields on Cat {
              ... on Cat {
                doesKnowCommand(catCommand: "JUMP") @include
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
            [
                {
                    "message": "Missing required < conditions > argument on < @include > directive.",
                    "path": None,
                    "locations": [{"line": 4, "column": 53}],
                },
                {
                    "message": "Missing required < list > argument on < @include > directive.",
                    "path": None,
                    "locations": [{"line": 4, "column": 53}],
                },
            ],
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
                cat(id: 1) @include {
                  ...CatFields
                }
              }
            }

            query {
              ...QueryFields
            }
            """,
            [
                {
                    "message": "Missing required < conditions > argument on < @include > directive.",
                    "path": None,
                    "locations": [{"line": 10, "column": 28}],
                },
                {
                    "message": "Missing required < list > argument on < @include > directive.",
                    "path": None,
                    "locations": [{"line": 10, "column": 28}],
                },
                {
                    "message": "Missing required < catCommand > argument on < doesKnowCommand > field.",
                    "path": None,
                    "locations": [{"line": 4, "column": 17}],
                },
            ],
        ),
    ],
)
async def test_issue101(query, errors):
    assert await _TTFTT_ENGINE.execute(query) == {
        "data": None,
        "errors": errors,
    }
