import pytest

from tartiflette.schema.registry import SchemaRegistry


@pytest.yield_fixture
def clean_registry():
    SchemaRegistry.clean()
    yield SchemaRegistry
    SchemaRegistry.clean()
