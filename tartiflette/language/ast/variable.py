from typing import Any, Optional

from tartiflette.language.ast.base import ValueNode


class VariableNode(ValueNode):
    """
    AST node representing a GraphQL variable.
    """

    __slots__ = ("name", "location")

    def __init__(
        self, name: "NameNode", location: Optional["Location"] = None
    ) -> None:
        """
        :param name: name of the variable
        :param location: location of the variable in the query/SDL
        :type name: NameNode
        :type location: Optional[Location]
        """
        self.name = name
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
            isinstance(other, VariableNode)
            and (self.name == other.name and self.location == other.location)
        )

    def __repr__(self) -> str:
        """
        Returns the representation of a VariableNode instance.
        :return: the representation of a VariableNode instance
        :rtype: str
        """
        return "VariableNode(name=%r, location=%r)" % (
            self.name,
            self.location,
        )
