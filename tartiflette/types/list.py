from typing import Any

from tartiflette.types.type import GraphQLWrappingType

__all__ = ("GraphQLList",)


class GraphQLList(GraphQLWrappingType):
    """
    Definition of a GraphQL list container.
    """

    is_list_type = True

    # Introspection attributes
    kind = "LIST"

    def __eq__(self, other: Any) -> bool:
        """
        Returns True if `other` instance is identical to `self`.
        :param other: object instance to compare to `self`
        :type other: Any
        :return: whether or not `other` is identical to `self`
        :rtype: bool
        """
        return self is other or (
            isinstance(other, GraphQLList) and self.gql_type == other.gql_type
        )

    def __repr__(self) -> str:
        """
        Returns the representation of a GraphQLList instance.
        :return: the representation of a GraphQLList instance
        :rtype: str
        """
        return "GraphQLList(gql_type={!r})".format(self.gql_type)

    def __str__(self) -> str:
        """
        Returns a human-readable representation of the list type.
        :return: a human-readable representation of the list type
        :rtype: str
        """
        return "[{!s}]".format(self.gql_type)
