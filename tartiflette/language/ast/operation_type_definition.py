from typing import Any, Optional

from tartiflette.language.ast.base import Node


class OperationTypeDefinitionNode(Node):
    """
    TODO:
    """

    __slots__ = ("operation_type", "type", "location")

    def __init__(
        self,
        operation_type: str,
        type: "NamedTypeNode",
        location: Optional["Location"] = None,
    ) -> None:
        """
        TODO:
        :param operation_type: TODO:
        :param type: TODO:
        :param location: TODO:
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
        TODO:
        :param other: TODO:
        :type other: Any
        :return: TODO:
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
        TODO:
        :return: TODO:
        :rtype: str
        """
        return (
            "OperationTypeDefinitionNode(operation_type=%r, type=%r, location=%r)"
            % (self.operation_type, self.type, self.location)
        )
