import pytest

from tartiflette.language.ast import (
    BooleanValueNode,
    EnumValueNode,
    FloatValueNode,
    IntValueNode,
    ListValueNode,
    NullValueNode,
    ObjectFieldNode,
    ObjectValueNode,
    StringValueNode,
)


def test_booleanvaluenode__init__():
    boolean_value_node = BooleanValueNode(
        value="booleanValueValue", location="booleanValueLocation"
    )
    assert boolean_value_node.value == "booleanValueValue"
    assert boolean_value_node.location == "booleanValueLocation"


@pytest.mark.parametrize(
    "boolean_value_node,other,expected",
    [
        (
            BooleanValueNode(
                value="booleanValueValue", location="booleanValueLocation"
            ),
            Ellipsis,
            False,
        ),
        (
            BooleanValueNode(
                value="booleanValueValue", location="booleanValueLocation"
            ),
            BooleanValueNode(
                value="booleanValueValueBis", location="booleanValueLocation"
            ),
            False,
        ),
        (
            BooleanValueNode(
                value="booleanValueValue", location="booleanValueLocation"
            ),
            BooleanValueNode(
                value="booleanValueValue", location="booleanValueLocationBis"
            ),
            False,
        ),
        (
            BooleanValueNode(
                value="booleanValueValue", location="booleanValueLocation"
            ),
            BooleanValueNode(
                value="booleanValueValue", location="booleanValueLocation"
            ),
            True,
        ),
    ],
)
def test_booleanvaluenode__eq__(boolean_value_node, other, expected):
    assert (boolean_value_node == other) is expected


@pytest.mark.parametrize(
    "boolean_value_node,expected",
    [
        (
            BooleanValueNode(
                value="booleanValueValue", location="booleanValueLocation"
            ),
            "BooleanValueNode(value='booleanValueValue', "
            "location='booleanValueLocation')",
        )
    ],
)
def test_booleanvaluenode__repr__(boolean_value_node, expected):
    assert boolean_value_node.__repr__() == expected


def test_enumvaluenode__init__():
    enum_value_node = EnumValueNode(
        value="enumValueValue", location="enumValueLocation"
    )
    assert enum_value_node.value == "enumValueValue"
    assert enum_value_node.location == "enumValueLocation"


@pytest.mark.parametrize(
    "enum_value_node,other,expected",
    [
        (
            EnumValueNode(
                value="enumValueValue", location="enumValueLocation"
            ),
            Ellipsis,
            False,
        ),
        (
            EnumValueNode(
                value="enumValueValue", location="enumValueLocation"
            ),
            EnumValueNode(
                value="enumValueValueBis", location="enumValueLocation"
            ),
            False,
        ),
        (
            EnumValueNode(
                value="enumValueValue", location="enumValueLocation"
            ),
            EnumValueNode(
                value="enumValueValue", location="enumValueLocationBis"
            ),
            False,
        ),
        (
            EnumValueNode(
                value="enumValueValue", location="enumValueLocation"
            ),
            EnumValueNode(
                value="enumValueValue", location="enumValueLocation"
            ),
            True,
        ),
    ],
)
def test_enumvaluenode__eq__(enum_value_node, other, expected):
    assert (enum_value_node == other) is expected


@pytest.mark.parametrize(
    "enum_value_node,expected",
    [
        (
            EnumValueNode(
                value="enumValueValue", location="enumValueLocation"
            ),
            "EnumValueNode(value='enumValueValue', "
            "location='enumValueLocation')",
        )
    ],
)
def test_enumvaluenode__repr__(enum_value_node, expected):
    assert enum_value_node.__repr__() == expected


def test_floatvaluenode__init__():
    float_value_node = FloatValueNode(
        value="floatValueValue", location="floatValueLocation"
    )
    assert float_value_node.value == "floatValueValue"
    assert float_value_node.location == "floatValueLocation"


@pytest.mark.parametrize(
    "float_value_node,other,expected",
    [
        (
            FloatValueNode(
                value="floatValueValue", location="floatValueLocation"
            ),
            Ellipsis,
            False,
        ),
        (
            FloatValueNode(
                value="floatValueValue", location="floatValueLocation"
            ),
            FloatValueNode(
                value="floatValueValueBis", location="floatValueLocation"
            ),
            False,
        ),
        (
            FloatValueNode(
                value="floatValueValue", location="floatValueLocation"
            ),
            FloatValueNode(
                value="floatValueValue", location="floatValueLocationBis"
            ),
            False,
        ),
        (
            FloatValueNode(
                value="floatValueValue", location="floatValueLocation"
            ),
            FloatValueNode(
                value="floatValueValue", location="floatValueLocation"
            ),
            True,
        ),
    ],
)
def test_floatvaluenode__eq__(float_value_node, other, expected):
    assert (float_value_node == other) is expected


@pytest.mark.parametrize(
    "float_value_node,expected",
    [
        (
            FloatValueNode(
                value="floatValueValue", location="floatValueLocation"
            ),
            "FloatValueNode(value='floatValueValue', "
            "location='floatValueLocation')",
        )
    ],
)
def test_floatvaluenode__repr__(float_value_node, expected):
    assert float_value_node.__repr__() == expected


def test_intvaluenode__init__():
    int_value_node = IntValueNode(
        value="intValueValue", location="intValueLocation"
    )
    assert int_value_node.value == "intValueValue"
    assert int_value_node.location == "intValueLocation"


@pytest.mark.parametrize(
    "int_value_node,other,expected",
    [
        (
            IntValueNode(value="intValueValue", location="intValueLocation"),
            Ellipsis,
            False,
        ),
        (
            IntValueNode(value="intValueValue", location="intValueLocation"),
            IntValueNode(
                value="intValueValueBis", location="intValueLocation"
            ),
            False,
        ),
        (
            IntValueNode(value="intValueValue", location="intValueLocation"),
            IntValueNode(
                value="intValueValue", location="intValueLocationBis"
            ),
            False,
        ),
        (
            IntValueNode(value="intValueValue", location="intValueLocation"),
            IntValueNode(value="intValueValue", location="intValueLocation"),
            True,
        ),
    ],
)
def test_intvaluenode__eq__(int_value_node, other, expected):
    assert (int_value_node == other) is expected


@pytest.mark.parametrize(
    "int_value_node,expected",
    [
        (
            IntValueNode(value="intValueValue", location="intValueLocation"),
            "IntValueNode(value='intValueValue', "
            "location='intValueLocation')",
        )
    ],
)
def test_intvaluenode__repr__(int_value_node, expected):
    assert int_value_node.__repr__() == expected


def test_nullvaluenode__init__():
    null_value_node = NullValueNode(location="nullValueLocation")
    assert null_value_node.value is None
    assert null_value_node.location == "nullValueLocation"


@pytest.mark.parametrize(
    "null_value_node,other,expected",
    [
        (NullValueNode(location="nullValueLocation"), Ellipsis, False),
        (
            NullValueNode(location="nullValueLocation"),
            NullValueNode(location="nullValueLocationBis"),
            False,
        ),
        (
            NullValueNode(location="nullValueLocation"),
            NullValueNode(location="nullValueLocation"),
            True,
        ),
    ],
)
def test_nullvaluenode__eq__(null_value_node, other, expected):
    assert (null_value_node == other) is expected


@pytest.mark.parametrize(
    "null_value_node,expected",
    [
        (
            NullValueNode(location="nullValueLocation"),
            "NullValueNode(location='nullValueLocation')",
        )
    ],
)
def test_nullvaluenode__repr__(null_value_node, expected):
    assert null_value_node.__repr__() == expected


def test_stringvaluenode__init__():
    string_value_node = StringValueNode(
        value="stringValueValue", location="stringValueLocation"
    )
    assert string_value_node.value == "stringValueValue"
    assert string_value_node.location == "stringValueLocation"


@pytest.mark.parametrize(
    "string_value_node,other,expected",
    [
        (
            StringValueNode(
                value="stringValueValue", location="stringValueLocation"
            ),
            Ellipsis,
            False,
        ),
        (
            StringValueNode(
                value="stringValueValue", location="stringValueLocation"
            ),
            StringValueNode(
                value="stringValueValueBis", location="stringValueLocation"
            ),
            False,
        ),
        (
            StringValueNode(
                value="stringValueValue", location="stringValueLocation"
            ),
            StringValueNode(
                value="stringValueValue", location="stringValueLocationBis"
            ),
            False,
        ),
        (
            StringValueNode(
                value="stringValueValue", location="stringValueLocation"
            ),
            StringValueNode(
                value="stringValueValue", location="stringValueLocation"
            ),
            True,
        ),
    ],
)
def test_stringvaluenode__eq__(string_value_node, other, expected):
    assert (string_value_node == other) is expected


@pytest.mark.parametrize(
    "string_value_node,expected",
    [
        (
            StringValueNode(
                value="stringValueValue", location="stringValueLocation"
            ),
            "StringValueNode(value='stringValueValue', "
            "location='stringValueLocation')",
        )
    ],
)
def test_stringvaluenode__repr__(string_value_node, expected):
    assert string_value_node.__repr__() == expected


def test_listvaluenode__init__():
    list_value_node = ListValueNode(
        values="listValueValues", location="listValueLocation"
    )
    assert list_value_node.values == "listValueValues"
    assert list_value_node.location == "listValueLocation"


@pytest.mark.parametrize(
    "list_value_node,other,expected",
    [
        (
            ListValueNode(
                values="listValueValues", location="listValueLocation"
            ),
            Ellipsis,
            False,
        ),
        (
            ListValueNode(
                values="listValueValues", location="listValueLocation"
            ),
            ListValueNode(
                values="listValueValuesBis", location="listValueLocation"
            ),
            False,
        ),
        (
            ListValueNode(
                values="listValueValues", location="listValueLocation"
            ),
            ListValueNode(
                values="listValueValues", location="listValueLocationBis"
            ),
            False,
        ),
        (
            ListValueNode(
                values="listValueValues", location="listValueLocation"
            ),
            ListValueNode(
                values="listValueValues", location="listValueLocation"
            ),
            True,
        ),
    ],
)
def test_listvaluenode__eq__(list_value_node, other, expected):
    assert (list_value_node == other) is expected


@pytest.mark.parametrize(
    "list_value_node,expected",
    [
        (
            ListValueNode(
                values="listValueValues", location="listValueLocation"
            ),
            "ListValueNode(values='listValueValues', "
            "location='listValueLocation')",
        )
    ],
)
def test_listvaluenode__repr__(list_value_node, expected):
    assert list_value_node.__repr__() == expected


def test_objectfieldnode__init__():
    object_field_node = ObjectFieldNode(
        name="objectFieldName",
        value="objectFieldValue",
        location="objectFieldLocation",
    )
    assert object_field_node.name == "objectFieldName"
    assert object_field_node.value == "objectFieldValue"
    assert object_field_node.location == "objectFieldLocation"


@pytest.mark.parametrize(
    "object_field_node,other,expected",
    [
        (
            ObjectFieldNode(
                name="objectFieldName",
                value="objectFieldValue",
                location="objectFieldLocation",
            ),
            Ellipsis,
            False,
        ),
        (
            ObjectFieldNode(
                name="objectFieldName",
                value="objectFieldValue",
                location="objectFieldLocation",
            ),
            ObjectFieldNode(
                name="objectFieldNameBis",
                value="objectFieldValue",
                location="objectFieldLocation",
            ),
            False,
        ),
        (
            ObjectFieldNode(
                name="objectFieldName",
                value="objectFieldValue",
                location="objectFieldLocation",
            ),
            ObjectFieldNode(
                name="objectFieldName",
                value="objectFieldValueBis",
                location="objectFieldLocation",
            ),
            False,
        ),
        (
            ObjectFieldNode(
                name="objectFieldName",
                value="objectFieldValue",
                location="objectFieldLocation",
            ),
            ObjectFieldNode(
                name="objectFieldName",
                value="objectFieldValue",
                location="objectFieldLocationBis",
            ),
            False,
        ),
        (
            ObjectFieldNode(
                name="objectFieldName",
                value="objectFieldValue",
                location="objectFieldLocation",
            ),
            ObjectFieldNode(
                name="objectFieldName",
                value="objectFieldValue",
                location="objectFieldLocation",
            ),
            True,
        ),
    ],
)
def test_objectfieldnode__eq__(object_field_node, other, expected):
    assert (object_field_node == other) is expected


@pytest.mark.parametrize(
    "object_field_node,expected",
    [
        (
            ObjectFieldNode(
                name="objectFieldName",
                value="objectFieldValue",
                location="objectFieldLocation",
            ),
            "ObjectFieldNode(name='objectFieldName', "
            "value='objectFieldValue', location='objectFieldLocation')",
        )
    ],
)
def test_objectfieldnode__repr__(object_field_node, expected):
    assert object_field_node.__repr__() == expected


def test_objectvaluenode__init__():
    object_value_node = ObjectValueNode(
        fields="objectValueFields", location="objectValueLocation"
    )
    assert object_value_node.fields == "objectValueFields"
    assert object_value_node.location == "objectValueLocation"


@pytest.mark.parametrize(
    "object_value_node,other,expected",
    [
        (
            ObjectValueNode(
                fields="objectValueFields", location="objectValueLocation"
            ),
            Ellipsis,
            False,
        ),
        (
            ObjectValueNode(
                fields="objectValueFields", location="objectValueLocation"
            ),
            ObjectValueNode(
                fields="objectValueFieldsBis", location="objectValueLocation"
            ),
            False,
        ),
        (
            ObjectValueNode(
                fields="objectValueFields", location="objectValueLocation"
            ),
            ObjectValueNode(
                fields="objectValueFields", location="objectValueLocationBis"
            ),
            False,
        ),
        (
            ObjectValueNode(
                fields="objectValueFields", location="objectValueLocation"
            ),
            ObjectValueNode(
                fields="objectValueFields", location="objectValueLocation"
            ),
            True,
        ),
    ],
)
def test_objectvaluenode__eq__(object_value_node, other, expected):
    assert (object_value_node == other) is expected


@pytest.mark.parametrize(
    "object_value_node,expected",
    [
        (
            ObjectValueNode(
                fields="objectValueFields", location="objectValueLocation"
            ),
            "ObjectValueNode(fields='objectValueFields', "
            "location='objectValueLocation')",
        )
    ],
)
def test_objectvaluenode__repr__(object_value_node, expected):
    assert object_value_node.__repr__() == expected
