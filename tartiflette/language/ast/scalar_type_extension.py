from typing import Any, List, Optional

from tartiflette.language.ast.base import TypeExtensionNode


class ScalarTypeExtensionNode(TypeExtensionNode):
    """
    AST node representing a GraphQL scalar type extension.
    """

    __slots__ = ("name", "directives", "location")

    def __init__(
        self,
        name: "NameNode",
        directives: List["DirectiveNode"],
        location: Optional["Location"] = None,
    ) -> None:
        """
        :param name: name of the scalar type extension
        :param directives: directives of the scalar type extension
        :param location: location of the scalar type extension in the query/SDL
        :type name: NameNode
        :type directives: List[DirectiveNode]
        :type location: Optional[Location]
        """
        self.name = name
        self.directives = directives
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
            isinstance(other, ScalarTypeExtensionNode)
            and (
                self.name == other.name
                and self.directives == other.directives
                and self.location == other.location
            )
        )

    def __repr__(self) -> str:
        """
        Returns the representation of a ScalarTypeExtensionNode instance.
        :return: the representation of a ScalarTypeExtensionNode instance
        :rtype: str
        """
        return (
            "ScalarTypeExtensionNode(name=%r, directives=%r, location=%r)"
            % (self.name, self.directives, self.location)
        )
