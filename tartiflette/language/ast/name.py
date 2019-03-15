from typing import Optional

from tartiflette.language.ast.base import Node


class NameNode(Node):
    """
    TODO:
    """

    __slots__ = ("value", "location")

    def __init__(
        self, value: str, location: Optional["Location"] = None
    ) -> None:
        """
        TODO:
        :param value: TODO:
        :param location: TODO:
        :type value: TODO:
        :type location: TODO:
        """
        self.value = value
        self.location = location

    def __eq__(self, other):
        """
        TODO:
        :param other: TODO:
        :type other: TODO:
        :return: TODO:
        :rtype: TODO:
        """
        return self is other or (
            isinstance(other, NameNode)
            and (self.value == other.value and self.location == other.location)
        )

    def __repr__(self) -> str:
        """
        TODO:
        :return: TODO:
        :rtype: TODO:
        """
        return "NameNode(value=%r, location=%r)" % (self.value, self.location)
