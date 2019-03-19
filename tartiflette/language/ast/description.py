from typing import Any, Optional

from tartiflette.language.ast.base import Node


class DescriptionNode(Node):
    """
    AST node representing a GraphQL description.
    """

    __slots__ = ("value", "location")

    def __init__(
        self, value: str, location: Optional["Location"] = None
    ) -> None:
        """
        :param value: value of the description
        :param location: location of the description in the query/SDL
        :type value: str
        :type location: Optional[Location]
        """
        self.value = value
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
            isinstance(other, DescriptionNode)
            and (self.value == other.value and self.location == other.location)
        )

    def __repr__(self) -> str:
        """
        Returns the representation of a DescriptionNode instance.
        :return: the representation of a DescriptionNode instance
        :rtype: str
        """
        return "DescriptionNode(value=%r, location=%r)" % (
            self.value,
            self.location,
        )
