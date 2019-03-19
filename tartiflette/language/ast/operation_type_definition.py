from typing import Any, Optional

from tartiflette.language.ast.base import Node


class OperationTypeDefinitionNode(Node):
    """
    AST node representing a GraphQL operation type definition.
    """

    __slots__ = ("operation_type", "type", "location")

    def __init__(
        self,
        operation_type: str,
        type: "NamedTypeNode",
        location: Optional["Location"] = None,
    ) -> None:
        """
        :param operation_type: operation type of the operation type definition
        :param type: type of the operation type definition
        :param location: location of the operation type definition in the
        query/SDL
        :type operation_type: str
        :type type: NamedTypeNode
        :type location: Optional[Location]
        """
        # pylint: disable=redefined-builtin
        self.operation_type = operation_type
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
            isinstance(other, OperationTypeDefinitionNode)
            and (
                self.operation_type == other.operation_type
                and self.type == other.type
                and self.location == other.location
            )
        )

    def __repr__(self) -> str:
        """
        Returns the representation of an OperationTypeDefinitionNode instance.
        :return: the representation of an OperationTypeDefinitionNode instance
        :rtype: str
        """
        return (
            "OperationTypeDefinitionNode(operation_type=%r, type=%r, "
            "location=%r)" % (self.operation_type, self.type, self.location)
        )
