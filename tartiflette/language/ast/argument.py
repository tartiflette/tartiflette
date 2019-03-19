from typing import Any, Optional

from tartiflette.language.ast.base import Node


class ArgumentNode(Node):
    """
    AST node representing a GraphQL argument.
    """

    __slots__ = ("name", "value", "location")

    def __init__(
        self,
        name: "NameNode",
        value: "ValueNode",
        location: Optional["Location"] = None,
    ) -> None:
        """
        :param name: name of the argument
        :param value: value of the argument
        :param location: location of the argument in the query/SDL
        :type name: NameNode
        :type value: ValueNode
        :type location: Optional[Location]
        """
        self.name = name
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
            isinstance(other, ArgumentNode)
            and (
                self.name == other.name
                and self.value == other.value
                and self.location == other.location
            )
        )

    def __repr__(self) -> str:
        """
        Returns the representation of an ArgumentNode instance.
        :return: the representation of an ArgumentNode instance
        :rtype: str
        """
        return "ArgumentNode(name=%r, value=%r, location=%r)" % (
            self.name,
            self.value,
            self.location,
        )
