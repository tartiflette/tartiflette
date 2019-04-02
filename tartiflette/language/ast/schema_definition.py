from typing import Any, List, Optional

from tartiflette.language.ast.base import TypeSystemDefinitionNode


class SchemaDefinitionNode(TypeSystemDefinitionNode):
    """
    AST node representing a GraphQL schema definition.
    """

    __slots__ = ("directives", "operation_type_definitions", "location")

    def __init__(
        self,
        operation_type_definitions: List["OperationTypeDefinitionNode"],
        directives: Optional[List["DirectiveNode"]] = None,
        location: Optional["Location"] = None,
    ) -> None:
        """
        :param operation_type_definitions: operation type definitions of the
        schema definition
        :param directives: directives of the schema definition
        :param location: location of the schema definition in the query/SDL
        :type operation_type_definitions: List[OperationTypeDefinitionNode]
        :type directives: Optional[List[DirectiveNode]]
        :type location: Optional[Location]
        """
        self.operation_type_definitions = operation_type_definitions
        self.directives = directives
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
        Returns the representation of a SchemaDefinitionNode instance.
        :return: the representation of a SchemaDefinitionNode instance
        :rtype: str
        """
        return (
            "SchemaDefinitionNode(directives=%r, "
            "operation_type_definitions=%r, location=%r)"
            % (self.directives, self.operation_type_definitions, self.location)
        )
