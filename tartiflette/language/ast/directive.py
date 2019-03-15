from typing import List, Optional

from tartiflette.language.ast.base import Node


class DirectiveNode(Node):
    """
    TODO:
    """

    __slots__ = ("name", "arguments", "location")

    def __init__(
        self,
        name: "NameNode",
        arguments: Optional[List["ArgumentNode"]] = None,
        location: Optional["Location"] = None,
    ) -> None:
        """
        TODO:
        :param name: TODO:
        :param arguments: TODO:
        :param location: TODO:
        :type name: TODO:
        :type arguments: TODO:
        :type location: TODO:
        """
        self.name = name
        self.arguments = arguments
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
            isinstance(other, DirectiveNode)
            and (
                self.name == other.name
                and self.arguments == other.arguments
                and self.location == other.location
            )
        )

    def __repr__(self) -> str:
        """
        TODO:
        :return: TODO:
        :rtype: TODO:
        """
        return "DirectiveNode(name=%r, arguments=%r, location=%r)" % (
            self.name,
            self.arguments,
            self.location,
        )
