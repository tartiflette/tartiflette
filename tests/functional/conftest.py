import os

import pytest

from tartiflette import Engine
from tartiflette.schema.registry import SchemaRegistry


_CURR_PATH = os.path.dirname(os.path.abspath(__file__))

_DEFAULT_ENGINE = Engine(
    os.path.join(_CURR_PATH, "data", "sdls", "animals.sdl")
)

_TTFTT_ENGINES = {
    "default": _DEFAULT_ENGINE,
    "animals": _DEFAULT_ENGINE,
}


@pytest.yield_fixture
def clean_registry():
    SchemaRegistry._schemas = {}
    yield SchemaRegistry
    SchemaRegistry._schemas = {}


def pytest_generate_tests(metafunc):
    try:
        marker = metafunc.definition.get_closest_marker("ttftt_engine")
        if not marker:
            return None
    except AttributeError:
        return None

    engine_name = marker.kwargs.get("name") or "default"
    try:
        engine = _TTFTT_ENGINES[engine_name]
    except KeyError:
        engine = _TTFTT_ENGINES["default"]

    metafunc.parametrize("engine", [engine])
