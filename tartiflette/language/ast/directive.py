from typing import Any, List, Optional

from tartiflette.language.ast.base import Node


class DirectiveNode(Node):
    """
    AST node representing a GraphQL directive.
    """

    __slots__ = ("name", "arguments", "location")

    def __init__(
        self,
        name: "NameNode",
        arguments: Optional[List["ArgumentNode"]] = None,
        location: Optional["Location"] = None,
    ) -> None:
        """
        :param name: name of the directive
        :param arguments: arguments of the directive
        :param location: location of the directive in the query/SDL
        :type name: NameNode
        :type arguments: Optional[List[ArgumentNode]]
        :type location: Optional[Location]
        """
        self.name = name
        self.arguments = arguments
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
            isinstance(other, DirectiveNode)
            and (
                self.name == other.name
                and self.arguments == other.arguments
                and self.location == other.location
            )
        )

    def __repr__(self) -> str:
        """
        Returns the representation of a DirectiveNode instance.
        :return: the representation of a DirectiveNode instance
        :rtype: str
        """
        return "DirectiveNode(name=%r, arguments=%r, location=%r)" % (
            self.name,
            self.arguments,
            self.location,
        )
