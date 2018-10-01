import pytest
from tartiflette.schema.registry import SchemaRegistry


@pytest.yield_fixture
def clean_registry():
    SchemaRegistry._schemas = {}
    yield SchemaRegistry
    SchemaRegistry._schemas = {}
