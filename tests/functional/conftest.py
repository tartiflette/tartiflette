import asyncio
import os

import pytest

from tartiflette import Directive, Resolver, TypeResolver, create_engine
from tartiflette.schema.registry import SchemaRegistry
from tartiflette.subscription.subscription import Subscription

_CURR_PATH = os.path.dirname(os.path.abspath(__file__))


def _get_sdl_path(*args):
    return os.path.join(_CURR_PATH, "data", "sdls", *args)


_DEFAULT_SCHEMA = _get_sdl_path("animals.sdl")

_SCHEMAS = {
    "default": _DEFAULT_SCHEMA,
    "animals": _DEFAULT_SCHEMA,
    "libraries": _get_sdl_path("libraries.sdl"),
    "coercion": (
        _get_sdl_path("coercion.sdl"),
        {"modules": ["tests.functional.coercers.common"]},
    ),
    "pets": os.path.join(_CURR_PATH, "reusable", "pets", "schema.graphql"),
}

_TTFTT_ENGINES = {}
for schema_name, sdl in _SCHEMAS.items():
    sdl, extra = sdl if isinstance(sdl, tuple) else (sdl, {})
    _TTFTT_ENGINES[schema_name] = asyncio.get_event_loop().run_until_complete(
        create_engine(sdl, schema_name=schema_name, **extra)
    )


@pytest.yield_fixture
def clean_registry():
    SchemaRegistry._schemas = {}
    yield SchemaRegistry
    SchemaRegistry._schemas = {}


@pytest.yield_fixture(scope="module")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


def _get_ttftt_engine_marker(node):
    try:
        return node.get_closest_marker("ttftt_engine")
    except AttributeError:
        pass
    return None


def _get_schema_name_from_marker(marker):
    return marker.kwargs.get("name") or "default"


def pytest_generate_tests(metafunc):
    marker = _get_ttftt_engine_marker(metafunc.definition)
    if not marker:
        return

    schema_name = _get_schema_name_from_marker(marker)

    try:
        engine = _TTFTT_ENGINES[schema_name]
    except KeyError:
        engine = _TTFTT_ENGINES["default"]

    metafunc.parametrize("engine", [engine])


def pytest_runtest_teardown(item, nextitem):
    if nextitem:
        nextitem.allow_schema_bake = item.function is not nextitem.function


def pytest_runtest_setup(item):
    marker = _get_ttftt_engine_marker(item)
    if not marker or not getattr(item, "allow_schema_bake", True):
        return

    resolvers = marker.kwargs.get("resolvers") or {}
    type_resolvers = marker.kwargs.get("type_resolvers") or {}
    subscriptions = marker.kwargs.get("subscriptions") or {}
    directives = marker.kwargs.get("directives") or {}
    if not (resolvers or subscriptions or directives):
        return

    schema_name = _get_schema_name_from_marker(marker)

    # Init schema definitions
    SchemaRegistry._schemas.setdefault(schema_name, {})

    # Reset schema resolvers
    if resolvers:
        SchemaRegistry._schemas[schema_name]["resolvers"] = {}

    # Reset schema type_resolvers
    if type_resolvers:
        SchemaRegistry._schemas[schema_name]["type_resolvers"] = {}

    if subscriptions:
        SchemaRegistry._schemas[schema_name]["subscriptions"] = {}

    if directives:
        SchemaRegistry._schemas[schema_name]["directives"] = {}

    # Apply "Resolver" decorators to resolvers functions
    for name, implementation in resolvers.items():
        Resolver(name, schema_name=schema_name)(implementation)

    # Apply "TypeResolver" decorators to type resolvers functions
    for name, implementation in type_resolvers.items():
        TypeResolver(name, schema_name=schema_name)(implementation)

    # Apply "Subscription" decorators to resolvers functions
    for name, implementation in subscriptions.items():
        Subscription(name, schema_name=schema_name)(implementation)

    # Apply "Directive" decorators to resolvers functions
    for name, implementation in directives.items():
        Directive(name, schema_name=schema_name)(implementation)

    # Bake resolvers
    for resolver in (
        SchemaRegistry._schemas[schema_name].get("resolvers") or {}
    ).values():
        resolver.bake(_TTFTT_ENGINES[schema_name]._schema)

    # Bake type resolvers
    for type_resolver in (
        SchemaRegistry._schemas[schema_name].get("type_resolvers") or {}
    ).values():
        type_resolver.bake(_TTFTT_ENGINES[schema_name]._schema)

    # Bake subscriptions
    for subscription in (
        SchemaRegistry._schemas[schema_name].get("subscriptions") or {}
    ).values():
        subscription.bake(_TTFTT_ENGINES[schema_name]._schema)

    # Bake directives
    for directive in (
        SchemaRegistry._schemas[schema_name].get("directives") or {}
    ).values():
        directive.bake(_TTFTT_ENGINES[schema_name]._schema)

    # Re-bake engine schema
    loop = asyncio.new_event_loop()
    loop.run_until_complete(_TTFTT_ENGINES[schema_name]._schema.bake())


def pytest_configure(config):
    config.addinivalue_line("markers", "ttftt_engine: choose a test engine")
