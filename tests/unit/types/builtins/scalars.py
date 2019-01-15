from tartiflette.types.builtins import (
    GraphQLBoolean,
    GraphQLFloat,
    GraphQLID,
    GraphQLInt,
    GraphQLString,
)
from tartiflette.types.scalar import GraphQLScalarType


def test_scalar_boolean():
    var_bool = GraphQLBoolean

    assert isinstance(var_bool, GraphQLScalarType)
    assert var_bool.name == "Boolean"


def test_scalar_float():
    var_float = GraphQLFloat

    assert isinstance(var_float, GraphQLScalarType)
    assert var_float.name == "Float"


def test_scalar_id():
    var_id = GraphQLID

    assert isinstance(var_id, GraphQLScalarType)
    assert var_id.name == "ID"


def test_scalar_int():
    var_int = GraphQLInt

    assert isinstance(var_int, GraphQLScalarType)
    assert var_int.name == "Int"


def test_scalar_string():
    var_string = GraphQLString

    assert isinstance(var_string, GraphQLScalarType)
    assert var_string.name == "String"
