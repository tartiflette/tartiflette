import pytest

from tartiflette import Engine, Resolver, create_engine

_SDL = """
type Query {
  name: String
}
"""

_QUERY = """
query {
  name
}
"""

_EXPECTED = {"data": {"name": None}, "errors": [{"message": "Oopsie"}]}


async def custom_error_coercer(exception, error):
    return {"message": "Oopsie"}


async def from_create_engine(schema_name):
    return await create_engine(
        _SDL, schema_name=schema_name, error_coercer=custom_error_coercer
    )


async def from_engine_class_init(schema_name):
    engine = Engine(
        _SDL, schema_name=schema_name, error_coercer=custom_error_coercer
    )
    await engine.cook()
    return engine


async def from_engine_class_cook(schema_name):
    engine = Engine()
    await engine.cook(
        _SDL, schema_name=schema_name, error_coercer=custom_error_coercer
    )
    return engine


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "engine_factory",
    [from_create_engine, from_engine_class_init, from_engine_class_cook],
)
async def test_error_coercers(random_schema_name, engine_factory):
    @Resolver("Query.name", schema_name=random_schema_name)
    async def resolve_query_name(*_):
        raise Exception("Oopsie")

    engine = await engine_factory(random_schema_name)
    assert await engine.execute(_QUERY) == _EXPECTED
