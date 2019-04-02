from typing import Any, List, Optional

from tartiflette.language.ast.base import TypeExtensionNode


class UnionTypeExtensionNode(TypeExtensionNode):
    """
    AST node representing a GraphQL union type extension.
    """

    __slots__ = ("name", "directives", "types", "location")

    def __init__(
        self,
        name: "NameNode",
        directives: Optional[List["DirectiveNode"]] = None,
        types: Optional[List["NamedTypeNode"]] = None,
        location: Optional["Location"] = None,
    ) -> None:
        """
        :param name: name of the union type extension
        :param directives: directives of the union type extension
        :param types: types of the union type extension
        :param location: location of the union type extension in the query/SDL
        :type name: NameNode
        :type directives: Optional[List[DirectiveNode]]
        :type types: Optional[List[NamedTypeNode]]
        :type location: Optional[Location]
        """
        self.name = name
        self.directives = directives
        self.types = types
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
            isinstance(other, UnionTypeExtensionNode)
            and (
                self.name == other.name
                and self.directives == other.directives
                and self.types == other.types
                and self.location == other.location
            )
        )

    def __repr__(self) -> str:
        """
        Returns the representation of an UnionTypeExtensionNode instance.
        :return: the representation of an UnionTypeExtensionNode instance
        :rtype: str
        """
        return (
            "UnionTypeExtensionNode(name=%r, directives=%r, types=%r, "
            "location=%r)"
            % (self.name, self.directives, self.types, self.location)
        )
