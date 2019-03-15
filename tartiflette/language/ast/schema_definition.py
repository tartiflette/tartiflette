from typing import Any, List, Optional

from tartiflette.language.ast.base import TypeSystemDefinitionNode


class SchemaDefinitionNode(TypeSystemDefinitionNode):
    """
    TODO:
    """

    __slots__ = ("directives", "operation_type_definitions", "location")

    def __init__(
        self,
        operation_type_definitions: List["OperationTypeDefinitionNode"],
        directives: Optional[List["DirectiveNode"]] = None,
        location: Optional["Location"] = None,
    ) -> None:
        """
        TODO:
        :param operation_type_definitions: TODO:
        :param directives: TODO:
        :param location: TODO:
        :type operation_type_definitions: List[OperationTypeDefinitionNode]
        :type directives: Optional[List[DirectiveNode]]
        :type location: Optional[Location]
        """
        self.operation_type_definitions = operation_type_definitions
        self.directives = directives
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
            isinstance(other, SchemaDefinitionNode)
            and (
                self.directives == other.directives
                and self.operation_type_definitions
                == other.operation_type_definitions
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
            "SchemaDefinitionNode(directives=%r, operation_type_definitions=%r, location=%r)"
            % (self.directives, self.operation_type_definitions, self.location)
        )
