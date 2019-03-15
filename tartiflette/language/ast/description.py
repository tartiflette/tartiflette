from typing import Any, Optional

from tartiflette.language.ast.base import Node


class DescriptionNode(Node):
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
        :type value: str
        :type location: Optional[Location]
        """
        self.value = value
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
            isinstance(other, DescriptionNode)
            and (self.value == other.value and self.location == other.location)
        )

    def __repr__(self) -> str:
        """
        TODO:
        :return: TODO:
        :rtype: str
        """
        return "DescriptionNode(value=%r, location=%r)" % (
            self.value,
            self.location,
        )
