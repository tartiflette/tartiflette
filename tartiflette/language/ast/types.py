from typing import Any, Optional, Union

from tartiflette.language.ast.base import TypeNode


class ListTypeNode(TypeNode):
    """
    AST node representing a GraphQL list type.
    """

    __slots__ = ("type", "location")

    def __init__(
        self,
        type: Union["NamedTypeNode", "NonNullTypeNode"],
        location: Optional["Location"] = None,
    ) -> None:
        """
        :param type: type of the list type
        :param location: location of the list type in the query/SDL
        :type type: Union[NamedTypeNode, NonNullTypeNode]
        :type location: Optional[Location]
        """
        # pylint: disable=redefined-builtin
        self.type = type
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
            isinstance(other, ListTypeNode)
            and (self.type == other.type and self.location == other.location)
        )

    def __repr__(self) -> str:
        """
        Returns the representation of a ListTypeNode instance.
        :return: the representation of a ListTypeNode instance
        :rtype: str
        """
        return "ListTypeNode(type=%r, location=%r)" % (
            self.type,
            self.location,
        )


class NonNullTypeNode(TypeNode):
    """
    AST node representing a GraphQL non null type.
    """

    __slots__ = ("type", "location")

    def __init__(
        self,
        type: Union["NamedTypeNode", "ListTypeNode"],
        location: Optional["Location"] = None,
    ) -> None:
        """
        :param type: type of the non null type
        :param location: location of the non null type in the query/SDL
        :type type: Union[NamedTypeNode, ListTypeNode]
        :type location: Optional[Location]
        """
        # pylint: disable=redefined-builtin
        self.type = type
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
            isinstance(other, NonNullTypeNode)
            and (self.type == other.type and self.location == other.location)
        )

    def __repr__(self) -> str:
        """
        Returns the representation of a NonNullTypeNode instance.
        :return: the representation of a NonNullTypeNode instance
        :rtype: str
        """
        return "NonNullTypeNode(type=%r, location=%r)" % (
            self.type,
            self.location,
        )
