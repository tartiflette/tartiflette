
from tartiflette.types.scalar import GraphQLScalarType

GraphQLBoolean = GraphQLScalarType(
    name="Boolean", coerce_output=bool, coerce_input=bool
)

GraphQLFloat = GraphQLScalarType(
    name="Float", coerce_output=float, coerce_input=float
)

GraphQLID = GraphQLScalarType(name="ID", coerce_output=str, coerce_input=str)

GraphQLInt = GraphQLScalarType(name="Int", coerce_output=int, coerce_input=int)

GraphQLString = GraphQLScalarType(
    name="String", coerce_output=str, coerce_input=str
)
