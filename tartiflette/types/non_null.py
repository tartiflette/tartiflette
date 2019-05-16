from typing import Any

from tartiflette.types.type import GraphQLWrappingType

__all__ = ("GraphQLNonNull",)


class GraphQLNonNull(GraphQLWrappingType):
    """
    Definition of a GraphQL non-null container.
    """

    is_non_null_type = True

    # Introspection attributes
    kind = "NON_NULL"

    def __eq__(self, other: Any) -> bool:
        """
        Returns True if `other` instance is identical to `self`.
        :param other: object instance to compare to `self`
        :type other: Any
        :return: whether or not `other` is identical to `self`
        :rtype: bool
        """
        return self is other or (
            isinstance(other, GraphQLNonNull)
            and self.gql_type == other.gql_type
        )

    def __repr__(self) -> str:
        """
        Returns the representation of a GraphQLNonNull instance.
        :return: the representation of a GraphQLNonNull instance
        :rtype: str
        """
        return "GraphQLNonNull(gql_type={!r})".format(self.gql_type)

    def __str__(self) -> str:
        """
        Returns a human-readable representation of the non-null type.
        :return: a human-readable representation of the non-null type
        :rtype: str
        """
        return "{!s}!".format(self.gql_type)
