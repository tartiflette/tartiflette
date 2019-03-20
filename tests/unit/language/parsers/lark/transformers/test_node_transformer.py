import pytest

from tartiflette.language.parsers.lark.transformers.node_transformer import (
    SchemaNode,
)


def test_schemanode__init__():
    schema_node = SchemaNode(type="aType", value="aValue")
    assert schema_node.type == "aType"
    assert schema_node.value == "aValue"


@pytest.mark.parametrize(
    "schema_node,other,expected",
    [
        (SchemaNode(type="aType", value="aValue"), Ellipsis, False),
        (
            SchemaNode(type="aType", value="aValue"),
            SchemaNode(type="aTypeBis", value="aValue"),
            False,
        ),
        (
            SchemaNode(type="aType", value="aValue"),
            SchemaNode(type="aType", value="aValueBis"),
            False,
        ),
        (
            SchemaNode(type="aType", value="aValue"),
            SchemaNode(type="aType", value="aValue"),
            True,
        ),
    ],
)
def test_schemanode__eq__(schema_node, other, expected):
    assert (schema_node == other) is expected


@pytest.mark.parametrize(
    "schema_node,expected",
    [
        (
            SchemaNode(type="aType", value="aValue"),
            "SchemaNode(type='aType', value='aValue')",
        )
    ],
)
def test_schemanode__repr__(schema_node, expected):
    assert schema_node.__repr__() == expected
