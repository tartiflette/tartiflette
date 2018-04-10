
from tartiflette.types.scalar import GraphQLScalarType

GraphQLBoolean = GraphQLScalarType(name="Boolean", serializer=bool, deserializer=bool)

GraphQLFloat = GraphQLScalarType(name="Float", serializer=float, deserializer=float)

GraphQLID = GraphQLScalarType(name="ID", serializer=str, deserializer=str)

GraphQLInt = GraphQLScalarType(name="Int", serializer=int, deserializer=int)

GraphQLString = GraphQLScalarType(name="String", serializer=str, deserializer=str)
