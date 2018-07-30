from tartiflette.executors.types import Info
from tartiflette.types.scalar import GraphQLScalarType


def test_graphql_scalar_init():
    scalar = GraphQLScalarType(name="Name", description="description")

    assert scalar.name == "Name"
    assert scalar.coerce_output is None
    assert scalar.coerce_input is None
    assert scalar.description == "description"


def test_graphql_scalar_repr():
    scalar = GraphQLScalarType(name="Name", description="description")

    assert scalar.__repr__() == "GraphQLScalarType(name='Name', " \
                                "description='description')"
    assert scalar == eval(repr(scalar))


def test_graphql_scalar_eq():
    scalar = GraphQLScalarType(name="Name", description="description")

    ## Same
    assert scalar == scalar
    assert scalar == GraphQLScalarType(name="Name", description="description")
    # Currently we ignore the description in comparing
    assert scalar == GraphQLScalarType(name="Name")

    ## Different
    assert scalar != GraphQLScalarType(name="OtherName")


def test_graphql_scalar_coerce_value():
    scalar = GraphQLScalarType(name="Name", description="description",
                               coerce_input=int, coerce_output=int)

    info = Info(
        None, None, None, None, None
    )
    # Coercing None returns None
    coerced_value = scalar.coerce_value(None, info)
    assert coerced_value.value is None
    assert coerced_value.error is None

    # Coercing a float returns an int (int() worked)
    src_val = 42.0
    coerced_value = scalar.coerce_value(src_val, info)
    assert coerced_value.value == 42
    assert coerced_value.error is None

    # Coercing something unknown returns an empty dict
    coerced_value = scalar.coerce_value("invalid string", info)
    assert coerced_value.value is None
    assert coerced_value.error is not None
