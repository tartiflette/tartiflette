import pytest

from tartiflette.schema.registry import SchemaRegistry


@pytest.fixture
def clean_registry():
    SchemaRegistry.clean()
    yield SchemaRegistry
    SchemaRegistry.clean()
