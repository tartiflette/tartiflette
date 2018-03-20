# from typing import Union
#
# from .enum_type import GraphQLEnumTypeDefinition
# from .input_object_type import GraphQLInputObjectTypeDefinition
# from .interface_type import GraphQLInterfaceTypeDefinition
# from .object_type import GraphQLObjectTypeDefinition
# from .scalar_type import GraphQLScalarTypeDefinition
# from .union_type import GraphQLUnionTypeDefinition
#
# from .list_type import GraphQLListType
# from .non_null_type import GraphQLNonNullType
#
#
# GraphQLType = Union[
#     GraphQLEnumTypeDefinition,
#     GraphQLInputObjectTypeDefinition,
#     GraphQLInterfaceTypeDefinition,
#     GraphQLObjectTypeDefinition,
#     GraphQLScalarTypeDefinition,
#     GraphQLUnionTypeDefinition,
#
#     GraphQLListType,
#     GraphQLNonNullType,
# ]
#
# GraphQLInputType = Union[
#     GraphQLScalarTypeDefinition,
#     GraphQLEnumTypeDefinition,
#     GraphQLInputObjectTypeDefinition,
#     GraphQLListType,
#     GraphQLNonNullType,
# ]
#
# GraphQLOutputType = Union[
#     GraphQLScalarTypeDefinition,
#     GraphQLObjectTypeDefinition,
#     GraphQLInterfaceTypeDefinition,
#     GraphQLUnionTypeDefinition,
#     GraphQLEnumTypeDefinition,
#     GraphQLListType,
#     GraphQLNonNullType,
# ]
#
# GraphQLLeafType = Union[
#     GraphQLScalarTypeDefinition,
#     GraphQLEnumTypeDefinition,
# ]
#
# GraphQLCompositeType = Union[
#     GraphQLObjectTypeDefinition,
#     GraphQLInterfaceTypeDefinition,
#     GraphQLUnionTypeDefinition,
# ]
#
# GraphQLAbstractType = Union[
#     GraphQLInterfaceTypeDefinition,
#     GraphQLUnionTypeDefinition,
# ]
#
# GraphQLWrappingType = Union[
#     GraphQLListType,
#     GraphQLNonNullType,
# ]
#
# GraphQLNullableType = Union[
#     GraphQLScalarTypeDefinition,
#     GraphQLObjectTypeDefinition,
#     GraphQLInterfaceTypeDefinition,
#     GraphQLUnionTypeDefinition,
#     GraphQLEnumTypeDefinition,
#     GraphQLInputObjectTypeDefinition,
#     GraphQLListType,
# ]
