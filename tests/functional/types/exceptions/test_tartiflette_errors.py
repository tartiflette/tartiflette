from datetime import datetime

import pytest

from tartiflette import Resolver
from tartiflette.engine import Engine


@pytest.mark.asyncio
async def test_tartiflette_execute_nested_error():
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

    ttftt = Engine(schema_sdl)

    @Resolver("Nested.lastUpdate", schema=ttftt.schema)
    async def func_field_resolver(*args, **kwargs):
        return [
            datetime(
                year=2018, month=4, day=19, hour=14, minute=57, second=38
            ).timestamp(),
            None,
        ]

    result = await ttftt.execute(
        """
    query Test{
        test {
            deep {
                lastUpdate
            }
        }
    }
    """
    )

    assert {
        "data": {"test": {"deep": {"lastUpdate": None}}},
        "errors": [
            {
                "message": "Shouldn't be null - lastUpdate is not nullable",
                "path": ["test", "deep", "lastUpdate"],
                "locations": [{"line": 1, "column": 68}],
            }
        ],
    } == result
