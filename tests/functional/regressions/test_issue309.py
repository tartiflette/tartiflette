import pytest

from tartiflette import (
    Resolver,
    create_schema,
    create_schema_with_operators,
    executor_factory,
)

_SDL = """
type Query {
  name: String
}
"""


async def custom_error_coercer(exception, error):
    return {"message": "Oopsie"}


async def from_create_schema_with_operators(schema_name):
    _, execute, __ = await create_schema_with_operators(
        _SDL, name=schema_name, error_coercer=custom_error_coercer
    )
    return execute


async def from_executor_factory(schema_name):
    schema = await create_schema(_SDL, name=schema_name)
    return executor_factory(schema, error_coercer=custom_error_coercer)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "executor_factory",
    [from_create_schema_with_operators, from_executor_factory],
)
async def test_error_coercers(random_schema_name, executor_factory):
    @Resolver("Query.name", schema_name=random_schema_name)
    async def resolve_query_name(*_):
        raise Exception("Oopsie")

    execute = await executor_factory(random_schema_name)

    assert (
        await execute(
            """
            query {
              name
            }
            """
        )
        == {"data": {"name": None}, "errors": [{"message": "Oopsie"}]}
    )
