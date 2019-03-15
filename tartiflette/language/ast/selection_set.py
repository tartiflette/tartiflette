from typing import Any, List, Optional

from tartiflette.language.ast.base import Node


class SelectionSetNode(Node):
    """
    TODO:
    """

    __slots__ = ("selections", "location")

    def __init__(
        self,
        selections: List["SelectionNode"],
        location: Optional["Location"] = None,
    ) -> None:
        """
        TODO:
        :param selections: TODO:
        :param location: TODO:
        :type selections: List["SelectionNode"]
        :type location: Optional[Location]
        """
        self.selections = selections
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
            isinstance(other, SelectionSetNode)
            and (
                self.selections == other.selections
                and self.location == other.location
            )
        )

    def __repr__(self) -> str:
        """
        TODO:
        :return: TODO:
        :rtype: str
        """
        return "SelectionSetNode(selections=%r, location=%r)" % (
            self.selections,
            self.location,
        )
