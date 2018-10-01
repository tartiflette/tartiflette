import pytest

from tartiflette.executors.types import Info
from tartiflette.types.exceptions.tartiflette import InvalidValue
from tartiflette.types.scalar import GraphQLScalarType


def test_graphql_scalar_init():
    scalar = GraphQLScalarType(name="Name", description="description")

    assert scalar.name == "Name"
    assert scalar.coerce_output is None
    assert scalar.coerce_input is None
    assert scalar.description == "description"


def test_graphql_scalar_repr():
    scalar = GraphQLScalarType(name="Name", description="description")

    assert (
        scalar.__repr__() == "GraphQLScalarType(name='Name', "
        "description='description')"
    )
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
