from typing import Optional, Union

from tartiflette.language.ast import (
    ListTypeNode,
    NamedTypeNode,
    NonNullTypeNode,
)
from tartiflette.types.list import GraphQLList
from tartiflette.types.non_null import GraphQLNonNull

__all__ = ("schema_type_from_ast",)


def schema_type_from_ast(
    schema: "GraphQLSchema",
    type_node: Union["ListTypeNode", "NonNullTypeNode", "NamedTypeNode"],
) -> Optional[Union["GraphQLList", "GraphQLNonNull", "GraphQLType"]]:
    """
    Given a Schema and an AST node describing a type, return a GraphQLType
    definition which applies to that type.
    :param schema: schema instance to use
    :param type_node: AST node describing a type
    :type schema: GraphQLSchema
    :type type_node: Union[ListTypeNode, NonNullTypeNode, NamedTypeNode]
    :return: a GraphQLType definition which applies to that type or None
    :rtype: Optional[Union[GraphQLList, GraphQLNonNull, GraphQLType]]
    """
    if isinstance(type_node, ListTypeNode):
        inner_type = schema_type_from_ast(schema, type_node.type)
        return GraphQLList(inner_type) if inner_type else None
    if isinstance(type_node, NonNullTypeNode):
        inner_type = schema_type_from_ast(schema, type_node.type)
        return GraphQLNonNull(inner_type) if inner_type else None
    if isinstance(type_node, NamedTypeNode):
        try:
            return schema.find_type(type_node.name.value)
        except KeyError:
            pass
        return None
    raise TypeError(f"Unexpected type kind: {type_node.__class__.__name__}")
