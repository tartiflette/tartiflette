from typing import Optional

from tartiflette.language.ast.base import Node


class ArgumentNode(Node):
    """
    TODO:
    """

    __slots__ = ("name", "value", "location")

    def __init__(
        self,
        name: "NameNode",
        value: "ValueNode",
        location: Optional["Location"] = None,
    ) -> None:
        """
        TODO:
        :param name: TODO:
        :param value: TODO:
        :param location: TODO:
        :type name: TODO:
        :type value: TODO:
        :type location: TODO:
        """
        self.name = name
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
            isinstance(other, ArgumentNode)
            and (
                self.name == other.name
                and self.value == other.value
                and self.location == other.location
            )
        )

    def __repr__(self) -> str:
        """
        TODO:
        :return: TODO:
        :rtype: TODO:
        """
        return "ArgumentNode(name=%r, value=%r, location=%r)" % (
            self.name,
            self.value,
            self.location,
        )
