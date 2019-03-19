from unittest.mock import Mock

import pytest

from lark.lexer import Token

from tartiflette.language.ast import Location
from tartiflette.language.parsers.lark.transformers.converters import (
    UnexpectedASTNode,
    _extract_node_info,
    lark_to_location_node,
)
from tartiflette.language.parsers.lark.transformers.node_transformer import (
    SchemaNode,
)


@pytest.mark.parametrize(
    "children,options,expected",
    [
        (
            [SchemaNode(type="name", value="aName"), Token("value", "aValue")],
            {"types_to_value": ["name", "value"]},
            {"name": "aName", "value": "aValue"},
        ),
        (
            [
                SchemaNode(type="definition", value="firstDefinition"),
                Token("definition", "secondDefinition"),
            ],
            {"types_to_list": {"definition": "definitions"}},
            {
                "definitions": [
                    SchemaNode(type="definition", value="firstDefinition"),
                    Token("definition", "secondDefinition"),
                ]
            },
        ),
        (
            [SchemaNode(type="to_ignore", value=None)],
            {"types_to_ignore": "to_ignore"},
            {},
        ),
        (
            [
                SchemaNode(type="definition", value="firstDefinition"),
                Token("value", "aValue"),
                SchemaNode(type="to_ignore", value=None),
                Token("definition", "secondDefinition"),
                SchemaNode(type="name", value="aName"),
            ],
            {
                "types_to_value": ["name", "value"],
                "types_to_list": {"definition": "definitions"},
                "types_to_ignore": "to_ignore",
            },
            {
                "name": "aName",
                "value": "aValue",
                "definitions": [
                    SchemaNode(type="definition", value="firstDefinition"),
                    Token("definition", "secondDefinition"),
                ],
            },
        ),
    ],
)
def test_extract_node_info(children, options, expected):
    assert _extract_node_info(children, **options) == expected


def test_extract_node_info_unexpected_ast_node():
    with pytest.raises(UnexpectedASTNode):
        _extract_node_info([SchemaNode(type="unexpected", value=None)])


@pytest.mark.parametrize(
    "line,column,end_line,end_column,expected",
    [
        (1, 2, 2, 1, Location(line=1, column=2, line_end=2, column_end=1)),
        (1, 2, 3, 4, Location(line=1, column=2, line_end=3, column_end=4)),
    ],
)
def test_lark_to_location_node(line, column, end_line, end_column, expected):
    node = Mock(
        line=line, column=column, end_line=end_line, end_column=end_column
    )
    assert lark_to_location_node(node) == expected
