from typing import Any, Optional

from tartiflette.language.ast.base import ValueNode


class VariableNode(ValueNode):
    """
    TODO:
    """

    __slots__ = ("name", "location")

    def __init__(
        self, name: "NameNode", location: Optional["Location"] = None
    ) -> None:
        """
        TODO:
        :param name: TODO:
        :param location: TODO:
        :type name: NameNode
        :type location: Optional[Location]
        """
        self.name = name
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
            isinstance(other, VariableNode)
            and (self.name == other.name and self.location == other.location)
        )

    def __repr__(self) -> str:
        """
        TODO:
        :return: TODO:
        :rtype: str
        """
        return "VariableNode(name=%r, location=%r)" % (
            self.name,
            self.location,
        )
