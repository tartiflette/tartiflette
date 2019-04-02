from typing import Any, List, Optional

from tartiflette.language.ast.base import Node


class DocumentNode(Node):
    """
    AST node representing a GraphQL document.
    """

    __slots__ = ("definitions", "location")

    def __init__(
        self,
        definitions: List["DefinitionNode"],
        location: Optional["Location"] = None,
    ) -> None:
        """
        :param definitions: definitions of the document
        :param location: location of the document in the query/SDL
        :type definitions: List[DefinitionNode]
        :type location: Optional[Location]
        """
        self.definitions = definitions
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
            isinstance(other, DocumentNode)
            and (
                self.definitions == other.definitions
                and self.location == other.location
            )
        )

    def __repr__(self) -> str:
        """
        Returns the representation of a DocumentNode instance.
        :return: the representation of a DocumentNode instance
        :rtype: str
        """
        return "DocumentNode(definitions=%r, location=%r)" % (
            self.definitions,
            self.location,
        )
