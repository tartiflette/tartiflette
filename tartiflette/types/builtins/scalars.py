
from tartiflette.types.scalar import GraphQLScalarType

GraphQLBoolean = GraphQLScalarType(name="Boolean", serialize=bool, deserialize=bool)

GraphQLFloat = GraphQLScalarType(name="Float", serialize=float, deserialize=float)

GraphQLID = GraphQLScalarType(name="ID", serialize=str, deserialize=str)

GraphQLInt = GraphQLScalarType(name="Int", serialize=int, deserialize=int)

GraphQLString = GraphQLScalarType(name="String", serialize=str, deserialize=str)
