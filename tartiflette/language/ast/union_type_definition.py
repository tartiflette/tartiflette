from typing import Any, List, Optional

from tartiflette.language.ast.base import TypeDefinitionNode
from tartiflette.language.ast.union_type_extension import (
    UnionTypeExtensionNode,
)

__all__ = ("UnionTypeDefinitionNode",)


class UnionTypeDefinitionNode(TypeDefinitionNode):
    """
    AST node representing a GraphQL union type definition.
    """

    __slots__ = ("description", "name", "directives", "types", "location")

    def __init__(
        self,
        name: "NameNode",
        description: Optional["DescriptionNode"] = None,
        directives: Optional[List["DirectiveNode"]] = None,
        types: Optional[List["NamedTypeNode"]] = None,
        location: Optional["Location"] = None,
    ) -> None:
        """
        :param name: name of the union type definition
        :param description: description of the union type definition
        :param directives: directives of the union type definition
        :param types: types of the union type definition
        :param location: location of the union type definition in the query/SDL
        :type name: NameNode
        :type description: Optional[DescriptionNode]
        :type directives: Optional[List[DirectiveNode]]
        :type types: Optional[List[NamedTypeNode]]
        :type location: Optional[Location]
        """
        self.name = name
        self.description = description
        self.directives = directives or []
        self.types = types or []
        self.location = location

    def __eq__(self, other: Any) -> bool:
        """
        Returns True if `other` instance is identical to `self`.
        :param other: object instance to compare to `self`
        :type other: Any
        :return: whether or not `other` is identical to `self`
        :rtype: bool
        """
        return self is other or (
            isinstance(other, UnionTypeDefinitionNode)
            and self.description == other.description
            and self.name == other.name
            and self.directives == other.directives
            and self.types == other.types
            and self.location == other.location
        )

    def __or__(self, extension: Any) -> "UnionTypeDefinitionNode":
        """
        Return a new union definition with elements from extension.

        :param extension: instance with which extend the union
        :type extension: Any
        :return: a new union definition with elements from extension
        :rtype: UnionTypeDefinitionNode
        """
        if isinstance(extension, UnionTypeExtensionNode):
            return UnionTypeDefinitionNode(
                name=self.name,
                description=self.description,
                directives=self.directives + extension.directives,
                types=self.types + extension.types,
                location=self.location,
            )
        return self

    def __repr__(self) -> str:
        """
        Returns the representation of an UnionTypeDefinitionNode instance.
        :return: the representation of an UnionTypeDefinitionNode instance
        :rtype: str
        """
        return (
            "UnionTypeDefinitionNode(description=%r, name=%r, directives=%r, "
            "types=%r, location=%r)"
            % (
                self.description,
                self.name,
                self.directives,
                self.types,
                self.location,
            )
        )
