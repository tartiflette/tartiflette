from datetime import datetime

import pytest

from tartiflette import Resolver, Scalar, create_schema_with_operators


def tartiflette_execute_scalar_type_output_bakery(schema_name):
    @Resolver("Query.lastUpdate", schema_name=schema_name)
    async def resolve_query_last_update(*args, **kwargs):
        return datetime(
            year=2018, month=4, day=19, hour=14, minute=57, second=38
        )


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl="""
    type Query {
        lastUpdate: DateTime
    }
    """,
    bakery=tartiflette_execute_scalar_type_output_bakery,
)
async def test_tartiflette_execute_scalar_type_output(schema_stack):
    assert (
        await schema_stack.execute(
            """
            query Test{
                lastUpdate
            }
            """,
            operation_name="Test",
        )
        == {"data": {"lastUpdate": "2018-04-19T14:57:38"}}
    )


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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
                    },
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 1],
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
                    },
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField", 1],
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
                    },
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 1],
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
                    },
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField", 1],
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
                    },
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 1],
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
                    },
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField", 1],
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
                    },
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 1],
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
                    },
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField", 1],
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
                    },
                    {
                        "message": "Cannot return null for non-nullable field Query.testField.",
                        "path": ["testField", 1],
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
                    },
                    {
                        "message": "Expected Iterable, but did not find one for field Query.testField.",
                        "path": ["testField", 1],
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
                        "locations": [{"line": 3, "column": 17}],
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
    input_sdl, resolver_response, expected, random_schema_name
):
    @Resolver("Query.testField", schema_name=random_schema_name)
    async def resolve_query_test_field(*args, **kwargs):
        return resolver_response

    _, execute, __ = await create_schema_with_operators(
        """
        type Query {{
            testField: {}
        }}
        """.format(
            input_sdl
        ),
        name=random_schema_name,
    )

    assert (
        await execute(
            """
            query Test{
                testField
            }
            """,
            operation_name="Test",
        )
        == expected
    )


def tartiflette_declare_custom_scalar_bakery(schema_name):
    @Resolver("Query.alol", schema_name=schema_name)
    async def alol_resolver(*_, **__):
        class customobject:
            def __init__(self, p1):
                self.p1 = p1

        return {"joey": customobject("OL")}

    @Scalar(name="Ntm", schema_name=schema_name)
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


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl="""
    scalar Ntm

    type Lol {
        joey: Ntm
    }

    type Query {
        alol: Lol
    }
    """,
    bakery=tartiflette_declare_custom_scalar_bakery,
)
async def test_tartiflette_declare_custom_scalar(schema_stack):
    assert (
        await schema_stack.execute(
            """
            query {
                alol {
                    joey
                }
            }
            """
        )
        == {"data": {"alol": {"joey": "I'am a val OL "}}}
    )
