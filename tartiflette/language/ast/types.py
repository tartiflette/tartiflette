from typing import Optional, Union

from tartiflette.language.ast.base import TypeNode


class ListTypeNode(TypeNode):
    """
    TODO:
    """

    __slots__ = ("type", "location")

    def __init__(
        self,
        type: Union["NamedTypeNode", "NonNullTypeNode"],
        location: Optional["Location"] = None,
    ) -> None:
        """
        TODO:
        :param type: TODO:
        :param location: TODO:
        :type type: TODO:
        :type location: TODO:
        """
        # pylint: disable=redefined-builtin
        self.type = type
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
            isinstance(other, ListTypeNode)
            and (self.type == other.type and self.location == other.location)
        )

    def __repr__(self) -> str:
        """
        TODO:
        :return: TODO:
        :rtype: TODO:
        """
        return "ListTypeNode(type=%r, location=%r)" % (
            self.type,
            self.location,
        )


class NonNullTypeNode(TypeNode):
    """
    TODO:
    """

    __slots__ = ("type", "location")

    def __init__(
        self,
        type: Union["NamedTypeNode", "ListTypeNode"],
        location: Optional["Location"] = None,
    ) -> None:
        """
        TODO:
        :param type: TODO:
        :param location: TODO:
        :type type: TODO:
        :type location: TODO:
        """
        # pylint: disable=redefined-builtin
        self.type = type
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
            isinstance(other, NonNullTypeNode)
            and (self.type == other.type and self.location == other.location)
        )

    def __repr__(self) -> str:
        """
        TODO:
        :return: TODO:
        :rtype: TODO:
        """
        return "NonNullTypeNode(type=%r, location=%r)" % (
            self.type,
            self.location,
        )
