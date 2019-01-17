import os

import pytest

from tartiflette import Engine, Resolver
from tartiflette.schema.registry import SchemaRegistry

_CURR_PATH = os.path.dirname(os.path.abspath(__file__))

_DEFAULT_SCHEMA = os.path.join(_CURR_PATH, "data", "sdls", "animals.sdl")

_SCHEMAS = {"default": _DEFAULT_SCHEMA, "animals": _DEFAULT_SCHEMA}

_TTFTT_ENGINES = {
    schema_name: Engine(sdl, schema_name=schema_name)
    for schema_name, sdl in _SCHEMAS.items()
}


@pytest.yield_fixture
def clean_registry():
    SchemaRegistry._schemas = {}
    yield SchemaRegistry
    SchemaRegistry._schemas = {}


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


def pytest_runtest_setup(item):
    marker = _get_ttftt_engine_marker(item)
    if not marker:
        return

    resolvers = marker.kwargs.get("resolvers")
    if not resolvers:
        return

    schema_name = _get_schema_name_from_marker(marker)

    # Init schema definitions
    SchemaRegistry._schemas.setdefault(schema_name, {})

    # Reset schema resolvers
    SchemaRegistry._schemas[schema_name]["resolvers"] = []

    # Apply "Resolver" decorators to resolvers functions
    for name, implementation in resolvers.items():
        Resolver(name, schema_name=schema_name)(implementation)

    # Bake resolvers
    for resolver in (
        SchemaRegistry._schemas[schema_name].get("resolvers") or []
    ):
        resolver.bake(_TTFTT_ENGINES[schema_name]._schema)

    # Re-bake engine schema
    _TTFTT_ENGINES[schema_name]._schema.bake()
