from datetime import datetime

import pytest

from tartiflette import Resolver, create_engine


@pytest.mark.asyncio
async def test_tartiflette_execute_scalar_type_output(clean_registry):
    schema_sdl = """
    type Query {
        lastUpdate: DateTime
    }
    """

    @Resolver("Query.lastUpdate")
    async def func_field_resolver(*args, **kwargs):
        return datetime(
            year=2018, month=4, day=19, hour=14, minute=57, second=38
        )

    ttftt = await create_engine(schema_sdl)

    result = await ttftt.execute(
        """
    query Test{
        lastUpdate
    }
    """,
        operation_name="Test",
    )

    assert {"data": {"lastUpdate": "2018-04-19T14:57:38"}} == result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_sdl,resolver_response,expected",
    [
        # Boolean
        ("Boolean", None, {"data": {"testField": None}}),
        ("Boolean", True, {"data": {"testField": True}}),
        (
            "Boolean!",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        ("Boolean!", True, {"data": {"testField": True}}),
        ("[Boolean]", None, {"data": {"testField": None}}),
        ("[Boolean]", [None], {"data": {"testField": [None]}}),
        (
            "[Boolean]",
            True,
            {
                "data": {"testField": None},
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        ("[Boolean]", [True], {"data": {"testField": [True]}}),
        ("[Boolean]", [True, None], {"data": {"testField": [True, None]}}),
        ("[Boolean]", [True, False], {"data": {"testField": [True, False]}}),
        (
            "[Boolean]!",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        ("[Boolean]!", [None], {"data": {"testField": [None]}}),
        (
            "[Boolean]!",
            True,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        ("[Boolean]!", [True], {"data": {"testField": [True]}}),
        ("[Boolean]!", [True, None], {"data": {"testField": [True, None]}}),
        ("[Boolean]!", [True, False], {"data": {"testField": [True, False]}}),
        ("[Boolean!]", None, {"data": {"testField": None}}),
        (
            "[Boolean!]",
            [None],
            {
                "data": {"testField": None},
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 0],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        (
            "[Boolean!]",
            True,
            {
                "data": {"testField": None},
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        ("[Boolean!]", [True], {"data": {"testField": [True]}}),
        (
            "[Boolean!]",
            [True, None],
            {
                "data": {"testField": None},
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 1],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        ("[Boolean!]", [True, False], {"data": {"testField": [True, False]}}),
        (
            "[Boolean!]!",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        (
            "[Boolean!]!",
            [None],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 0],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        (
            "[Boolean!]!",
            True,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        ("[Boolean!]!", [True], {"data": {"testField": [True]}}),
        (
            "[Boolean!]!",
            [True, None],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 1],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        ("[Boolean!]!", [True, False], {"data": {"testField": [True, False]}}),
        (
            "[[Boolean!]!]!",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        (
            "[[Boolean!]!]!",
            [None],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 0],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        (
            "[[Boolean!]!]!",
            True,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        (
            "[[Boolean!]!]!",
            [True],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField", 0],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        (
            "[[Boolean!]!]!",
            [True, None],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField", 0],
                        "locations": [{"line": 3, "column": 13}],
                    },
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 1],
                        "locations": [{"line": 3, "column": 13}],
                    },
                ],
            },
        ),
        (
            "[[Boolean!]!]!",
            [True, False],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField", 0],
                        "locations": [{"line": 3, "column": 13}],
                    },
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField", 1],
                        "locations": [{"line": 3, "column": 13}],
                    },
                ],
            },
        ),
        (
            "[[Boolean!]!]!",
            [[None]],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 0, 0],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        ("[[Boolean!]!]!", [[True]], {"data": {"testField": [[True]]}}),
        (
            "[[Boolean!]!]!",
            [[True, None]],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 0, 1],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        (
            "[[Boolean!]!]!",
            [[True, False]],
            {"data": {"testField": [[True, False]]}},
        ),
        # Float
        ("Float", None, {"data": {"testField": None}}),
        ("Float", 45.0, {"data": {"testField": 45.0}}),
        (
            "Float!",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        ("Float!", 45.0, {"data": {"testField": 45.0}}),
        ("[Float]", None, {"data": {"testField": None}}),
        ("[Float]", [None], {"data": {"testField": [None]}}),
        (
            "[Float]",
            45.0,
            {
                "data": {"testField": None},
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        ("[Float]", [45.0], {"data": {"testField": [45.0]}}),
        ("[Float]", [45.0, None], {"data": {"testField": [45.0, None]}}),
        ("[Float]", [45.0, 46.1], {"data": {"testField": [45.0, 46.1]}}),
        (
            "[Float]!",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        ("[Float]!", [None], {"data": {"testField": [None]}}),
        (
            "[Float]!",
            45.0,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        ("[Float]!", [45.0], {"data": {"testField": [45.0]}}),
        ("[Float]!", [45.0, None], {"data": {"testField": [45.0, None]}}),
        ("[Float]!", [45.0, 46.1], {"data": {"testField": [45.0, 46.1]}}),
        ("[Float!]", None, {"data": {"testField": None}}),
        (
            "[Float!]",
            [None],
            {
                "data": {"testField": None},
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 0],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        (
            "[Float!]",
            45.0,
            {
                "data": {"testField": None},
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        ("[Float!]", [45.0], {"data": {"testField": [45.0]}}),
        (
            "[Float!]",
            [45.0, None],
            {
                "data": {"testField": None},
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 1],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        ("[Float!]", [45.0, 46.1], {"data": {"testField": [45.0, 46.1]}}),
        (
            "[Float!]!",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        (
            "[Float!]!",
            [None],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 0],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        (
            "[Float!]!",
            45.0,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        ("[Float!]!", [45.0], {"data": {"testField": [45.0]}}),
        (
            "[Float!]!",
            [45.0, None],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 1],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        ("[Float!]!", [45.0, 46.1], {"data": {"testField": [45.0, 46.1]}}),
        (
            "[[Float!]!]!",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        (
            "[[Float!]!]!",
            [None],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 0],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        (
            "[[Float!]!]!",
            45.0,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        (
            "[[Float!]!]!",
            [45.0],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField", 0],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        (
            "[[Float!]!]!",
            [45.0, None],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField", 0],
                        "locations": [{"line": 3, "column": 13}],
                    },
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 1],
                        "locations": [{"line": 3, "column": 13}],
                    },
                ],
            },
        ),
        (
            "[[Float!]!]!",
            [45.0, 46.1],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField", 0],
                        "locations": [{"line": 3, "column": 13}],
                    },
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField", 1],
                        "locations": [{"line": 3, "column": 13}],
                    },
                ],
            },
        ),
        (
            "[[Float!]!]!",
            [[None]],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 0, 0],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        ("[[Float!]!]!", [[45.0]], {"data": {"testField": [[45.0]]}}),
        (
            "[[Float!]!]!",
            [[45.0, None]],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 0, 1],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        (
            "[[Float!]!]!",
            [[45.0, 46.1]],
            {"data": {"testField": [[45.0, 46.1]]}},
        ),
        # Int
        ("Int", None, {"data": {"testField": None}}),
        ("Int", 45, {"data": {"testField": 45}}),
        (
            "Int!",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        ("Int!", 45, {"data": {"testField": 45}}),
        ("[Int]", None, {"data": {"testField": None}}),
        ("[Int]", [None], {"data": {"testField": [None]}}),
        (
            "[Int]",
            45,
            {
                "data": {"testField": None},
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        ("[Int]", [45], {"data": {"testField": [45]}}),
        ("[Int]", [45, None], {"data": {"testField": [45, None]}}),
        ("[Int]", [45, 46], {"data": {"testField": [45, 46]}}),
        (
            "[Int]!",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        ("[Int]!", [None], {"data": {"testField": [None]}}),
        (
            "[Int]!",
            45,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        ("[Int]!", [45], {"data": {"testField": [45]}}),
        ("[Int]!", [45, None], {"data": {"testField": [45, None]}}),
        ("[Int]!", [45, 46], {"data": {"testField": [45, 46]}}),
        ("[Int!]", None, {"data": {"testField": None}}),
        (
            "[Int!]",
            [None],
            {
                "data": {"testField": None},
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 0],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        (
            "[Int!]",
            45,
            {
                "data": {"testField": None},
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        ("[Int!]", [45], {"data": {"testField": [45]}}),
        (
            "[Int!]",
            [45, None],
            {
                "data": {"testField": None},
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 1],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        ("[Int!]", [45, 46], {"data": {"testField": [45, 46]}}),
        (
            "[Int!]!",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        (
            "[Int!]!",
            [None],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 0],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        (
            "[Int!]!",
            45,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        ("[Int!]!", [45], {"data": {"testField": [45]}}),
        (
            "[Int!]!",
            [45, None],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 1],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        ("[Int!]!", [45, 46], {"data": {"testField": [45, 46]}}),
        (
            "[[Int!]!]!",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        (
            "[[Int!]!]!",
            [None],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 0],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        (
            "[[Int!]!]!",
            45,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        (
            "[[Int!]!]!",
            [45],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField", 0],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        (
            "[[Int!]!]!",
            [45, None],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField", 0],
                        "locations": [{"line": 3, "column": 13}],
                    },
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 1],
                        "locations": [{"line": 3, "column": 13}],
                    },
                ],
            },
        ),
        (
            "[[Int!]!]!",
            [45, 46],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField", 0],
                        "locations": [{"line": 3, "column": 13}],
                    },
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField", 1],
                        "locations": [{"line": 3, "column": 13}],
                    },
                ],
            },
        ),
        (
            "[[Int!]!]!",
            [[None]],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 0, 0],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        ("[[Int!]!]!", [[45]], {"data": {"testField": [[45]]}}),
        (
            "[[Int!]!]!",
            [[45, None]],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 0, 1],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        ("[[Int!]!]!", [[45, 46]], {"data": {"testField": [[45, 46]]}}),
        # String
        ("String", None, {"data": {"testField": None}}),
        ("String", "value1", {"data": {"testField": "value1"}}),
        (
            "String!",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        ("String!", "value1", {"data": {"testField": "value1"}}),
        ("[String]", None, {"data": {"testField": None}}),
        ("[String]", [None], {"data": {"testField": [None]}}),
        (
            "[String]",
            "value1",
            {
                "data": {"testField": None},
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        ("[String]", ["value1"], {"data": {"testField": ["value1"]}}),
        (
            "[String]",
            ["value1", None],
            {"data": {"testField": ["value1", None]}},
        ),
        (
            "[String]",
            ["value1", "value2"],
            {"data": {"testField": ["value1", "value2"]}},
        ),
        (
            "[String]!",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        ("[String]!", [None], {"data": {"testField": [None]}}),
        (
            "[String]!",
            "value1",
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        ("[String]!", ["value1"], {"data": {"testField": ["value1"]}}),
        (
            "[String]!",
            ["value1", None],
            {"data": {"testField": ["value1", None]}},
        ),
        (
            "[String]!",
            ["value1", "value2"],
            {"data": {"testField": ["value1", "value2"]}},
        ),
        ("[String!]", None, {"data": {"testField": None}}),
        (
            "[String!]",
            [None],
            {
                "data": {"testField": None},
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 0],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        (
            "[String!]",
            "value1",
            {
                "data": {"testField": None},
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        ("[String!]", ["value1"], {"data": {"testField": ["value1"]}}),
        (
            "[String!]",
            ["value1", None],
            {
                "data": {"testField": None},
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 1],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        (
            "[String!]",
            ["value1", "value2"],
            {"data": {"testField": ["value1", "value2"]}},
        ),
        (
            "[String!]!",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        (
            "[String!]!",
            [None],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 0],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        (
            "[String!]!",
            "value1",
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        ("[String!]!", ["value1"], {"data": {"testField": ["value1"]}}),
        (
            "[String!]!",
            ["value1", None],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 1],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        (
            "[String!]!",
            ["value1", "value2"],
            {"data": {"testField": ["value1", "value2"]}},
        ),
        (
            "[[String!]!]!",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        (
            "[[String!]!]!",
            [None],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 0],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        (
            "[[String!]!]!",
            "value1",
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        (
            "[[String!]!]!",
            ["value1"],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField", 0],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        (
            "[[String!]!]!",
            ["value1", None],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField", 0],
                        "locations": [{"line": 3, "column": 13}],
                    },
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 1],
                        "locations": [{"line": 3, "column": 13}],
                    },
                ],
            },
        ),
        (
            "[[String!]!]!",
            ["value1", "value2"],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField", 0],
                        "locations": [{"line": 3, "column": 13}],
                    },
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField", 1],
                        "locations": [{"line": 3, "column": 13}],
                    },
                ],
            },
        ),
        (
            "[[String!]!]!",
            [[None]],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 0, 0],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        ("[[String!]!]!", [["value1"]], {"data": {"testField": [["value1"]]}}),
        (
            "[[String!]!]!",
            [["value1", None]],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 0, 1],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        (
            "[[String!]!]!",
            [["value1", "value2"]],
            {"data": {"testField": [["value1", "value2"]]}},
        ),
        # DateTime
        ("DateTime", None, {"data": {"testField": None}}),
        (
            "DateTime",
            datetime(
                year=2018, month=4, day=19, hour=14, minute=57, second=38
            ),
            {"data": {"testField": "2018-04-19T14:57:38"}},
        ),
        (
            "DateTime!",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        (
            "DateTime!",
            datetime(
                year=2018, month=4, day=19, hour=14, minute=57, second=38
            ),
            {"data": {"testField": "2018-04-19T14:57:38"}},
        ),
        ("[DateTime]", None, {"data": {"testField": None}}),
        ("[DateTime]", [None], {"data": {"testField": [None]}}),
        (
            "[DateTime]",
            datetime(
                year=2018, month=4, day=19, hour=14, minute=57, second=38
            ),
            {
                "data": {"testField": None},
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        (
            "[DateTime]",
            [
                datetime(
                    year=2018, month=4, day=19, hour=14, minute=57, second=38
                )
            ],
            {"data": {"testField": ["2018-04-19T14:57:38"]}},
        ),
        (
            "[DateTime]",
            [
                datetime(
                    year=2018, month=4, day=19, hour=14, minute=57, second=38
                ),
                None,
            ],
            {"data": {"testField": ["2018-04-19T14:57:38", None]}},
        ),
        (
            "[DateTime]",
            [
                datetime(
                    year=2018, month=4, day=19, hour=14, minute=57, second=38
                ),
                datetime(
                    year=2017, month=3, day=18, hour=13, minute=56, second=37
                ),
            ],
            {
                "data": {
                    "testField": ["2018-04-19T14:57:38", "2017-03-18T13:56:37"]
                }
            },
        ),
        (
            "[DateTime]!",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        ("[DateTime]!", [None], {"data": {"testField": [None]}}),
        (
            "[DateTime]!",
            datetime(
                year=2018, month=4, day=19, hour=14, minute=57, second=38
            ),
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        (
            "[DateTime]!",
            [
                datetime(
                    year=2018, month=4, day=19, hour=14, minute=57, second=38
                )
            ],
            {"data": {"testField": ["2018-04-19T14:57:38"]}},
        ),
        (
            "[DateTime]!",
            [
                datetime(
                    year=2018, month=4, day=19, hour=14, minute=57, second=38
                ),
                None,
            ],
            {"data": {"testField": ["2018-04-19T14:57:38", None]}},
        ),
        (
            "[DateTime]!",
            [
                datetime(
                    year=2018, month=4, day=19, hour=14, minute=57, second=38
                ),
                datetime(
                    year=2017, month=3, day=18, hour=13, minute=56, second=37
                ),
            ],
            {
                "data": {
                    "testField": ["2018-04-19T14:57:38", "2017-03-18T13:56:37"]
                }
            },
        ),
        ("[DateTime!]", None, {"data": {"testField": None}}),
        (
            "[DateTime!]",
            [None],
            {
                "data": {"testField": None},
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 0],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        (
            "[DateTime!]",
            datetime(
                year=2018, month=4, day=19, hour=14, minute=57, second=38
            ),
            {
                "data": {"testField": None},
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        (
            "[DateTime!]",
            [
                datetime(
                    year=2018, month=4, day=19, hour=14, minute=57, second=38
                )
            ],
            {"data": {"testField": ["2018-04-19T14:57:38"]}},
        ),
        (
            "[DateTime!]",
            [
                datetime(
                    year=2018, month=4, day=19, hour=14, minute=57, second=38
                ),
                None,
            ],
            {
                "data": {"testField": None},
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 1],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        (
            "[DateTime!]",
            [
                datetime(
                    year=2018, month=4, day=19, hour=14, minute=57, second=38
                ),
                datetime(
                    year=2017, month=3, day=18, hour=13, minute=56, second=37
                ),
            ],
            {
                "data": {
                    "testField": ["2018-04-19T14:57:38", "2017-03-18T13:56:37"]
                }
            },
        ),
        (
            "[DateTime!]!",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        (
            "[DateTime!]!",
            [None],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 0],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        (
            "[DateTime!]!",
            datetime(
                year=2018, month=4, day=19, hour=14, minute=57, second=38
            ),
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        (
            "[DateTime!]!",
            [
                datetime(
                    year=2018, month=4, day=19, hour=14, minute=57, second=38
                )
            ],
            {"data": {"testField": ["2018-04-19T14:57:38"]}},
        ),
        (
            "[DateTime!]!",
            [
                datetime(
                    year=2018, month=4, day=19, hour=14, minute=57, second=38
                ),
                None,
            ],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 1],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        (
            "[DateTime!]!",
            [
                datetime(
                    year=2018, month=4, day=19, hour=14, minute=57, second=38
                ),
                datetime(
                    year=2017, month=3, day=18, hour=13, minute=56, second=37
                ),
            ],
            {
                "data": {
                    "testField": ["2018-04-19T14:57:38", "2017-03-18T13:56:37"]
                }
            },
        ),
        (
            "[[DateTime!]!]!",
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        (
            "[[DateTime!]!]!",
            [None],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 0],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        (
            "[[DateTime!]!]!",
            datetime(
                year=2018, month=4, day=19, hour=14, minute=57, second=38
            ),
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField"],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        (
            "[[DateTime!]!]!",
            [
                datetime(
                    year=2018, month=4, day=19, hour=14, minute=57, second=38
                )
            ],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField", 0],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        (
            "[[DateTime!]!]!",
            [
                datetime(
                    year=2018, month=4, day=19, hour=14, minute=57, second=38
                ),
                None,
            ],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField", 0],
                        "locations": [{"line": 3, "column": 13}],
                    },
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 1],
                        "locations": [{"line": 3, "column": 13}],
                    },
                ],
            },
        ),
        (
            "[[DateTime!]!]!",
            [
                datetime(
                    year=2018, month=4, day=19, hour=14, minute=57, second=38
                ),
                datetime(
                    year=2017, month=3, day=18, hour=13, minute=56, second=37
                ),
            ],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField", 0],
                        "locations": [{"line": 3, "column": 13}],
                    },
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField", 1],
                        "locations": [{"line": 3, "column": 13}],
                    },
                ],
            },
        ),
        (
            "[[DateTime!]!]!",
            [[None]],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 0, 0],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        (
            "[[DateTime!]!]!",
            [
                [
                    datetime(
                        year=2018,
                        month=4,
                        day=19,
                        hour=14,
                        minute=57,
                        second=38,
                    )
                ]
            ],
            {"data": {"testField": [["2018-04-19T14:57:38"]]}},
        ),
        (
            "[[DateTime!]!]!",
            [
                [
                    datetime(
                        year=2018,
                        month=4,
                        day=19,
                        hour=14,
                        minute=57,
                        second=38,
                    ),
                    None,
                ]
            ],
            {
                "data": None,
                "errors": [
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 0, 1],
                        "locations": [{"line": 3, "column": 13}],
                    }
                ],
            },
        ),
        (
            "[[DateTime!]!]!",
            [
                [
                    datetime(
                        year=2018,
                        month=4,
                        day=19,
                        hour=14,
                        minute=57,
                        second=38,
                    ),
                    datetime(
                        year=2017,
                        month=3,
                        day=18,
                        hour=13,
                        minute=56,
                        second=37,
                    ),
                ]
            ],
            {
                "data": {
                    "testField": [
                        ["2018-04-19T14:57:38", "2017-03-18T13:56:37"]
                    ]
                }
            },
        ),
    ],
)
async def test_tartiflette_execute_scalar_type_advanced(
    input_sdl, resolver_response, expected, clean_registry
):
    schema_sdl = """
    type Query {{
        testField: {}
    }}
    """.format(
        input_sdl
    )

    @Resolver("Query.testField")
    async def func_field_resolver(*args, **kwargs):
        return resolver_response

    ttftt = await create_engine(schema_sdl)

    result = await ttftt.execute(
        """
        query Test{
            testField
        }
        """,
        operation_name="Test",
    )

    assert expected == result


@pytest.mark.asyncio
async def test_tartiflette_declare_custom_scalar(clean_registry):
    from tartiflette import Scalar

    sdl = """
        scalar Ntm

        type Lol {
            joey: Ntm
        }

        type Query {
            alol: Lol
        }
    """

    @Resolver("Query.alol")
    async def alol_resolver(*_, **__):
        class customobject:
            def __init__(self, p1):
                self.p1 = p1

        return {"joey": customobject("OL")}

    @Scalar(name="Ntm")
    class Ntm:
        @staticmethod
        def coerce_output(val):
            return "I'am a val %s " % val.p1

        @staticmethod
        def coerce_input(val):
            return val

        @staticmethod
        def parse_literal(ast: "Node") -> str:
            return ast.value

    ttftt = await create_engine(sdl)

    result = await ttftt.execute(
        query="""
        query {
            alol {
                joey
            }
        }
        """
    )

    assert {"data": {"alol": {"joey": "I'am a val OL "}}} == result
