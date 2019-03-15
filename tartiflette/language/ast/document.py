from typing import Any, List, Optional

from tartiflette.language.ast.base import Node


class DocumentNode(Node):
    """
    TODO:
    """

    __slots__ = ("definitions", "location")

    def __init__(
        self,
        definitions: List["DefinitionNode"],
        location: Optional["Location"] = None,
    ) -> None:
        """
        TODO:
        :param definitions: TODO:
        :param location: TODO:
        :type definitions: List[DefinitionNode]
        :type location: Optional[Location]
        """
        self.definitions = definitions
        self.location = location

    def __eq__(self, other: Any) -> bool:
        """
        TODO:
        :param other: TODO:
        :type other: Any
        :return: TODO:
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
        TODO:
        :return: TODO:
        :rtype: str
        """
        return "DocumentNode(definitions=%r, location=%r)" % (
            self.definitions,
            self.location,
        )
