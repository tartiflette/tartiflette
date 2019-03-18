import pytest

from tartiflette.language.ast import (
    ArgumentNode,
    BooleanValueNode,
    DirectiveNode,
    DocumentNode,
    EnumValueNode,
    FieldNode,
    FloatValueNode,
    FragmentDefinitionNode,
    FragmentSpreadNode,
    InlineFragmentNode,
    IntValueNode,
    ListTypeNode,
    ListValueNode,
    Location,
    NamedTypeNode,
    NameNode,
    NonNullTypeNode,
    NullValueNode,
    ObjectFieldNode,
    ObjectValueNode,
    OperationDefinitionNode,
    SelectionSetNode,
    StringValueNode,
    VariableDefinitionNode,
    VariableNode,
)
from tartiflette.language.parsers.libgraphqlparser.transformers import (
    _parse_argument,
    _parse_arguments,
    _parse_boolean_value,
    _parse_definition,
    _parse_definitions,
    _parse_directive,
    _parse_directives,
    _parse_enum_value,
    _parse_field,
    _parse_float_value,
    _parse_fragment_definition,
    _parse_fragment_spread,
    _parse_inline_fragment,
    _parse_int_value,
    _parse_list_value,
    _parse_location,
    _parse_name,
    _parse_named_type,
    _parse_null_value,
    _parse_object_field,
    _parse_object_fields,
    _parse_object_value,
    _parse_operation_definition,
    _parse_selection,
    _parse_selection_set,
    _parse_selections,
    _parse_string_value,
    _parse_type,
    _parse_value,
    _parse_values,
    _parse_variable,
    _parse_variable_definition,
    _parse_variable_definitions,
    document_from_ast_json,
)

_DEFAULT_JSON_AST_LOCATION = {
    "start": {"line": 1, "column": 2},
    "end": {"line": 3, "column": 4},
}

_EXPECTED_DEFAULT_LOCATION = Location(
    line=1, column=2, line_end=3, column_end=4
)


def test_parse_location():
    assert (
        _parse_location(_DEFAULT_JSON_AST_LOCATION)
        == _EXPECTED_DEFAULT_LOCATION
    )


@pytest.mark.parametrize(
    "json_ast,expected",
    [
        (
            {"value": None, "loc": _DEFAULT_JSON_AST_LOCATION},
            NameNode(value=None, location=_EXPECTED_DEFAULT_LOCATION),
        ),
        (
            {"value": "name", "loc": _DEFAULT_JSON_AST_LOCATION},
            NameNode(value="name", location=_EXPECTED_DEFAULT_LOCATION),
        ),
    ],
)
def test_parse_name(json_ast, expected):
    assert _parse_name(json_ast) == expected


@pytest.mark.parametrize(
    "json_ast,expected",
    [
        (
            {
                "name": {"value": None, "loc": _DEFAULT_JSON_AST_LOCATION},
                "loc": _DEFAULT_JSON_AST_LOCATION,
            },
            NamedTypeNode(
                name=NameNode(value=None, location=_EXPECTED_DEFAULT_LOCATION),
                location=_EXPECTED_DEFAULT_LOCATION,
            ),
        ),
        (
            {
                "name": {"value": "name", "loc": _DEFAULT_JSON_AST_LOCATION},
                "loc": _DEFAULT_JSON_AST_LOCATION,
            },
            NamedTypeNode(
                name=NameNode(
                    value="name", location=_EXPECTED_DEFAULT_LOCATION
                ),
                location=_EXPECTED_DEFAULT_LOCATION,
            ),
        ),
    ],
)
def test_parse_named_type(json_ast, expected):
    assert _parse_named_type(json_ast) == expected


@pytest.mark.parametrize(
    "json_ast,expected",
    [
        (
            {
                "name": {"value": None, "loc": _DEFAULT_JSON_AST_LOCATION},
                "loc": _DEFAULT_JSON_AST_LOCATION,
            },
            VariableNode(
                name=NameNode(value=None, location=_EXPECTED_DEFAULT_LOCATION),
                location=_EXPECTED_DEFAULT_LOCATION,
            ),
        ),
        (
            {
                "name": {"value": "name", "loc": _DEFAULT_JSON_AST_LOCATION},
                "loc": _DEFAULT_JSON_AST_LOCATION,
            },
            VariableNode(
                name=NameNode(
                    value="name", location=_EXPECTED_DEFAULT_LOCATION
                ),
                location=_EXPECTED_DEFAULT_LOCATION,
            ),
        ),
    ],
)
def test_parse_variable(json_ast, expected):
    assert _parse_variable(json_ast) == expected


@pytest.mark.parametrize(
    "json_ast,expected",
    [
        (
            {"value": True, "loc": _DEFAULT_JSON_AST_LOCATION},
            BooleanValueNode(value=True, location=_EXPECTED_DEFAULT_LOCATION),
        ),
        (
            {"value": False, "loc": _DEFAULT_JSON_AST_LOCATION},
            BooleanValueNode(value=False, location=_EXPECTED_DEFAULT_LOCATION),
        ),
    ],
)
def test_parse_boolean_value(json_ast, expected):
    assert _parse_boolean_value(json_ast) == expected


@pytest.mark.parametrize(
    "json_ast,expected",
    [
        (
            {"value": None, "loc": _DEFAULT_JSON_AST_LOCATION},
            EnumValueNode(value=None, location=_EXPECTED_DEFAULT_LOCATION),
        ),
        (
            {"value": "ENUM_VALUE", "loc": _DEFAULT_JSON_AST_LOCATION},
            EnumValueNode(
                value="ENUM_VALUE", location=_EXPECTED_DEFAULT_LOCATION
            ),
        ),
    ],
)
def test_parse_enum_value(json_ast, expected):
    assert _parse_enum_value(json_ast) == expected


@pytest.mark.parametrize(
    "json_ast,expected",
    [
        (
            {"value": 1.1, "loc": _DEFAULT_JSON_AST_LOCATION},
            FloatValueNode(value=1.1, location=_EXPECTED_DEFAULT_LOCATION),
        ),
        (
            {"value": "1.1", "loc": _DEFAULT_JSON_AST_LOCATION},
            FloatValueNode(value=1.1, location=_EXPECTED_DEFAULT_LOCATION),
        ),
        (
            {"value": -1.1, "loc": _DEFAULT_JSON_AST_LOCATION},
            FloatValueNode(value=-1.1, location=_EXPECTED_DEFAULT_LOCATION),
        ),
        (
            {"value": "-1.1", "loc": _DEFAULT_JSON_AST_LOCATION},
            FloatValueNode(value=-1.1, location=_EXPECTED_DEFAULT_LOCATION),
        ),
        (
            {"value": "0.123e2", "loc": _DEFAULT_JSON_AST_LOCATION},
            FloatValueNode(value=12.3, location=_EXPECTED_DEFAULT_LOCATION),
        ),
        (
            {"value": "-0.123e2", "loc": _DEFAULT_JSON_AST_LOCATION},
            FloatValueNode(value=-12.3, location=_EXPECTED_DEFAULT_LOCATION),
        ),
    ],
)
def test_parse_float_value(json_ast, expected):
    assert _parse_float_value(json_ast) == expected


@pytest.mark.parametrize(
    "json_ast,expected",
    [
        (
            {"value": "1", "loc": _DEFAULT_JSON_AST_LOCATION},
            IntValueNode(value=1, location=_EXPECTED_DEFAULT_LOCATION),
        ),
        (
            {"value": 1, "loc": _DEFAULT_JSON_AST_LOCATION},
            IntValueNode(value=1, location=_EXPECTED_DEFAULT_LOCATION),
        ),
        (
            {"value": "-0", "loc": _DEFAULT_JSON_AST_LOCATION},
            IntValueNode(value=0, location=_EXPECTED_DEFAULT_LOCATION),
        ),
        (
            {"value": "10", "loc": _DEFAULT_JSON_AST_LOCATION},
            IntValueNode(value=10, location=_EXPECTED_DEFAULT_LOCATION),
        ),
        (
            {"value": 10, "loc": _DEFAULT_JSON_AST_LOCATION},
            IntValueNode(value=10, location=_EXPECTED_DEFAULT_LOCATION),
        ),
        (
            {"value": "-10", "loc": _DEFAULT_JSON_AST_LOCATION},
            IntValueNode(value=-10, location=_EXPECTED_DEFAULT_LOCATION),
        ),
    ],
)
def test_parse_int_value(json_ast, expected):
    assert _parse_int_value(json_ast) == expected


@pytest.mark.parametrize(
    "json_ast,expected",
    [
        (None, []),
        ([], []),
        (
            [
                {
                    "kind": "BooleanValue",
                    "value": False,
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                {
                    "kind": "EnumValue",
                    "value": "ENUM_VALUE",
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                {
                    "kind": "FloatValue",
                    "value": 1.1,
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                {
                    "kind": "IntValue",
                    "value": 1,
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                {
                    "kind": "ListValue",
                    "values": [
                        {
                            "kind": "BooleanValue",
                            "value": False,
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        }
                    ],
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                {"kind": "NullValue", "loc": _DEFAULT_JSON_AST_LOCATION},
                {
                    "kind": "ObjectValue",
                    "fields": [
                        {
                            "name": {
                                "value": "booleanField",
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            },
                            "value": {
                                "kind": "BooleanValue",
                                "value": False,
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            },
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        }
                    ],
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                {
                    "kind": "StringValue",
                    "value": "StringValue",
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                {
                    "kind": "Variable",
                    "name": {
                        "value": "name",
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
            ],
            [
                BooleanValueNode(
                    value=False, location=_EXPECTED_DEFAULT_LOCATION
                ),
                EnumValueNode(
                    value="ENUM_VALUE", location=_EXPECTED_DEFAULT_LOCATION
                ),
                FloatValueNode(value=1.1, location=_EXPECTED_DEFAULT_LOCATION),
                IntValueNode(value=1, location=_EXPECTED_DEFAULT_LOCATION),
                ListValueNode(
                    values=[
                        BooleanValueNode(
                            value=False, location=_EXPECTED_DEFAULT_LOCATION
                        )
                    ],
                    location=_EXPECTED_DEFAULT_LOCATION,
                ),
                NullValueNode(location=_EXPECTED_DEFAULT_LOCATION),
                ObjectValueNode(
                    fields=[
                        ObjectFieldNode(
                            name=NameNode(
                                value="booleanField",
                                location=_EXPECTED_DEFAULT_LOCATION,
                            ),
                            value=BooleanValueNode(
                                value=False,
                                location=_EXPECTED_DEFAULT_LOCATION,
                            ),
                            location=_EXPECTED_DEFAULT_LOCATION,
                        )
                    ],
                    location=_EXPECTED_DEFAULT_LOCATION,
                ),
                StringValueNode(
                    value="StringValue", location=_EXPECTED_DEFAULT_LOCATION
                ),
                VariableNode(
                    name=NameNode(
                        value="name", location=_EXPECTED_DEFAULT_LOCATION
                    ),
                    location=_EXPECTED_DEFAULT_LOCATION,
                ),
            ],
        ),
    ],
)
def test_parse_values(json_ast, expected):
    assert _parse_values(json_ast) == expected


@pytest.mark.parametrize(
    "json_ast,expected",
    [
        (
            {"values": None, "loc": _DEFAULT_JSON_AST_LOCATION},
            ListValueNode(values=[], location=_EXPECTED_DEFAULT_LOCATION),
        ),
        (
            {"values": [], "loc": _DEFAULT_JSON_AST_LOCATION},
            ListValueNode(values=[], location=_EXPECTED_DEFAULT_LOCATION),
        ),
        (
            {
                "values": [
                    {
                        "kind": "BooleanValue",
                        "value": False,
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    {
                        "kind": "EnumValue",
                        "value": "ENUM_VALUE",
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    {
                        "kind": "FloatValue",
                        "value": 1.1,
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    {
                        "kind": "IntValue",
                        "value": 1,
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    {
                        "kind": "ListValue",
                        "values": [
                            {
                                "kind": "BooleanValue",
                                "value": False,
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            }
                        ],
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    {"kind": "NullValue", "loc": _DEFAULT_JSON_AST_LOCATION},
                    {
                        "kind": "ObjectValue",
                        "fields": [
                            {
                                "name": {
                                    "value": "booleanField",
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                },
                                "value": {
                                    "kind": "BooleanValue",
                                    "value": False,
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                },
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            }
                        ],
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    {
                        "kind": "StringValue",
                        "value": "StringValue",
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    {
                        "kind": "Variable",
                        "name": {
                            "value": "name",
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                ],
                "loc": _DEFAULT_JSON_AST_LOCATION,
            },
            ListValueNode(
                values=[
                    BooleanValueNode(
                        value=False, location=_EXPECTED_DEFAULT_LOCATION
                    ),
                    EnumValueNode(
                        value="ENUM_VALUE", location=_EXPECTED_DEFAULT_LOCATION
                    ),
                    FloatValueNode(
                        value=1.1, location=_EXPECTED_DEFAULT_LOCATION
                    ),
                    IntValueNode(value=1, location=_EXPECTED_DEFAULT_LOCATION),
                    ListValueNode(
                        values=[
                            BooleanValueNode(
                                value=False,
                                location=_EXPECTED_DEFAULT_LOCATION,
                            )
                        ],
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                    NullValueNode(location=_EXPECTED_DEFAULT_LOCATION),
                    ObjectValueNode(
                        fields=[
                            ObjectFieldNode(
                                name=NameNode(
                                    value="booleanField",
                                    location=_EXPECTED_DEFAULT_LOCATION,
                                ),
                                value=BooleanValueNode(
                                    value=False,
                                    location=_EXPECTED_DEFAULT_LOCATION,
                                ),
                                location=_EXPECTED_DEFAULT_LOCATION,
                            )
                        ],
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                    StringValueNode(
                        value="StringValue",
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                    VariableNode(
                        name=NameNode(
                            value="name", location=_EXPECTED_DEFAULT_LOCATION
                        ),
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                ],
                location=_EXPECTED_DEFAULT_LOCATION,
            ),
        ),
    ],
)
def test_parse_list_value(json_ast, expected):
    assert _parse_list_value(json_ast) == expected


@pytest.mark.parametrize(
    "json_ast,expected",
    [
        (
            {"loc": _DEFAULT_JSON_AST_LOCATION},
            NullValueNode(location=_EXPECTED_DEFAULT_LOCATION),
        )
    ],
)
def test_parse_null_value(json_ast, expected):
    assert _parse_null_value(json_ast) == expected


@pytest.mark.parametrize(
    "json_ast,expected",
    [
        (
            {
                "name": {"value": "field", "loc": _DEFAULT_JSON_AST_LOCATION},
                "value": {
                    "kind": "StringValue",
                    "value": "StringValue",
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                "loc": _DEFAULT_JSON_AST_LOCATION,
            },
            ObjectFieldNode(
                name=NameNode(
                    value="field", location=_EXPECTED_DEFAULT_LOCATION
                ),
                value=StringValueNode(
                    value="StringValue", location=_EXPECTED_DEFAULT_LOCATION
                ),
                location=_EXPECTED_DEFAULT_LOCATION,
            ),
        ),
        (
            {
                "name": {"value": "field", "loc": _DEFAULT_JSON_AST_LOCATION},
                "value": {
                    "kind": "BooleanValue",
                    "value": True,
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                "loc": _DEFAULT_JSON_AST_LOCATION,
            },
            ObjectFieldNode(
                name=NameNode(
                    value="field", location=_EXPECTED_DEFAULT_LOCATION
                ),
                value=BooleanValueNode(
                    value=True, location=_EXPECTED_DEFAULT_LOCATION
                ),
                location=_EXPECTED_DEFAULT_LOCATION,
            ),
        ),
    ],
)
def test_parse_object_field(json_ast, expected):
    assert _parse_object_field(json_ast) == expected


@pytest.mark.parametrize(
    "json_ast,expected",
    [
        (None, []),
        ([], []),
        (
            [
                {
                    "name": {
                        "value": "booleanField",
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    "value": {
                        "kind": "BooleanValue",
                        "value": False,
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                {
                    "name": {
                        "value": "enumField",
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    "value": {
                        "kind": "EnumValue",
                        "value": "ENUM_VALUE",
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                {
                    "name": {
                        "value": "floatField",
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    "value": {
                        "kind": "FloatValue",
                        "value": 1.1,
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                {
                    "name": {
                        "value": "intField",
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    "value": {
                        "kind": "IntValue",
                        "value": 1,
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                {
                    "name": {
                        "value": "listField",
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    "value": {
                        "kind": "ListValue",
                        "values": [
                            {
                                "kind": "BooleanValue",
                                "value": False,
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            }
                        ],
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                {
                    "name": {
                        "value": "nullField",
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    "value": {
                        "kind": "NullValue",
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                {
                    "name": {
                        "value": "objectField",
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    "value": {
                        "kind": "ObjectValue",
                        "fields": [
                            {
                                "name": {
                                    "value": "booleanField",
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                },
                                "value": {
                                    "kind": "BooleanValue",
                                    "value": False,
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                },
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            }
                        ],
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                {
                    "name": {
                        "value": "stringField",
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    "value": {
                        "kind": "StringValue",
                        "value": "StringValue",
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                {
                    "name": {
                        "value": "variableField",
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    "value": {
                        "kind": "Variable",
                        "name": {
                            "value": "name",
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
            ],
            [
                ObjectFieldNode(
                    name=NameNode(
                        value="booleanField",
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                    value=BooleanValueNode(
                        value=False, location=_EXPECTED_DEFAULT_LOCATION
                    ),
                    location=_EXPECTED_DEFAULT_LOCATION,
                ),
                ObjectFieldNode(
                    name=NameNode(
                        value="enumField", location=_EXPECTED_DEFAULT_LOCATION
                    ),
                    value=EnumValueNode(
                        value="ENUM_VALUE", location=_EXPECTED_DEFAULT_LOCATION
                    ),
                    location=_EXPECTED_DEFAULT_LOCATION,
                ),
                ObjectFieldNode(
                    name=NameNode(
                        value="floatField", location=_EXPECTED_DEFAULT_LOCATION
                    ),
                    value=FloatValueNode(
                        value=1.1, location=_EXPECTED_DEFAULT_LOCATION
                    ),
                    location=_EXPECTED_DEFAULT_LOCATION,
                ),
                ObjectFieldNode(
                    name=NameNode(
                        value="intField", location=_EXPECTED_DEFAULT_LOCATION
                    ),
                    value=IntValueNode(
                        value=1, location=_EXPECTED_DEFAULT_LOCATION
                    ),
                    location=_EXPECTED_DEFAULT_LOCATION,
                ),
                ObjectFieldNode(
                    name=NameNode(
                        value="listField", location=_EXPECTED_DEFAULT_LOCATION
                    ),
                    value=ListValueNode(
                        values=[
                            BooleanValueNode(
                                value=False,
                                location=_EXPECTED_DEFAULT_LOCATION,
                            )
                        ],
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                    location=_EXPECTED_DEFAULT_LOCATION,
                ),
                ObjectFieldNode(
                    name=NameNode(
                        value="nullField", location=_EXPECTED_DEFAULT_LOCATION
                    ),
                    value=NullValueNode(location=_EXPECTED_DEFAULT_LOCATION),
                    location=_EXPECTED_DEFAULT_LOCATION,
                ),
                ObjectFieldNode(
                    name=NameNode(
                        value="objectField",
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                    value=ObjectValueNode(
                        fields=[
                            ObjectFieldNode(
                                name=NameNode(
                                    value="booleanField",
                                    location=_EXPECTED_DEFAULT_LOCATION,
                                ),
                                value=BooleanValueNode(
                                    value=False,
                                    location=_EXPECTED_DEFAULT_LOCATION,
                                ),
                                location=_EXPECTED_DEFAULT_LOCATION,
                            )
                        ],
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                    location=_EXPECTED_DEFAULT_LOCATION,
                ),
                ObjectFieldNode(
                    name=NameNode(
                        value="stringField",
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                    value=StringValueNode(
                        value="StringValue",
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                    location=_EXPECTED_DEFAULT_LOCATION,
                ),
                ObjectFieldNode(
                    name=NameNode(
                        value="variableField",
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                    value=VariableNode(
                        name=NameNode(
                            value="name", location=_EXPECTED_DEFAULT_LOCATION
                        ),
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                    location=_EXPECTED_DEFAULT_LOCATION,
                ),
            ],
        ),
    ],
)
def test_parse_object_fields(json_ast, expected):
    assert _parse_object_fields(json_ast) == expected


@pytest.mark.parametrize(
    "json_ast,expected",
    [
        (
            {"fields": None, "loc": _DEFAULT_JSON_AST_LOCATION},
            ObjectValueNode(fields=[], location=_EXPECTED_DEFAULT_LOCATION),
        ),
        (
            {"fields": [], "loc": _DEFAULT_JSON_AST_LOCATION},
            ObjectValueNode(fields=[], location=_EXPECTED_DEFAULT_LOCATION),
        ),
        (
            {
                "fields": [
                    {
                        "name": {
                            "value": "booleanField",
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "value": {
                            "kind": "BooleanValue",
                            "value": False,
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    {
                        "name": {
                            "value": "enumField",
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "value": {
                            "kind": "EnumValue",
                            "value": "ENUM_VALUE",
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    {
                        "name": {
                            "value": "floatField",
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "value": {
                            "kind": "FloatValue",
                            "value": 1.1,
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    {
                        "name": {
                            "value": "intField",
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "value": {
                            "kind": "IntValue",
                            "value": 1,
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    {
                        "name": {
                            "value": "listField",
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "value": {
                            "kind": "ListValue",
                            "values": [
                                {
                                    "kind": "BooleanValue",
                                    "value": False,
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                }
                            ],
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    {
                        "name": {
                            "value": "nullField",
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "value": {
                            "kind": "NullValue",
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    {
                        "name": {
                            "value": "objectField",
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "value": {
                            "kind": "ObjectValue",
                            "fields": [
                                {
                                    "name": {
                                        "value": "booleanField",
                                        "loc": _DEFAULT_JSON_AST_LOCATION,
                                    },
                                    "value": {
                                        "kind": "BooleanValue",
                                        "value": False,
                                        "loc": _DEFAULT_JSON_AST_LOCATION,
                                    },
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                }
                            ],
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    {
                        "name": {
                            "value": "stringField",
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "value": {
                            "kind": "StringValue",
                            "value": "StringValue",
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    {
                        "name": {
                            "value": "variableField",
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "value": {
                            "kind": "Variable",
                            "name": {
                                "value": "name",
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            },
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                ],
                "loc": _DEFAULT_JSON_AST_LOCATION,
            },
            ObjectValueNode(
                fields=[
                    ObjectFieldNode(
                        name=NameNode(
                            value="booleanField",
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        value=BooleanValueNode(
                            value=False, location=_EXPECTED_DEFAULT_LOCATION
                        ),
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                    ObjectFieldNode(
                        name=NameNode(
                            value="enumField",
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        value=EnumValueNode(
                            value="ENUM_VALUE",
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                    ObjectFieldNode(
                        name=NameNode(
                            value="floatField",
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        value=FloatValueNode(
                            value=1.1, location=_EXPECTED_DEFAULT_LOCATION
                        ),
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                    ObjectFieldNode(
                        name=NameNode(
                            value="intField",
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        value=IntValueNode(
                            value=1, location=_EXPECTED_DEFAULT_LOCATION
                        ),
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                    ObjectFieldNode(
                        name=NameNode(
                            value="listField",
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        value=ListValueNode(
                            values=[
                                BooleanValueNode(
                                    value=False,
                                    location=_EXPECTED_DEFAULT_LOCATION,
                                )
                            ],
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                    ObjectFieldNode(
                        name=NameNode(
                            value="nullField",
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        value=NullValueNode(
                            location=_EXPECTED_DEFAULT_LOCATION
                        ),
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                    ObjectFieldNode(
                        name=NameNode(
                            value="objectField",
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        value=ObjectValueNode(
                            fields=[
                                ObjectFieldNode(
                                    name=NameNode(
                                        value="booleanField",
                                        location=_EXPECTED_DEFAULT_LOCATION,
                                    ),
                                    value=BooleanValueNode(
                                        value=False,
                                        location=_EXPECTED_DEFAULT_LOCATION,
                                    ),
                                    location=_EXPECTED_DEFAULT_LOCATION,
                                )
                            ],
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                    ObjectFieldNode(
                        name=NameNode(
                            value="stringField",
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        value=StringValueNode(
                            value="StringValue",
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                    ObjectFieldNode(
                        name=NameNode(
                            value="variableField",
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        value=VariableNode(
                            name=NameNode(
                                value="name",
                                location=_EXPECTED_DEFAULT_LOCATION,
                            ),
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                ],
                location=_EXPECTED_DEFAULT_LOCATION,
            ),
        ),
    ],
)
def test_parse_object_value(json_ast, expected):
    assert _parse_object_value(json_ast) == expected


@pytest.mark.parametrize(
    "json_ast,expected",
    [
        (
            {"value": None, "loc": _DEFAULT_JSON_AST_LOCATION},
            StringValueNode(value=None, location=_EXPECTED_DEFAULT_LOCATION),
        ),
        (
            {"value": "", "loc": _DEFAULT_JSON_AST_LOCATION},
            StringValueNode(value="", location=_EXPECTED_DEFAULT_LOCATION),
        ),
        (
            {"value": "StringValue", "loc": _DEFAULT_JSON_AST_LOCATION},
            StringValueNode(
                value="StringValue", location=_EXPECTED_DEFAULT_LOCATION
            ),
        ),
    ],
)
def test_parse_string_value(json_ast, expected):
    assert _parse_string_value(json_ast) == expected


@pytest.mark.parametrize(
    "json_ast,expected",
    [
        (None, None),
        ({}, None),
        (
            {
                "kind": "BooleanValue",
                "value": False,
                "loc": _DEFAULT_JSON_AST_LOCATION,
            },
            BooleanValueNode(value=False, location=_EXPECTED_DEFAULT_LOCATION),
        ),
        (
            {
                "kind": "EnumValue",
                "value": "ENUM_VALUE",
                "loc": _DEFAULT_JSON_AST_LOCATION,
            },
            EnumValueNode(
                value="ENUM_VALUE", location=_EXPECTED_DEFAULT_LOCATION
            ),
        ),
        (
            {
                "kind": "FloatValue",
                "value": 1.1,
                "loc": _DEFAULT_JSON_AST_LOCATION,
            },
            FloatValueNode(value=1.1, location=_EXPECTED_DEFAULT_LOCATION),
        ),
        (
            {
                "kind": "IntValue",
                "value": 1,
                "loc": _DEFAULT_JSON_AST_LOCATION,
            },
            IntValueNode(value=1, location=_EXPECTED_DEFAULT_LOCATION),
        ),
        (
            {
                "kind": "ListValue",
                "values": [
                    {
                        "kind": "BooleanValue",
                        "value": False,
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    }
                ],
                "loc": _DEFAULT_JSON_AST_LOCATION,
            },
            ListValueNode(
                values=[
                    BooleanValueNode(
                        value=False, location=_EXPECTED_DEFAULT_LOCATION
                    )
                ],
                location=_EXPECTED_DEFAULT_LOCATION,
            ),
        ),
        (
            {"kind": "NullValue", "loc": _DEFAULT_JSON_AST_LOCATION},
            NullValueNode(location=_EXPECTED_DEFAULT_LOCATION),
        ),
        (
            {
                "kind": "ObjectValue",
                "fields": [
                    {
                        "name": {
                            "value": "booleanField",
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "value": {
                            "kind": "BooleanValue",
                            "value": False,
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    }
                ],
                "loc": _DEFAULT_JSON_AST_LOCATION,
            },
            ObjectValueNode(
                fields=[
                    ObjectFieldNode(
                        name=NameNode(
                            value="booleanField",
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        value=BooleanValueNode(
                            value=False, location=_EXPECTED_DEFAULT_LOCATION
                        ),
                        location=_EXPECTED_DEFAULT_LOCATION,
                    )
                ],
                location=_EXPECTED_DEFAULT_LOCATION,
            ),
        ),
        (
            {
                "kind": "StringValue",
                "value": "StringValue",
                "loc": _DEFAULT_JSON_AST_LOCATION,
            },
            StringValueNode(
                value="StringValue", location=_EXPECTED_DEFAULT_LOCATION
            ),
        ),
        (
            {
                "kind": "Variable",
                "name": {"value": "name", "loc": _DEFAULT_JSON_AST_LOCATION},
                "loc": _DEFAULT_JSON_AST_LOCATION,
            },
            VariableNode(
                name=NameNode(
                    value="name", location=_EXPECTED_DEFAULT_LOCATION
                ),
                location=_EXPECTED_DEFAULT_LOCATION,
            ),
        ),
    ],
)
def test_parse_value(json_ast, expected):
    assert _parse_value(json_ast) == expected


@pytest.mark.parametrize(
    "json_ast,expected",
    [
        (
            {
                "name": {
                    "value": "argName",
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                "value": {
                    "kind": "BooleanValue",
                    "value": True,
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                "loc": _DEFAULT_JSON_AST_LOCATION,
            },
            ArgumentNode(
                name=NameNode(
                    value="argName", location=_EXPECTED_DEFAULT_LOCATION
                ),
                value=BooleanValueNode(
                    value=True, location=_EXPECTED_DEFAULT_LOCATION
                ),
                location=_EXPECTED_DEFAULT_LOCATION,
            ),
        )
    ],
)
def test_parse_argument(json_ast, expected):
    assert _parse_argument(json_ast) == expected


@pytest.mark.parametrize(
    "json_ast,expected",
    [
        (None, []),
        ([], []),
        (
            [
                {
                    "name": {
                        "value": "booleanArg",
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    "value": {
                        "kind": "BooleanValue",
                        "value": True,
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                {
                    "name": {
                        "value": "nullArg",
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    "value": {
                        "kind": "NullValue",
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
            ],
            [
                ArgumentNode(
                    name=NameNode(
                        value="booleanArg", location=_EXPECTED_DEFAULT_LOCATION
                    ),
                    value=BooleanValueNode(
                        value=True, location=_EXPECTED_DEFAULT_LOCATION
                    ),
                    location=_EXPECTED_DEFAULT_LOCATION,
                ),
                ArgumentNode(
                    name=NameNode(
                        value="nullArg", location=_EXPECTED_DEFAULT_LOCATION
                    ),
                    value=NullValueNode(location=_EXPECTED_DEFAULT_LOCATION),
                    location=_EXPECTED_DEFAULT_LOCATION,
                ),
            ],
        ),
    ],
)
def test_parse_arguments(json_ast, expected):
    assert _parse_arguments(json_ast) == expected


@pytest.mark.parametrize(
    "json_ast,expected",
    [
        (
            {
                "name": {
                    "value": "directiveName",
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                "arguments": [
                    {
                        "name": {
                            "value": "nullArg",
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "value": {
                            "kind": "NullValue",
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    }
                ],
                "loc": _DEFAULT_JSON_AST_LOCATION,
            },
            DirectiveNode(
                name=NameNode(
                    value="directiveName", location=_EXPECTED_DEFAULT_LOCATION
                ),
                arguments=[
                    ArgumentNode(
                        name=NameNode(
                            value="nullArg",
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        value=NullValueNode(
                            location=_EXPECTED_DEFAULT_LOCATION
                        ),
                        location=_EXPECTED_DEFAULT_LOCATION,
                    )
                ],
                location=_EXPECTED_DEFAULT_LOCATION,
            ),
        )
    ],
)
def test_parse_directive(json_ast, expected):
    assert _parse_directive(json_ast) == expected


@pytest.mark.parametrize(
    "json_ast,expected",
    [
        (None, []),
        ([], []),
        (
            [
                {
                    "name": {
                        "value": "firstDirective",
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    "arguments": [
                        {
                            "name": {
                                "value": "nullArg",
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            },
                            "value": {
                                "kind": "NullValue",
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            },
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        }
                    ],
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                {
                    "name": {
                        "value": "secondDirective",
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    "arguments": None,
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
            ],
            [
                DirectiveNode(
                    name=NameNode(
                        value="firstDirective",
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                    arguments=[
                        ArgumentNode(
                            name=NameNode(
                                value="nullArg",
                                location=_EXPECTED_DEFAULT_LOCATION,
                            ),
                            value=NullValueNode(
                                location=_EXPECTED_DEFAULT_LOCATION
                            ),
                            location=_EXPECTED_DEFAULT_LOCATION,
                        )
                    ],
                    location=_EXPECTED_DEFAULT_LOCATION,
                ),
                DirectiveNode(
                    name=NameNode(
                        value="secondDirective",
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                    arguments=[],
                    location=_EXPECTED_DEFAULT_LOCATION,
                ),
            ],
        ),
    ],
)
def test_parse_directives(json_ast, expected):
    assert _parse_directives(json_ast) == expected


@pytest.mark.parametrize(
    "json_ast,expected",
    [
        (
            {
                "alias": {
                    "value": "fieldAlias",
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                "name": {
                    "value": "fieldName",
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                "arguments": [
                    {
                        "name": {
                            "value": "nullArg",
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "value": {
                            "kind": "NullValue",
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    }
                ],
                "directives": [
                    {
                        "name": {
                            "value": "firstDirective",
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "arguments": [
                            {
                                "name": {
                                    "value": "nullArg",
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                },
                                "value": {
                                    "kind": "NullValue",
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                },
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            }
                        ],
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    {
                        "name": {
                            "value": "secondDirective",
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "arguments": None,
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                ],
                "selectionSet": {
                    "selections": [
                        {
                            "kind": "FragmentSpread",
                            "name": {
                                "value": "spreadedFragment",
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            },
                            "directives": None,
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        }
                    ],
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                "loc": _DEFAULT_JSON_AST_LOCATION,
            },
            FieldNode(
                alias=NameNode(
                    value="fieldAlias", location=_EXPECTED_DEFAULT_LOCATION
                ),
                name=NameNode(
                    value="fieldName", location=_EXPECTED_DEFAULT_LOCATION
                ),
                arguments=[
                    ArgumentNode(
                        name=NameNode(
                            value="nullArg",
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        value=NullValueNode(
                            location=_EXPECTED_DEFAULT_LOCATION
                        ),
                        location=_EXPECTED_DEFAULT_LOCATION,
                    )
                ],
                directives=[
                    DirectiveNode(
                        name=NameNode(
                            value="firstDirective",
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        arguments=[
                            ArgumentNode(
                                name=NameNode(
                                    value="nullArg",
                                    location=_EXPECTED_DEFAULT_LOCATION,
                                ),
                                value=NullValueNode(
                                    location=_EXPECTED_DEFAULT_LOCATION
                                ),
                                location=_EXPECTED_DEFAULT_LOCATION,
                            )
                        ],
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                    DirectiveNode(
                        name=NameNode(
                            value="secondDirective",
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        arguments=[],
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                ],
                selection_set=SelectionSetNode(
                    selections=[
                        FragmentSpreadNode(
                            name=NameNode(
                                value="spreadedFragment",
                                location=_EXPECTED_DEFAULT_LOCATION,
                            ),
                            directives=[],
                            location=_EXPECTED_DEFAULT_LOCATION,
                        )
                    ],
                    location=_EXPECTED_DEFAULT_LOCATION,
                ),
                location=_EXPECTED_DEFAULT_LOCATION,
            ),
        ),
        (
            {
                "alias": None,
                "name": {
                    "value": "fieldName",
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                "arguments": None,
                "directives": None,
                "selectionSet": None,
                "loc": _DEFAULT_JSON_AST_LOCATION,
            },
            FieldNode(
                alias=None,
                name=NameNode(
                    value="fieldName", location=_EXPECTED_DEFAULT_LOCATION
                ),
                arguments=[],
                directives=[],
                selection_set=None,
                location=_EXPECTED_DEFAULT_LOCATION,
            ),
        ),
    ],
)
def test_parse_field(json_ast, expected):
    assert _parse_field(json_ast) == expected


@pytest.mark.parametrize(
    "json_ast,expected",
    [
        (
            {
                "name": {
                    "value": "spreadedFragment",
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                "directives": [
                    {
                        "name": {
                            "value": "firstDirective",
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "arguments": [
                            {
                                "name": {
                                    "value": "nullArg",
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                },
                                "value": {
                                    "kind": "NullValue",
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                },
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            }
                        ],
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    {
                        "name": {
                            "value": "secondDirective",
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "arguments": None,
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                ],
                "loc": _DEFAULT_JSON_AST_LOCATION,
            },
            FragmentSpreadNode(
                name=NameNode(
                    value="spreadedFragment",
                    location=_EXPECTED_DEFAULT_LOCATION,
                ),
                directives=[
                    DirectiveNode(
                        name=NameNode(
                            value="firstDirective",
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        arguments=[
                            ArgumentNode(
                                name=NameNode(
                                    value="nullArg",
                                    location=_EXPECTED_DEFAULT_LOCATION,
                                ),
                                value=NullValueNode(
                                    location=_EXPECTED_DEFAULT_LOCATION
                                ),
                                location=_EXPECTED_DEFAULT_LOCATION,
                            )
                        ],
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                    DirectiveNode(
                        name=NameNode(
                            value="secondDirective",
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        arguments=[],
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                ],
                location=_EXPECTED_DEFAULT_LOCATION,
            ),
        ),
        (
            {
                "name": {
                    "value": "spreadedFragment",
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                "directives": None,
                "loc": _DEFAULT_JSON_AST_LOCATION,
            },
            FragmentSpreadNode(
                name=NameNode(
                    value="spreadedFragment",
                    location=_EXPECTED_DEFAULT_LOCATION,
                ),
                directives=[],
                location=_EXPECTED_DEFAULT_LOCATION,
            ),
        ),
    ],
)
def test_parse_fragment_spread(json_ast, expected):
    assert _parse_fragment_spread(json_ast) == expected


@pytest.mark.parametrize(
    "json_ast,expected",
    [
        (
            {
                "directives": [
                    {
                        "name": {
                            "value": "firstDirective",
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "arguments": [
                            {
                                "name": {
                                    "value": "nullArg",
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                },
                                "value": {
                                    "kind": "NullValue",
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                },
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            }
                        ],
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    {
                        "name": {
                            "value": "secondDirective",
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "arguments": None,
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                ],
                "typeCondition": {
                    "name": {
                        "value": "MyType",
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                "selectionSet": {
                    "selections": [
                        {
                            "kind": "Field",
                            "alias": None,
                            "name": {
                                "value": "myTypeField",
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            },
                            "arguments": None,
                            "directives": None,
                            "selectionSet": None,
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        }
                    ],
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                "loc": _DEFAULT_JSON_AST_LOCATION,
            },
            InlineFragmentNode(
                directives=[
                    DirectiveNode(
                        name=NameNode(
                            value="firstDirective",
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        arguments=[
                            ArgumentNode(
                                name=NameNode(
                                    value="nullArg",
                                    location=_EXPECTED_DEFAULT_LOCATION,
                                ),
                                value=NullValueNode(
                                    location=_EXPECTED_DEFAULT_LOCATION
                                ),
                                location=_EXPECTED_DEFAULT_LOCATION,
                            )
                        ],
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                    DirectiveNode(
                        name=NameNode(
                            value="secondDirective",
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        arguments=[],
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                ],
                type_condition=NamedTypeNode(
                    name=NameNode(
                        value="MyType", location=_EXPECTED_DEFAULT_LOCATION
                    ),
                    location=_EXPECTED_DEFAULT_LOCATION,
                ),
                selection_set=SelectionSetNode(
                    selections=[
                        FieldNode(
                            alias=None,
                            name=NameNode(
                                value="myTypeField",
                                location=_EXPECTED_DEFAULT_LOCATION,
                            ),
                            arguments=[],
                            directives=[],
                            selection_set=None,
                            location=_EXPECTED_DEFAULT_LOCATION,
                        )
                    ],
                    location=_EXPECTED_DEFAULT_LOCATION,
                ),
                location=_EXPECTED_DEFAULT_LOCATION,
            ),
        ),
        (
            {
                "directives": None,
                "typeCondition": None,
                "selectionSet": None,
                "loc": _DEFAULT_JSON_AST_LOCATION,
            },
            InlineFragmentNode(
                directives=[],
                type_condition=None,
                selection_set=None,
                location=_EXPECTED_DEFAULT_LOCATION,
            ),
        ),
    ],
)
def test_parse_inline_fragment(json_ast, expected):
    assert _parse_inline_fragment(json_ast) == expected


@pytest.mark.parametrize(
    "json_ast,expected",
    [
        (
            {
                "kind": "Field",
                "alias": {
                    "value": "fieldAlias",
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                "name": {
                    "value": "fieldName",
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                "arguments": [
                    {
                        "name": {
                            "value": "nullArg",
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "value": {
                            "kind": "NullValue",
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    }
                ],
                "directives": [
                    {
                        "name": {
                            "value": "firstDirective",
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "arguments": [
                            {
                                "name": {
                                    "value": "nullArg",
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                },
                                "value": {
                                    "kind": "NullValue",
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                },
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            }
                        ],
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    {
                        "name": {
                            "value": "secondDirective",
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "arguments": None,
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                ],
                "selectionSet": {
                    "selections": [
                        {
                            "kind": "FragmentSpread",
                            "name": {
                                "value": "spreadedFragment",
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            },
                            "directives": None,
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        }
                    ],
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                "loc": _DEFAULT_JSON_AST_LOCATION,
            },
            FieldNode(
                alias=NameNode(
                    value="fieldAlias", location=_EXPECTED_DEFAULT_LOCATION
                ),
                name=NameNode(
                    value="fieldName", location=_EXPECTED_DEFAULT_LOCATION
                ),
                arguments=[
                    ArgumentNode(
                        name=NameNode(
                            value="nullArg",
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        value=NullValueNode(
                            location=_EXPECTED_DEFAULT_LOCATION
                        ),
                        location=_EXPECTED_DEFAULT_LOCATION,
                    )
                ],
                directives=[
                    DirectiveNode(
                        name=NameNode(
                            value="firstDirective",
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        arguments=[
                            ArgumentNode(
                                name=NameNode(
                                    value="nullArg",
                                    location=_EXPECTED_DEFAULT_LOCATION,
                                ),
                                value=NullValueNode(
                                    location=_EXPECTED_DEFAULT_LOCATION
                                ),
                                location=_EXPECTED_DEFAULT_LOCATION,
                            )
                        ],
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                    DirectiveNode(
                        name=NameNode(
                            value="secondDirective",
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        arguments=[],
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                ],
                selection_set=SelectionSetNode(
                    selections=[
                        FragmentSpreadNode(
                            name=NameNode(
                                value="spreadedFragment",
                                location=_EXPECTED_DEFAULT_LOCATION,
                            ),
                            directives=[],
                            location=_EXPECTED_DEFAULT_LOCATION,
                        )
                    ],
                    location=_EXPECTED_DEFAULT_LOCATION,
                ),
                location=_EXPECTED_DEFAULT_LOCATION,
            ),
        ),
        (
            {
                "kind": "FragmentSpread",
                "name": {
                    "value": "spreadedFragment",
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                "directives": [
                    {
                        "name": {
                            "value": "firstDirective",
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "arguments": [
                            {
                                "name": {
                                    "value": "nullArg",
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                },
                                "value": {
                                    "kind": "NullValue",
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                },
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            }
                        ],
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    {
                        "name": {
                            "value": "secondDirective",
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "arguments": None,
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                ],
                "loc": _DEFAULT_JSON_AST_LOCATION,
            },
            FragmentSpreadNode(
                name=NameNode(
                    value="spreadedFragment",
                    location=_EXPECTED_DEFAULT_LOCATION,
                ),
                directives=[
                    DirectiveNode(
                        name=NameNode(
                            value="firstDirective",
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        arguments=[
                            ArgumentNode(
                                name=NameNode(
                                    value="nullArg",
                                    location=_EXPECTED_DEFAULT_LOCATION,
                                ),
                                value=NullValueNode(
                                    location=_EXPECTED_DEFAULT_LOCATION
                                ),
                                location=_EXPECTED_DEFAULT_LOCATION,
                            )
                        ],
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                    DirectiveNode(
                        name=NameNode(
                            value="secondDirective",
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        arguments=[],
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                ],
                location=_EXPECTED_DEFAULT_LOCATION,
            ),
        ),
        (
            {
                "kind": "InlineFragment",
                "directives": [
                    {
                        "name": {
                            "value": "firstDirective",
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "arguments": [
                            {
                                "name": {
                                    "value": "nullArg",
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                },
                                "value": {
                                    "kind": "NullValue",
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                },
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            }
                        ],
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    {
                        "name": {
                            "value": "secondDirective",
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "arguments": None,
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                ],
                "typeCondition": {
                    "name": {
                        "value": "MyType",
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                "selectionSet": {
                    "selections": [
                        {
                            "kind": "Field",
                            "alias": None,
                            "name": {
                                "value": "myTypeField",
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            },
                            "arguments": None,
                            "directives": None,
                            "selectionSet": None,
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        }
                    ],
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                "loc": _DEFAULT_JSON_AST_LOCATION,
            },
            InlineFragmentNode(
                directives=[
                    DirectiveNode(
                        name=NameNode(
                            value="firstDirective",
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        arguments=[
                            ArgumentNode(
                                name=NameNode(
                                    value="nullArg",
                                    location=_EXPECTED_DEFAULT_LOCATION,
                                ),
                                value=NullValueNode(
                                    location=_EXPECTED_DEFAULT_LOCATION
                                ),
                                location=_EXPECTED_DEFAULT_LOCATION,
                            )
                        ],
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                    DirectiveNode(
                        name=NameNode(
                            value="secondDirective",
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        arguments=[],
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                ],
                type_condition=NamedTypeNode(
                    name=NameNode(
                        value="MyType", location=_EXPECTED_DEFAULT_LOCATION
                    ),
                    location=_EXPECTED_DEFAULT_LOCATION,
                ),
                selection_set=SelectionSetNode(
                    selections=[
                        FieldNode(
                            alias=None,
                            name=NameNode(
                                value="myTypeField",
                                location=_EXPECTED_DEFAULT_LOCATION,
                            ),
                            arguments=[],
                            directives=[],
                            selection_set=None,
                            location=_EXPECTED_DEFAULT_LOCATION,
                        )
                    ],
                    location=_EXPECTED_DEFAULT_LOCATION,
                ),
                location=_EXPECTED_DEFAULT_LOCATION,
            ),
        ),
    ],
)
def test_parse_selection(json_ast, expected):
    assert _parse_selection(json_ast) == expected


@pytest.mark.parametrize(
    "json_ast,expected",
    [
        (None, []),
        ([], []),
        (
            [
                {
                    "kind": "Field",
                    "alias": {
                        "value": "fieldAlias",
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    "name": {
                        "value": "fieldName",
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    "arguments": [
                        {
                            "name": {
                                "value": "nullArg",
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            },
                            "value": {
                                "kind": "NullValue",
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            },
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        }
                    ],
                    "directives": [
                        {
                            "name": {
                                "value": "firstDirective",
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            },
                            "arguments": [
                                {
                                    "name": {
                                        "value": "nullArg",
                                        "loc": _DEFAULT_JSON_AST_LOCATION,
                                    },
                                    "value": {
                                        "kind": "NullValue",
                                        "loc": _DEFAULT_JSON_AST_LOCATION,
                                    },
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                }
                            ],
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        {
                            "name": {
                                "value": "secondDirective",
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            },
                            "arguments": None,
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                    ],
                    "selectionSet": {
                        "selections": [
                            {
                                "kind": "FragmentSpread",
                                "name": {
                                    "value": "spreadedFragment",
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                },
                                "directives": None,
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            }
                        ],
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                {
                    "kind": "FragmentSpread",
                    "name": {
                        "value": "spreadedFragment",
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    "directives": [
                        {
                            "name": {
                                "value": "firstDirective",
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            },
                            "arguments": [
                                {
                                    "name": {
                                        "value": "nullArg",
                                        "loc": _DEFAULT_JSON_AST_LOCATION,
                                    },
                                    "value": {
                                        "kind": "NullValue",
                                        "loc": _DEFAULT_JSON_AST_LOCATION,
                                    },
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                }
                            ],
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        {
                            "name": {
                                "value": "secondDirective",
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            },
                            "arguments": None,
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                    ],
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                {
                    "kind": "InlineFragment",
                    "directives": [
                        {
                            "name": {
                                "value": "firstDirective",
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            },
                            "arguments": [
                                {
                                    "name": {
                                        "value": "nullArg",
                                        "loc": _DEFAULT_JSON_AST_LOCATION,
                                    },
                                    "value": {
                                        "kind": "NullValue",
                                        "loc": _DEFAULT_JSON_AST_LOCATION,
                                    },
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                }
                            ],
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        {
                            "name": {
                                "value": "secondDirective",
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            },
                            "arguments": None,
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                    ],
                    "typeCondition": {
                        "name": {
                            "value": "MyType",
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    "selectionSet": {
                        "selections": [
                            {
                                "kind": "Field",
                                "alias": None,
                                "name": {
                                    "value": "myTypeField",
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                },
                                "arguments": None,
                                "directives": None,
                                "selectionSet": None,
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            }
                        ],
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
            ],
            [
                FieldNode(
                    alias=NameNode(
                        value="fieldAlias", location=_EXPECTED_DEFAULT_LOCATION
                    ),
                    name=NameNode(
                        value="fieldName", location=_EXPECTED_DEFAULT_LOCATION
                    ),
                    arguments=[
                        ArgumentNode(
                            name=NameNode(
                                value="nullArg",
                                location=_EXPECTED_DEFAULT_LOCATION,
                            ),
                            value=NullValueNode(
                                location=_EXPECTED_DEFAULT_LOCATION
                            ),
                            location=_EXPECTED_DEFAULT_LOCATION,
                        )
                    ],
                    directives=[
                        DirectiveNode(
                            name=NameNode(
                                value="firstDirective",
                                location=_EXPECTED_DEFAULT_LOCATION,
                            ),
                            arguments=[
                                ArgumentNode(
                                    name=NameNode(
                                        value="nullArg",
                                        location=_EXPECTED_DEFAULT_LOCATION,
                                    ),
                                    value=NullValueNode(
                                        location=_EXPECTED_DEFAULT_LOCATION
                                    ),
                                    location=_EXPECTED_DEFAULT_LOCATION,
                                )
                            ],
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        DirectiveNode(
                            name=NameNode(
                                value="secondDirective",
                                location=_EXPECTED_DEFAULT_LOCATION,
                            ),
                            arguments=[],
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                    ],
                    selection_set=SelectionSetNode(
                        selections=[
                            FragmentSpreadNode(
                                name=NameNode(
                                    value="spreadedFragment",
                                    location=_EXPECTED_DEFAULT_LOCATION,
                                ),
                                directives=[],
                                location=_EXPECTED_DEFAULT_LOCATION,
                            )
                        ],
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                    location=_EXPECTED_DEFAULT_LOCATION,
                ),
                FragmentSpreadNode(
                    name=NameNode(
                        value="spreadedFragment",
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                    directives=[
                        DirectiveNode(
                            name=NameNode(
                                value="firstDirective",
                                location=_EXPECTED_DEFAULT_LOCATION,
                            ),
                            arguments=[
                                ArgumentNode(
                                    name=NameNode(
                                        value="nullArg",
                                        location=_EXPECTED_DEFAULT_LOCATION,
                                    ),
                                    value=NullValueNode(
                                        location=_EXPECTED_DEFAULT_LOCATION
                                    ),
                                    location=_EXPECTED_DEFAULT_LOCATION,
                                )
                            ],
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        DirectiveNode(
                            name=NameNode(
                                value="secondDirective",
                                location=_EXPECTED_DEFAULT_LOCATION,
                            ),
                            arguments=[],
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                    ],
                    location=_EXPECTED_DEFAULT_LOCATION,
                ),
                InlineFragmentNode(
                    directives=[
                        DirectiveNode(
                            name=NameNode(
                                value="firstDirective",
                                location=_EXPECTED_DEFAULT_LOCATION,
                            ),
                            arguments=[
                                ArgumentNode(
                                    name=NameNode(
                                        value="nullArg",
                                        location=_EXPECTED_DEFAULT_LOCATION,
                                    ),
                                    value=NullValueNode(
                                        location=_EXPECTED_DEFAULT_LOCATION
                                    ),
                                    location=_EXPECTED_DEFAULT_LOCATION,
                                )
                            ],
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        DirectiveNode(
                            name=NameNode(
                                value="secondDirective",
                                location=_EXPECTED_DEFAULT_LOCATION,
                            ),
                            arguments=[],
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                    ],
                    type_condition=NamedTypeNode(
                        name=NameNode(
                            value="MyType", location=_EXPECTED_DEFAULT_LOCATION
                        ),
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                    selection_set=SelectionSetNode(
                        selections=[
                            FieldNode(
                                alias=None,
                                name=NameNode(
                                    value="myTypeField",
                                    location=_EXPECTED_DEFAULT_LOCATION,
                                ),
                                arguments=[],
                                directives=[],
                                selection_set=None,
                                location=_EXPECTED_DEFAULT_LOCATION,
                            )
                        ],
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                    location=_EXPECTED_DEFAULT_LOCATION,
                ),
            ],
        ),
    ],
)
def test_parse_selections(json_ast, expected):
    assert _parse_selections(json_ast) == expected


@pytest.mark.parametrize(
    "json_ast,expected",
    [
        (None, None),
        ({}, None),
        (
            {
                "selections": [
                    {
                        "kind": "Field",
                        "alias": {
                            "value": "fieldAlias",
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "name": {
                            "value": "fieldName",
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "arguments": [
                            {
                                "name": {
                                    "value": "nullArg",
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                },
                                "value": {
                                    "kind": "NullValue",
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                },
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            }
                        ],
                        "directives": [
                            {
                                "name": {
                                    "value": "firstDirective",
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                },
                                "arguments": [
                                    {
                                        "name": {
                                            "value": "nullArg",
                                            "loc": _DEFAULT_JSON_AST_LOCATION,
                                        },
                                        "value": {
                                            "kind": "NullValue",
                                            "loc": _DEFAULT_JSON_AST_LOCATION,
                                        },
                                        "loc": _DEFAULT_JSON_AST_LOCATION,
                                    }
                                ],
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            },
                            {
                                "name": {
                                    "value": "secondDirective",
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                },
                                "arguments": None,
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            },
                        ],
                        "selectionSet": {
                            "selections": [
                                {
                                    "kind": "FragmentSpread",
                                    "name": {
                                        "value": "spreadedFragment",
                                        "loc": _DEFAULT_JSON_AST_LOCATION,
                                    },
                                    "directives": None,
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                }
                            ],
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    {
                        "kind": "FragmentSpread",
                        "name": {
                            "value": "spreadedFragment",
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "directives": [
                            {
                                "name": {
                                    "value": "firstDirective",
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                },
                                "arguments": [
                                    {
                                        "name": {
                                            "value": "nullArg",
                                            "loc": _DEFAULT_JSON_AST_LOCATION,
                                        },
                                        "value": {
                                            "kind": "NullValue",
                                            "loc": _DEFAULT_JSON_AST_LOCATION,
                                        },
                                        "loc": _DEFAULT_JSON_AST_LOCATION,
                                    }
                                ],
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            },
                            {
                                "name": {
                                    "value": "secondDirective",
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                },
                                "arguments": None,
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            },
                        ],
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    {
                        "kind": "InlineFragment",
                        "directives": [
                            {
                                "name": {
                                    "value": "firstDirective",
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                },
                                "arguments": [
                                    {
                                        "name": {
                                            "value": "nullArg",
                                            "loc": _DEFAULT_JSON_AST_LOCATION,
                                        },
                                        "value": {
                                            "kind": "NullValue",
                                            "loc": _DEFAULT_JSON_AST_LOCATION,
                                        },
                                        "loc": _DEFAULT_JSON_AST_LOCATION,
                                    }
                                ],
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            },
                            {
                                "name": {
                                    "value": "secondDirective",
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                },
                                "arguments": None,
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            },
                        ],
                        "typeCondition": {
                            "name": {
                                "value": "MyType",
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            },
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "selectionSet": {
                            "selections": [
                                {
                                    "kind": "Field",
                                    "alias": None,
                                    "name": {
                                        "value": "myTypeField",
                                        "loc": _DEFAULT_JSON_AST_LOCATION,
                                    },
                                    "arguments": None,
                                    "directives": None,
                                    "selectionSet": None,
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                }
                            ],
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                ],
                "loc": _DEFAULT_JSON_AST_LOCATION,
            },
            SelectionSetNode(
                selections=[
                    FieldNode(
                        alias=NameNode(
                            value="fieldAlias",
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        name=NameNode(
                            value="fieldName",
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        arguments=[
                            ArgumentNode(
                                name=NameNode(
                                    value="nullArg",
                                    location=_EXPECTED_DEFAULT_LOCATION,
                                ),
                                value=NullValueNode(
                                    location=_EXPECTED_DEFAULT_LOCATION
                                ),
                                location=_EXPECTED_DEFAULT_LOCATION,
                            )
                        ],
                        directives=[
                            DirectiveNode(
                                name=NameNode(
                                    value="firstDirective",
                                    location=_EXPECTED_DEFAULT_LOCATION,
                                ),
                                arguments=[
                                    ArgumentNode(
                                        name=NameNode(
                                            value="nullArg",
                                            location=_EXPECTED_DEFAULT_LOCATION,
                                        ),
                                        value=NullValueNode(
                                            location=_EXPECTED_DEFAULT_LOCATION
                                        ),
                                        location=_EXPECTED_DEFAULT_LOCATION,
                                    )
                                ],
                                location=_EXPECTED_DEFAULT_LOCATION,
                            ),
                            DirectiveNode(
                                name=NameNode(
                                    value="secondDirective",
                                    location=_EXPECTED_DEFAULT_LOCATION,
                                ),
                                arguments=[],
                                location=_EXPECTED_DEFAULT_LOCATION,
                            ),
                        ],
                        selection_set=SelectionSetNode(
                            selections=[
                                FragmentSpreadNode(
                                    name=NameNode(
                                        value="spreadedFragment",
                                        location=_EXPECTED_DEFAULT_LOCATION,
                                    ),
                                    directives=[],
                                    location=_EXPECTED_DEFAULT_LOCATION,
                                )
                            ],
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                    FragmentSpreadNode(
                        name=NameNode(
                            value="spreadedFragment",
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        directives=[
                            DirectiveNode(
                                name=NameNode(
                                    value="firstDirective",
                                    location=_EXPECTED_DEFAULT_LOCATION,
                                ),
                                arguments=[
                                    ArgumentNode(
                                        name=NameNode(
                                            value="nullArg",
                                            location=_EXPECTED_DEFAULT_LOCATION,
                                        ),
                                        value=NullValueNode(
                                            location=_EXPECTED_DEFAULT_LOCATION
                                        ),
                                        location=_EXPECTED_DEFAULT_LOCATION,
                                    )
                                ],
                                location=_EXPECTED_DEFAULT_LOCATION,
                            ),
                            DirectiveNode(
                                name=NameNode(
                                    value="secondDirective",
                                    location=_EXPECTED_DEFAULT_LOCATION,
                                ),
                                arguments=[],
                                location=_EXPECTED_DEFAULT_LOCATION,
                            ),
                        ],
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                    InlineFragmentNode(
                        directives=[
                            DirectiveNode(
                                name=NameNode(
                                    value="firstDirective",
                                    location=_EXPECTED_DEFAULT_LOCATION,
                                ),
                                arguments=[
                                    ArgumentNode(
                                        name=NameNode(
                                            value="nullArg",
                                            location=_EXPECTED_DEFAULT_LOCATION,
                                        ),
                                        value=NullValueNode(
                                            location=_EXPECTED_DEFAULT_LOCATION
                                        ),
                                        location=_EXPECTED_DEFAULT_LOCATION,
                                    )
                                ],
                                location=_EXPECTED_DEFAULT_LOCATION,
                            ),
                            DirectiveNode(
                                name=NameNode(
                                    value="secondDirective",
                                    location=_EXPECTED_DEFAULT_LOCATION,
                                ),
                                arguments=[],
                                location=_EXPECTED_DEFAULT_LOCATION,
                            ),
                        ],
                        type_condition=NamedTypeNode(
                            name=NameNode(
                                value="MyType",
                                location=_EXPECTED_DEFAULT_LOCATION,
                            ),
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        selection_set=SelectionSetNode(
                            selections=[
                                FieldNode(
                                    alias=None,
                                    name=NameNode(
                                        value="myTypeField",
                                        location=_EXPECTED_DEFAULT_LOCATION,
                                    ),
                                    arguments=[],
                                    directives=[],
                                    selection_set=None,
                                    location=_EXPECTED_DEFAULT_LOCATION,
                                )
                            ],
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                ],
                location=_EXPECTED_DEFAULT_LOCATION,
            ),
        ),
    ],
)
def test_parse_selection_set(json_ast, expected):
    assert _parse_selection_set(json_ast) == expected


@pytest.mark.parametrize(
    "json_ast,expected",
    [
        (
            {
                "name": {
                    "value": "MyFragment",
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                "typeCondition": {
                    "name": {
                        "value": "MyType",
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                "directives": [
                    {
                        "name": {
                            "value": "firstDirective",
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "arguments": [
                            {
                                "name": {
                                    "value": "nullArg",
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                },
                                "value": {
                                    "kind": "NullValue",
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                },
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            }
                        ],
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    {
                        "name": {
                            "value": "secondDirective",
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "arguments": None,
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                ],
                "selectionSet": {
                    "selections": [
                        {
                            "kind": "FragmentSpread",
                            "name": {
                                "value": "spreadedFragment",
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            },
                            "directives": None,
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        }
                    ],
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                "loc": _DEFAULT_JSON_AST_LOCATION,
            },
            FragmentDefinitionNode(
                name=NameNode(
                    value="MyFragment", location=_EXPECTED_DEFAULT_LOCATION
                ),
                type_condition=NamedTypeNode(
                    name=NameNode(
                        value="MyType", location=_EXPECTED_DEFAULT_LOCATION
                    ),
                    location=_EXPECTED_DEFAULT_LOCATION,
                ),
                directives=[
                    DirectiveNode(
                        name=NameNode(
                            value="firstDirective",
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        arguments=[
                            ArgumentNode(
                                name=NameNode(
                                    value="nullArg",
                                    location=_EXPECTED_DEFAULT_LOCATION,
                                ),
                                value=NullValueNode(
                                    location=_EXPECTED_DEFAULT_LOCATION
                                ),
                                location=_EXPECTED_DEFAULT_LOCATION,
                            )
                        ],
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                    DirectiveNode(
                        name=NameNode(
                            value="secondDirective",
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        arguments=[],
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                ],
                selection_set=SelectionSetNode(
                    selections=[
                        FragmentSpreadNode(
                            name=NameNode(
                                value="spreadedFragment",
                                location=_EXPECTED_DEFAULT_LOCATION,
                            ),
                            directives=[],
                            location=_EXPECTED_DEFAULT_LOCATION,
                        )
                    ],
                    location=_EXPECTED_DEFAULT_LOCATION,
                ),
                location=_EXPECTED_DEFAULT_LOCATION,
            ),
        ),
        (
            {
                "name": {
                    "value": "MyFragment",
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                "typeCondition": {
                    "name": {
                        "value": "MyType",
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                "directives": None,
                "selectionSet": None,
                "loc": _DEFAULT_JSON_AST_LOCATION,
            },
            FragmentDefinitionNode(
                name=NameNode(
                    value="MyFragment", location=_EXPECTED_DEFAULT_LOCATION
                ),
                type_condition=NamedTypeNode(
                    name=NameNode(
                        value="MyType", location=_EXPECTED_DEFAULT_LOCATION
                    ),
                    location=_EXPECTED_DEFAULT_LOCATION,
                ),
                directives=[],
                selection_set=None,
                location=_EXPECTED_DEFAULT_LOCATION,
            ),
        ),
    ],
)
def test_parse_fragment_definition(json_ast, expected):
    assert _parse_fragment_definition(json_ast) == expected


@pytest.mark.parametrize(
    "json_ast,expected",
    [
        (
            {
                "kind": "NamedType",
                "name": {"value": "MyType", "loc": _DEFAULT_JSON_AST_LOCATION},
                "loc": _DEFAULT_JSON_AST_LOCATION,
            },
            NamedTypeNode(
                name=NameNode(
                    value="MyType", location=_EXPECTED_DEFAULT_LOCATION
                ),
                location=_EXPECTED_DEFAULT_LOCATION,
            ),
        ),
        (
            {
                "kind": "NonNullType",
                "type": {
                    "kind": "ListType",
                    "type": {
                        "kind": "NonNullType",
                        "type": {
                            "kind": "NamedType",
                            "name": {
                                "value": "MyType",
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            },
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                "loc": _DEFAULT_JSON_AST_LOCATION,
            },
            NonNullTypeNode(
                type=ListTypeNode(
                    type=NonNullTypeNode(
                        type=NamedTypeNode(
                            name=NameNode(
                                value="MyType",
                                location=_EXPECTED_DEFAULT_LOCATION,
                            ),
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                    location=_EXPECTED_DEFAULT_LOCATION,
                ),
                location=_EXPECTED_DEFAULT_LOCATION,
            ),
        ),
    ],
)
def test_parse_type(json_ast, expected):
    assert _parse_type(json_ast) == expected


@pytest.mark.parametrize(
    "json_ast,expected",
    [
        (
            {
                "variable": {
                    "name": {
                        "value": "varName",
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                "type": {
                    "kind": "NamedType",
                    "name": {
                        "value": "MyInputType",
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                "defaultValue": {
                    "kind": "BooleanValue",
                    "value": True,
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                "loc": _DEFAULT_JSON_AST_LOCATION,
            },
            VariableDefinitionNode(
                variable=VariableNode(
                    name=NameNode(
                        value="varName", location=_EXPECTED_DEFAULT_LOCATION
                    ),
                    location=_EXPECTED_DEFAULT_LOCATION,
                ),
                type=NamedTypeNode(
                    name=NameNode(
                        value="MyInputType",
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                    location=_EXPECTED_DEFAULT_LOCATION,
                ),
                default_value=BooleanValueNode(
                    value=True, location=_EXPECTED_DEFAULT_LOCATION
                ),
                location=_EXPECTED_DEFAULT_LOCATION,
            ),
        )
    ],
)
def test_parse_variable_definition(json_ast, expected):
    assert _parse_variable_definition(json_ast) == expected


@pytest.mark.parametrize(
    "json_ast,expected",
    [
        (None, []),
        ([], []),
        (
            [
                {
                    "variable": {
                        "name": {
                            "value": "varName",
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    "type": {
                        "kind": "NamedType",
                        "name": {
                            "value": "MyInputType",
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    "defaultValue": {
                        "kind": "BooleanValue",
                        "value": True,
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                }
            ],
            [
                VariableDefinitionNode(
                    variable=VariableNode(
                        name=NameNode(
                            value="varName",
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                    type=NamedTypeNode(
                        name=NameNode(
                            value="MyInputType",
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                    default_value=BooleanValueNode(
                        value=True, location=_EXPECTED_DEFAULT_LOCATION
                    ),
                    location=_EXPECTED_DEFAULT_LOCATION,
                )
            ],
        ),
    ],
)
def test_parse_variable_definitions(json_ast, expected):
    assert _parse_variable_definitions(json_ast) == expected


@pytest.mark.parametrize(
    "json_ast,expected",
    [
        (
            {
                "operation": "query",
                "name": {
                    "value": "MyOperation",
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                "variableDefinitions": [
                    {
                        "variable": {
                            "name": {
                                "value": "varName",
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            },
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "type": {
                            "kind": "NamedType",
                            "name": {
                                "value": "MyInputType",
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            },
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "defaultValue": {
                            "kind": "BooleanValue",
                            "value": True,
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    }
                ],
                "directives": [
                    {
                        "name": {
                            "value": "firstDirective",
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "arguments": [
                            {
                                "name": {
                                    "value": "nullArg",
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                },
                                "value": {
                                    "kind": "NullValue",
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                },
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            }
                        ],
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    {
                        "name": {
                            "value": "secondDirective",
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "arguments": None,
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                ],
                "selectionSet": {
                    "selections": [
                        {
                            "kind": "FragmentSpread",
                            "name": {
                                "value": "spreadedFragment",
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            },
                            "directives": None,
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        }
                    ],
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                "loc": _DEFAULT_JSON_AST_LOCATION,
            },
            OperationDefinitionNode(
                operation_type="query",
                name=NameNode(
                    value="MyOperation", location=_EXPECTED_DEFAULT_LOCATION
                ),
                variable_definitions=[
                    VariableDefinitionNode(
                        variable=VariableNode(
                            name=NameNode(
                                value="varName",
                                location=_EXPECTED_DEFAULT_LOCATION,
                            ),
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        type=NamedTypeNode(
                            name=NameNode(
                                value="MyInputType",
                                location=_EXPECTED_DEFAULT_LOCATION,
                            ),
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        default_value=BooleanValueNode(
                            value=True, location=_EXPECTED_DEFAULT_LOCATION
                        ),
                        location=_EXPECTED_DEFAULT_LOCATION,
                    )
                ],
                directives=[
                    DirectiveNode(
                        name=NameNode(
                            value="firstDirective",
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        arguments=[
                            ArgumentNode(
                                name=NameNode(
                                    value="nullArg",
                                    location=_EXPECTED_DEFAULT_LOCATION,
                                ),
                                value=NullValueNode(
                                    location=_EXPECTED_DEFAULT_LOCATION
                                ),
                                location=_EXPECTED_DEFAULT_LOCATION,
                            )
                        ],
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                    DirectiveNode(
                        name=NameNode(
                            value="secondDirective",
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        arguments=[],
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                ],
                selection_set=SelectionSetNode(
                    selections=[
                        FragmentSpreadNode(
                            name=NameNode(
                                value="spreadedFragment",
                                location=_EXPECTED_DEFAULT_LOCATION,
                            ),
                            directives=[],
                            location=_EXPECTED_DEFAULT_LOCATION,
                        )
                    ],
                    location=_EXPECTED_DEFAULT_LOCATION,
                ),
                location=_EXPECTED_DEFAULT_LOCATION,
            ),
        ),
        (
            {
                "operation": "query",
                "name": None,
                "variableDefinitions": None,
                "directives": None,
                "selectionSet": None,
                "loc": _DEFAULT_JSON_AST_LOCATION,
            },
            OperationDefinitionNode(
                operation_type="query",
                name=None,
                variable_definitions=[],
                directives=[],
                selection_set=None,
                location=_EXPECTED_DEFAULT_LOCATION,
            ),
        ),
    ],
)
def test_parse_operation_definition(json_ast, expected):
    assert _parse_operation_definition(json_ast) == expected


@pytest.mark.parametrize(
    "json_ast,expected",
    [
        (
            {
                "kind": "FragmentDefinition",
                "name": {
                    "value": "MyFragment",
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                "typeCondition": {
                    "name": {
                        "value": "MyType",
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                "directives": [
                    {
                        "name": {
                            "value": "firstDirective",
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "arguments": [
                            {
                                "name": {
                                    "value": "nullArg",
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                },
                                "value": {
                                    "kind": "NullValue",
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                },
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            }
                        ],
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    {
                        "name": {
                            "value": "secondDirective",
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "arguments": None,
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                ],
                "selectionSet": {
                    "selections": [
                        {
                            "kind": "FragmentSpread",
                            "name": {
                                "value": "spreadedFragment",
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            },
                            "directives": None,
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        }
                    ],
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                "loc": _DEFAULT_JSON_AST_LOCATION,
            },
            FragmentDefinitionNode(
                name=NameNode(
                    value="MyFragment", location=_EXPECTED_DEFAULT_LOCATION
                ),
                type_condition=NamedTypeNode(
                    name=NameNode(
                        value="MyType", location=_EXPECTED_DEFAULT_LOCATION
                    ),
                    location=_EXPECTED_DEFAULT_LOCATION,
                ),
                directives=[
                    DirectiveNode(
                        name=NameNode(
                            value="firstDirective",
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        arguments=[
                            ArgumentNode(
                                name=NameNode(
                                    value="nullArg",
                                    location=_EXPECTED_DEFAULT_LOCATION,
                                ),
                                value=NullValueNode(
                                    location=_EXPECTED_DEFAULT_LOCATION
                                ),
                                location=_EXPECTED_DEFAULT_LOCATION,
                            )
                        ],
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                    DirectiveNode(
                        name=NameNode(
                            value="secondDirective",
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        arguments=[],
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                ],
                selection_set=SelectionSetNode(
                    selections=[
                        FragmentSpreadNode(
                            name=NameNode(
                                value="spreadedFragment",
                                location=_EXPECTED_DEFAULT_LOCATION,
                            ),
                            directives=[],
                            location=_EXPECTED_DEFAULT_LOCATION,
                        )
                    ],
                    location=_EXPECTED_DEFAULT_LOCATION,
                ),
                location=_EXPECTED_DEFAULT_LOCATION,
            ),
        ),
        (
            {
                "kind": "OperationDefinition",
                "operation": "query",
                "name": {
                    "value": "MyOperation",
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                "variableDefinitions": [
                    {
                        "variable": {
                            "name": {
                                "value": "varName",
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            },
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "type": {
                            "kind": "NamedType",
                            "name": {
                                "value": "MyInputType",
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            },
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "defaultValue": {
                            "kind": "BooleanValue",
                            "value": True,
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    }
                ],
                "directives": [
                    {
                        "name": {
                            "value": "firstDirective",
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "arguments": [
                            {
                                "name": {
                                    "value": "nullArg",
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                },
                                "value": {
                                    "kind": "NullValue",
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                },
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            }
                        ],
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    {
                        "name": {
                            "value": "secondDirective",
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "arguments": None,
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                ],
                "selectionSet": {
                    "selections": [
                        {
                            "kind": "FragmentSpread",
                            "name": {
                                "value": "spreadedFragment",
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            },
                            "directives": None,
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        }
                    ],
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                "loc": _DEFAULT_JSON_AST_LOCATION,
            },
            OperationDefinitionNode(
                operation_type="query",
                name=NameNode(
                    value="MyOperation", location=_EXPECTED_DEFAULT_LOCATION
                ),
                variable_definitions=[
                    VariableDefinitionNode(
                        variable=VariableNode(
                            name=NameNode(
                                value="varName",
                                location=_EXPECTED_DEFAULT_LOCATION,
                            ),
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        type=NamedTypeNode(
                            name=NameNode(
                                value="MyInputType",
                                location=_EXPECTED_DEFAULT_LOCATION,
                            ),
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        default_value=BooleanValueNode(
                            value=True, location=_EXPECTED_DEFAULT_LOCATION
                        ),
                        location=_EXPECTED_DEFAULT_LOCATION,
                    )
                ],
                directives=[
                    DirectiveNode(
                        name=NameNode(
                            value="firstDirective",
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        arguments=[
                            ArgumentNode(
                                name=NameNode(
                                    value="nullArg",
                                    location=_EXPECTED_DEFAULT_LOCATION,
                                ),
                                value=NullValueNode(
                                    location=_EXPECTED_DEFAULT_LOCATION
                                ),
                                location=_EXPECTED_DEFAULT_LOCATION,
                            )
                        ],
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                    DirectiveNode(
                        name=NameNode(
                            value="secondDirective",
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        arguments=[],
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                ],
                selection_set=SelectionSetNode(
                    selections=[
                        FragmentSpreadNode(
                            name=NameNode(
                                value="spreadedFragment",
                                location=_EXPECTED_DEFAULT_LOCATION,
                            ),
                            directives=[],
                            location=_EXPECTED_DEFAULT_LOCATION,
                        )
                    ],
                    location=_EXPECTED_DEFAULT_LOCATION,
                ),
                location=_EXPECTED_DEFAULT_LOCATION,
            ),
        ),
    ],
)
def test_parse_definition(json_ast, expected):
    assert _parse_definition(json_ast) == expected


@pytest.mark.parametrize(
    "json_ast,expected",
    [
        (None, []),
        ([], []),
        (
            [
                {
                    "kind": "FragmentDefinition",
                    "name": {
                        "value": "MyFragment",
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    "typeCondition": {
                        "name": {
                            "value": "MyType",
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    "directives": [
                        {
                            "name": {
                                "value": "firstDirective",
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            },
                            "arguments": [
                                {
                                    "name": {
                                        "value": "nullArg",
                                        "loc": _DEFAULT_JSON_AST_LOCATION,
                                    },
                                    "value": {
                                        "kind": "NullValue",
                                        "loc": _DEFAULT_JSON_AST_LOCATION,
                                    },
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                }
                            ],
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        {
                            "name": {
                                "value": "secondDirective",
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            },
                            "arguments": None,
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                    ],
                    "selectionSet": {
                        "selections": [
                            {
                                "kind": "FragmentSpread",
                                "name": {
                                    "value": "spreadedFragment",
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                },
                                "directives": None,
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            }
                        ],
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
                {
                    "kind": "OperationDefinition",
                    "operation": "query",
                    "name": {
                        "value": "MyOperation",
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    "variableDefinitions": [
                        {
                            "variable": {
                                "name": {
                                    "value": "varName",
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                },
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            },
                            "type": {
                                "kind": "NamedType",
                                "name": {
                                    "value": "MyInputType",
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                },
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            },
                            "defaultValue": {
                                "kind": "BooleanValue",
                                "value": True,
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            },
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        }
                    ],
                    "directives": [
                        {
                            "name": {
                                "value": "firstDirective",
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            },
                            "arguments": [
                                {
                                    "name": {
                                        "value": "nullArg",
                                        "loc": _DEFAULT_JSON_AST_LOCATION,
                                    },
                                    "value": {
                                        "kind": "NullValue",
                                        "loc": _DEFAULT_JSON_AST_LOCATION,
                                    },
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                }
                            ],
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        {
                            "name": {
                                "value": "secondDirective",
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            },
                            "arguments": None,
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                    ],
                    "selectionSet": {
                        "selections": [
                            {
                                "kind": "FragmentSpread",
                                "name": {
                                    "value": "spreadedFragment",
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                },
                                "directives": None,
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            }
                        ],
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    "loc": _DEFAULT_JSON_AST_LOCATION,
                },
            ],
            [
                FragmentDefinitionNode(
                    name=NameNode(
                        value="MyFragment", location=_EXPECTED_DEFAULT_LOCATION
                    ),
                    type_condition=NamedTypeNode(
                        name=NameNode(
                            value="MyType", location=_EXPECTED_DEFAULT_LOCATION
                        ),
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                    directives=[
                        DirectiveNode(
                            name=NameNode(
                                value="firstDirective",
                                location=_EXPECTED_DEFAULT_LOCATION,
                            ),
                            arguments=[
                                ArgumentNode(
                                    name=NameNode(
                                        value="nullArg",
                                        location=_EXPECTED_DEFAULT_LOCATION,
                                    ),
                                    value=NullValueNode(
                                        location=_EXPECTED_DEFAULT_LOCATION
                                    ),
                                    location=_EXPECTED_DEFAULT_LOCATION,
                                )
                            ],
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        DirectiveNode(
                            name=NameNode(
                                value="secondDirective",
                                location=_EXPECTED_DEFAULT_LOCATION,
                            ),
                            arguments=[],
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                    ],
                    selection_set=SelectionSetNode(
                        selections=[
                            FragmentSpreadNode(
                                name=NameNode(
                                    value="spreadedFragment",
                                    location=_EXPECTED_DEFAULT_LOCATION,
                                ),
                                directives=[],
                                location=_EXPECTED_DEFAULT_LOCATION,
                            )
                        ],
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                    location=_EXPECTED_DEFAULT_LOCATION,
                ),
                OperationDefinitionNode(
                    operation_type="query",
                    name=NameNode(
                        value="MyOperation",
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                    variable_definitions=[
                        VariableDefinitionNode(
                            variable=VariableNode(
                                name=NameNode(
                                    value="varName",
                                    location=_EXPECTED_DEFAULT_LOCATION,
                                ),
                                location=_EXPECTED_DEFAULT_LOCATION,
                            ),
                            type=NamedTypeNode(
                                name=NameNode(
                                    value="MyInputType",
                                    location=_EXPECTED_DEFAULT_LOCATION,
                                ),
                                location=_EXPECTED_DEFAULT_LOCATION,
                            ),
                            default_value=BooleanValueNode(
                                value=True, location=_EXPECTED_DEFAULT_LOCATION
                            ),
                            location=_EXPECTED_DEFAULT_LOCATION,
                        )
                    ],
                    directives=[
                        DirectiveNode(
                            name=NameNode(
                                value="firstDirective",
                                location=_EXPECTED_DEFAULT_LOCATION,
                            ),
                            arguments=[
                                ArgumentNode(
                                    name=NameNode(
                                        value="nullArg",
                                        location=_EXPECTED_DEFAULT_LOCATION,
                                    ),
                                    value=NullValueNode(
                                        location=_EXPECTED_DEFAULT_LOCATION
                                    ),
                                    location=_EXPECTED_DEFAULT_LOCATION,
                                )
                            ],
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        DirectiveNode(
                            name=NameNode(
                                value="secondDirective",
                                location=_EXPECTED_DEFAULT_LOCATION,
                            ),
                            arguments=[],
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                    ],
                    selection_set=SelectionSetNode(
                        selections=[
                            FragmentSpreadNode(
                                name=NameNode(
                                    value="spreadedFragment",
                                    location=_EXPECTED_DEFAULT_LOCATION,
                                ),
                                directives=[],
                                location=_EXPECTED_DEFAULT_LOCATION,
                            )
                        ],
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                    location=_EXPECTED_DEFAULT_LOCATION,
                ),
            ],
        ),
    ],
)
def test_parse_definitions(json_ast, expected):
    assert _parse_definitions(json_ast) == expected


@pytest.mark.parametrize(
    "json_ast,expected",
    [
        (
            {"definitions": None, "loc": _DEFAULT_JSON_AST_LOCATION},
            DocumentNode(definitions=[], location=_EXPECTED_DEFAULT_LOCATION),
        ),
        (
            {"definitions": [], "loc": _DEFAULT_JSON_AST_LOCATION},
            DocumentNode(definitions=[], location=_EXPECTED_DEFAULT_LOCATION),
        ),
        (
            {
                "definitions": [
                    {
                        "kind": "FragmentDefinition",
                        "name": {
                            "value": "MyFragment",
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "typeCondition": {
                            "name": {
                                "value": "MyType",
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            },
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "directives": [
                            {
                                "name": {
                                    "value": "firstDirective",
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                },
                                "arguments": [
                                    {
                                        "name": {
                                            "value": "nullArg",
                                            "loc": _DEFAULT_JSON_AST_LOCATION,
                                        },
                                        "value": {
                                            "kind": "NullValue",
                                            "loc": _DEFAULT_JSON_AST_LOCATION,
                                        },
                                        "loc": _DEFAULT_JSON_AST_LOCATION,
                                    }
                                ],
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            },
                            {
                                "name": {
                                    "value": "secondDirective",
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                },
                                "arguments": None,
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            },
                        ],
                        "selectionSet": {
                            "selections": [
                                {
                                    "kind": "FragmentSpread",
                                    "name": {
                                        "value": "spreadedFragment",
                                        "loc": _DEFAULT_JSON_AST_LOCATION,
                                    },
                                    "directives": None,
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                }
                            ],
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                    {
                        "kind": "OperationDefinition",
                        "operation": "query",
                        "name": {
                            "value": "MyOperation",
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "variableDefinitions": [
                            {
                                "variable": {
                                    "name": {
                                        "value": "varName",
                                        "loc": _DEFAULT_JSON_AST_LOCATION,
                                    },
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                },
                                "type": {
                                    "kind": "NamedType",
                                    "name": {
                                        "value": "MyInputType",
                                        "loc": _DEFAULT_JSON_AST_LOCATION,
                                    },
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                },
                                "defaultValue": {
                                    "kind": "BooleanValue",
                                    "value": True,
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                },
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            }
                        ],
                        "directives": [
                            {
                                "name": {
                                    "value": "firstDirective",
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                },
                                "arguments": [
                                    {
                                        "name": {
                                            "value": "nullArg",
                                            "loc": _DEFAULT_JSON_AST_LOCATION,
                                        },
                                        "value": {
                                            "kind": "NullValue",
                                            "loc": _DEFAULT_JSON_AST_LOCATION,
                                        },
                                        "loc": _DEFAULT_JSON_AST_LOCATION,
                                    }
                                ],
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            },
                            {
                                "name": {
                                    "value": "secondDirective",
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                },
                                "arguments": None,
                                "loc": _DEFAULT_JSON_AST_LOCATION,
                            },
                        ],
                        "selectionSet": {
                            "selections": [
                                {
                                    "kind": "FragmentSpread",
                                    "name": {
                                        "value": "spreadedFragment",
                                        "loc": _DEFAULT_JSON_AST_LOCATION,
                                    },
                                    "directives": None,
                                    "loc": _DEFAULT_JSON_AST_LOCATION,
                                }
                            ],
                            "loc": _DEFAULT_JSON_AST_LOCATION,
                        },
                        "loc": _DEFAULT_JSON_AST_LOCATION,
                    },
                ],
                "loc": _DEFAULT_JSON_AST_LOCATION,
            },
            DocumentNode(
                definitions=[
                    FragmentDefinitionNode(
                        name=NameNode(
                            value="MyFragment",
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        type_condition=NamedTypeNode(
                            name=NameNode(
                                value="MyType",
                                location=_EXPECTED_DEFAULT_LOCATION,
                            ),
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        directives=[
                            DirectiveNode(
                                name=NameNode(
                                    value="firstDirective",
                                    location=_EXPECTED_DEFAULT_LOCATION,
                                ),
                                arguments=[
                                    ArgumentNode(
                                        name=NameNode(
                                            value="nullArg",
                                            location=_EXPECTED_DEFAULT_LOCATION,
                                        ),
                                        value=NullValueNode(
                                            location=_EXPECTED_DEFAULT_LOCATION
                                        ),
                                        location=_EXPECTED_DEFAULT_LOCATION,
                                    )
                                ],
                                location=_EXPECTED_DEFAULT_LOCATION,
                            ),
                            DirectiveNode(
                                name=NameNode(
                                    value="secondDirective",
                                    location=_EXPECTED_DEFAULT_LOCATION,
                                ),
                                arguments=[],
                                location=_EXPECTED_DEFAULT_LOCATION,
                            ),
                        ],
                        selection_set=SelectionSetNode(
                            selections=[
                                FragmentSpreadNode(
                                    name=NameNode(
                                        value="spreadedFragment",
                                        location=_EXPECTED_DEFAULT_LOCATION,
                                    ),
                                    directives=[],
                                    location=_EXPECTED_DEFAULT_LOCATION,
                                )
                            ],
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                    OperationDefinitionNode(
                        operation_type="query",
                        name=NameNode(
                            value="MyOperation",
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        variable_definitions=[
                            VariableDefinitionNode(
                                variable=VariableNode(
                                    name=NameNode(
                                        value="varName",
                                        location=_EXPECTED_DEFAULT_LOCATION,
                                    ),
                                    location=_EXPECTED_DEFAULT_LOCATION,
                                ),
                                type=NamedTypeNode(
                                    name=NameNode(
                                        value="MyInputType",
                                        location=_EXPECTED_DEFAULT_LOCATION,
                                    ),
                                    location=_EXPECTED_DEFAULT_LOCATION,
                                ),
                                default_value=BooleanValueNode(
                                    value=True,
                                    location=_EXPECTED_DEFAULT_LOCATION,
                                ),
                                location=_EXPECTED_DEFAULT_LOCATION,
                            )
                        ],
                        directives=[
                            DirectiveNode(
                                name=NameNode(
                                    value="firstDirective",
                                    location=_EXPECTED_DEFAULT_LOCATION,
                                ),
                                arguments=[
                                    ArgumentNode(
                                        name=NameNode(
                                            value="nullArg",
                                            location=_EXPECTED_DEFAULT_LOCATION,
                                        ),
                                        value=NullValueNode(
                                            location=_EXPECTED_DEFAULT_LOCATION
                                        ),
                                        location=_EXPECTED_DEFAULT_LOCATION,
                                    )
                                ],
                                location=_EXPECTED_DEFAULT_LOCATION,
                            ),
                            DirectiveNode(
                                name=NameNode(
                                    value="secondDirective",
                                    location=_EXPECTED_DEFAULT_LOCATION,
                                ),
                                arguments=[],
                                location=_EXPECTED_DEFAULT_LOCATION,
                            ),
                        ],
                        selection_set=SelectionSetNode(
                            selections=[
                                FragmentSpreadNode(
                                    name=NameNode(
                                        value="spreadedFragment",
                                        location=_EXPECTED_DEFAULT_LOCATION,
                                    ),
                                    directives=[],
                                    location=_EXPECTED_DEFAULT_LOCATION,
                                )
                            ],
                            location=_EXPECTED_DEFAULT_LOCATION,
                        ),
                        location=_EXPECTED_DEFAULT_LOCATION,
                    ),
                ],
                location=_EXPECTED_DEFAULT_LOCATION,
            ),
        ),
    ],
)
def test_document_from_ast_json(json_ast, expected):
    assert document_from_ast_json(json_ast) == expected
