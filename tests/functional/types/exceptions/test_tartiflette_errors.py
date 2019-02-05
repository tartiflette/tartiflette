from datetime import datetime

import pytest

from tartiflette import Resolver
from tartiflette.engine import Engine


@pytest.mark.asyncio
async def test_tartiflette_execute_nested_error(clean_registry):
    schema_sdl = """

    type Obj {
        deep: Nested
    }

    type Nested {
        lastUpdate: [Float!]
    }

    type Query {
        test: Obj
    }
    """

    @Resolver("Nested.lastUpdate")
    async def func_field_resolver(*args, **kwargs):
        return [
            datetime(
                year=2018, month=4, day=19, hour=14, minute=57, second=38
            ).timestamp(),
            None,
        ]

    ttftt = Engine(schema_sdl)

    result = await ttftt.execute(
        """
    query Test{
        test {
            deep {
                lastUpdate
            }
        }
    }
    """,
        operation_name="Test",
    )

    assert {
        "data": {"test": {"deep": {"lastUpdate": None}}},
        "errors": [
            {
                "message": "Invalid value (value: None) for field `lastUpdate` of type `[Float!]`",
                "path": ["test", "deep", "lastUpdate"],
                "locations": [{"line": 5, "column": 17}],
            }
        ],
    } == result
