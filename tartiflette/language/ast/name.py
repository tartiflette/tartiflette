from typing import Any, Optional

from tartiflette.language.ast.base import Node


class NameNode(Node):
    """
    AST node representing a GraphQL name.
    """

    __slots__ = ("value", "location")

    def __init__(
        self, value: str, location: Optional["Location"] = None
    ) -> None:
        """
        :param value: value of the name
        :param location: location of the name in the query/SDL
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
            isinstance(other, NameNode)
            and (self.value == other.value and self.location == other.location)
        )

    def __repr__(self) -> str:
        """
        Returns the representation of a NameNode instance.
        :return: the representation of a NameNode instance
        :rtype: str
        """
        return "NameNode(value=%r, location=%r)" % (self.value, self.location)
