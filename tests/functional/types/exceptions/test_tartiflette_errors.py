from datetime import datetime

import pytest

from tartiflette import Resolver, TartifletteError


def tartiflette_execute_nested_error_bakery(schema_name):
    @Resolver("Query.test", schema_name=schema_name)
    @Resolver("Obj.deep", schema_name=schema_name)
    async def resolver_x(*_args, **_kwargs):
        return {}

    @Resolver("Nested.lastUpdate", schema_name=schema_name)
    async def func_field_resolver(*args, **kwargs):
        return [
            datetime(
                year=2018, month=4, day=19, hour=14, minute=57, second=38
            ).timestamp(),
            None,
        ]


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl="""
    type Obj {
        deep: Nested
    }

    type Nested {
        lastUpdate: [Float!]
    }

    type Query {
        test: Obj
    }
    """,
    bakery=tartiflette_execute_nested_error_bakery,
)
async def test_tartiflette_execute_nested_error(schema_stack):
    assert (
        await schema_stack.execute(
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
        == {
            "data": {"test": {"deep": {"lastUpdate": None}}},
            "errors": [
                {
                    "message": "Cannot return null for non-nullable field Nested.lastUpdate.",
                    "path": ["test", "deep", "lastUpdate", 1],
                    "locations": [{"line": 5, "column": 25}],
                }
            ],
        }
    )


def tartiflette_execute_tartifletteerror_custom_bakery(schema_name):
    class CustomException(TartifletteError):
        def __init__(self, code, message):
            super().__init__(message)
            self.code = code
            self.extensions = {"code": code}

    @Resolver("Query.test", schema_name=schema_name)
    @Resolver("Obj.deep", schema_name=schema_name)
    async def resolver_x(*_args, **_kwargs):
        return {}

    @Resolver("Nested.lastUpdate", schema_name=schema_name)
    async def func_field_resolver(*args, **kwargs):
        raise CustomException("my_error", "There is an error")


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl="""
    type Obj {
        deep: Nested
    }

    type Nested {
        lastUpdate: [Float!]
    }

    type Query {
        test: Obj
    }
    """,
    bakery=tartiflette_execute_tartifletteerror_custom_bakery,
)
async def test_tartiflette_execute_tartifletteerror_custom(schema_stack):
    assert (
        await schema_stack.execute(
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
        == {
            "data": {"test": {"deep": {"lastUpdate": None}}},
            "errors": [
                {
                    "message": "There is an error",
                    "path": ["test", "deep", "lastUpdate"],
                    "locations": [{"line": 5, "column": 25}],
                    "extensions": {"code": "my_error"},
                }
            ],
        }
    )
