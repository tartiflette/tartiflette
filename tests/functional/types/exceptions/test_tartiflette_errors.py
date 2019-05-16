from datetime import datetime

import pytest

from tartiflette import Resolver, TartifletteError, create_engine


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

    @Resolver("Query.test")
    @Resolver("Obj.deep")
    async def resolver_x(*_args, **_kwargs):
        return {}

    @Resolver("Nested.lastUpdate")
    async def func_field_resolver(*args, **kwargs):
        return [
            datetime(
                year=2018, month=4, day=19, hour=14, minute=57, second=38
            ).timestamp(),
            None,
        ]

    ttftt = await create_engine(schema_sdl)

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
                "message": "Cannot return null for non-nullable field Nested.lastUpdate.",
                "path": ["test", "deep", "lastUpdate", 1],
                "locations": [{"line": 5, "column": 17}],
            }
        ],
    } == result


@pytest.mark.asyncio
async def test_tartiflette_execute_tartifletteerror_custom(clean_registry):
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

    class CustomException(TartifletteError):
        def __init__(self, code, message):
            super().__init__(message)
            self.code = code
            self.extensions = {"code": code}

    @Resolver("Query.test")
    @Resolver("Obj.deep")
    async def resolver_x(*_args, **_kwargs):
        return {}

    @Resolver("Nested.lastUpdate")
    async def func_field_resolver(*args, **kwargs):
        raise CustomException("my_error", "There is an error")

    ttftt = await create_engine(schema_sdl)

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
                "message": "There is an error",
                "path": ["test", "deep", "lastUpdate"],
                "locations": [{"line": 5, "column": 17}],
                "extensions": {"code": "my_error"},
            }
        ],
    } == result
