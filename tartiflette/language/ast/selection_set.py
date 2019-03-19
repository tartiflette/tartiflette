from typing import Any, List, Optional

from tartiflette.language.ast.base import Node


class SelectionSetNode(Node):
    """
    AST node representing a GraphQL selection set.
    """

    __slots__ = ("selections", "location")

    def __init__(
        self,
        selections: List["SelectionNode"],
        location: Optional["Location"] = None,
    ) -> None:
        """
        :param selections: selections of the selection set
        :param location: location of the selection set in the query/SDL
        :type selections: List["SelectionNode"]
        :type location: Optional[Location]
        """
        self.selections = selections
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
            isinstance(other, SelectionSetNode)
            and (
                self.selections == other.selections
                and self.location == other.location
            )
        )

    def __repr__(self) -> str:
        """
        Returns the representation of a SelectionSetNode instance.
        :return: the representation of a SelectionSetNode instance
        :rtype: str
        """
        return "SelectionSetNode(selections=%r, location=%r)" % (
            self.selections,
            self.location,
        )
