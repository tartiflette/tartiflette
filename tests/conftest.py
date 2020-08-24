import asyncio

from functools import partial
from uuid import uuid4

import pytest

from tartiflette import create_schema_with_operators
from tartiflette.schema.registry import SchemaRegistry
from tests.data.utils import get_path_to_sdl, load_sdl
from tests.schema_stack import SchemaStack

_KNOWN_SCHEMA_STACKS = {}
_KNOWN_SCHEMAS = {
    "animals": get_path_to_sdl("animals.graphql"),
    "libraries": get_path_to_sdl("libraries.graphql"),
    "coercion": (
        get_path_to_sdl("coercion.graphql"),
        {"modules": ["tests.data.modules.pets.common"]},
    ),
    "pets": get_path_to_sdl("pets.graphql"),
    "harness": get_path_to_sdl("harness.graphql"),
}


@pytest.yield_fixture(scope="module")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.yield_fixture
def clean_registry():
    SchemaRegistry.clean()
    yield SchemaRegistry
    SchemaRegistry.clean()


@pytest.fixture
def random_schema_name():
    return uuid4().hex


@pytest.fixture
def random_schema_name():
    return uuid4().hex


def _forge_schema_stack_hash(sdl, options):
    stack_hash = load_sdl(sdl)
    if options:
        for option in options.values():
            stack_hash = f"{stack_hash}{str(id(option))}"
    return str(hash(stack_hash))


def _fetch_with_schema_stack_marker(node):
    try:
        return node.get_closest_marker("with_schema_stack")
    except AttributeError:
        pass
    return None


async def _build_schema_stack_from_marker(marker):
    marker_kwargs = dict(marker.kwargs)

    preset = marker_kwargs.pop("preset", None)
    sdl = marker_kwargs.pop("sdl", None)

    if not bool(preset) ^ bool(sdl):
        raise Exception(
            "The < preset > or < sdl > option must be provided, but not both "
            "at the same time."
        )

    if preset:
        known_schema = _KNOWN_SCHEMAS[preset]
        sdl, extra = (
            known_schema
            if isinstance(known_schema, tuple)
            else (known_schema, {})
        )
        marker_kwargs.update(extra)

    loaded_sdl = load_sdl(sdl if preset else sdl)
    schema_stack_hash = _forge_schema_stack_hash(loaded_sdl, marker_kwargs)

    schema_stack = _KNOWN_SCHEMA_STACKS.get(schema_stack_hash)
    if not schema_stack:
        bakery = marker_kwargs.pop("bakery", None)
        if bakery:
            bakery(schema_stack_hash)

        schema, executor, subscriptor = await create_schema_with_operators(
            loaded_sdl, name=schema_stack_hash, **marker_kwargs
        )
        schema_stack = _KNOWN_SCHEMA_STACKS[schema_stack_hash] = SchemaStack(
            schema_stack_hash, schema, executor, subscriptor
        )

    return schema_stack


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "with_schema_stack: parametrize a schema"
    )


def pytest_generate_tests(metafunc):
    marker = _fetch_with_schema_stack_marker(metafunc.definition)
    if not marker:
        return

    metafunc.parametrize(
        "schema_stack", [partial(_build_schema_stack_from_marker, marker)]
    )


def pytest_runtest_setup(item):
    marker = _fetch_with_schema_stack_marker(item)
    if not marker:
        return

    item.callspec.params[
        "schema_stack"
    ] = asyncio.get_event_loop().run_until_complete(
        item.callspec.params["schema_stack"]()
    )
