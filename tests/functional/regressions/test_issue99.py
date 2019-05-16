import pytest


# TODO: unskip this test once `validate_document` function has been implemented
@pytest.mark.skip(
    reason="Will handled by the `validate_document` function which isn't implemented yet."
)
@pytest.mark.asyncio
@pytest.mark.ttftt_engine
@pytest.mark.parametrize(
    "query,errors",
    [
        (
            """
            query {
              cat {
                name
                doesKnowCommand(catCommand: JUMP, catCommand: JUMP)
              }
            }
            """,
            [
                {
                    "message": "There can be only one argument named < catCommand >.",
                    "path": None,
                    "locations": [
                        {"line": 5, "column": 33},
                        {"line": 5, "column": 51},
                    ],
                }
            ],
        ),
        (
            """
            query {
              cat {
                name
                doesKnowCommand(catCommand: JUMP, catCommand: JUMP, catCommand: JUMP)
              }
            }
            """,
            [
                {
                    "message": "There can be only one argument named < catCommand >.",
                    "path": None,
                    "locations": [
                        {"line": 5, "column": 33},
                        {"line": 5, "column": 51},
                    ],
                },
                {
                    "message": "There can be only one argument named < catCommand >.",
                    "path": None,
                    "locations": [
                        {"line": 5, "column": 33},
                        {"line": 5, "column": 69},
                    ],
                },
            ],
        ),
        (
            """
            query {
              cat {
                name @deprecated(reason: "first", reason: "second")
              }
            }
            """,
            [
                {
                    "message": "There can be only one argument named < reason >.",
                    "path": None,
                    "locations": [
                        {"line": 4, "column": 34},
                        {"line": 4, "column": 51},
                    ],
                }
            ],
        ),
        (
            """
            query {
              cat {
                name @deprecated(reason: "first", reason: "second", reason: "third")
              }
            }
            """,
            [
                {
                    "message": "There can be only one argument named < reason >.",
                    "path": None,
                    "locations": [
                        {"line": 4, "column": 34},
                        {"line": 4, "column": 51},
                    ],
                },
                {
                    "message": "There can be only one argument named < reason >.",
                    "path": None,
                    "locations": [
                        {"line": 4, "column": 34},
                        {"line": 4, "column": 69},
                    ],
                },
            ],
        ),
    ],
)
async def test_issue99(engine, query, errors):
    assert await engine.execute(query) == {"data": None, "errors": errors}
