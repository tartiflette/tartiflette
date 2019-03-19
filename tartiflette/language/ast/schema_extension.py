from typing import Any, List, Optional

from tartiflette.language.ast.base import TypeSystemExtensionNode


class SchemaExtensionNode(TypeSystemExtensionNode):
    """
    AST node representing a GraphQL schema extension.
    """

    __slots__ = ("directives", "operation_type_definitions", "location")

    def __init__(
        self,
        directives: Optional[List["DirectiveNode"]] = None,
        operation_type_definitions: Optional[
            List["OperationTypeDefinitionNode"]
        ] = None,
        location: Optional["Location"] = None,
    ) -> None:
        """
        :param directives: directives of the schema extension
        :param operation_type_definitions: operation type definitions of the
        schema extension
        :param location: location of the schema extension in the query/SDL
        :type directives: Optional[List[DirectiveNode]]
        :type operation_type_definitions: Optional[List[OperationTypeDefinitionNode]]
        :type location: Optional[Location]
        """
        self.directives = directives
        self.operation_type_definitions = operation_type_definitions
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
            isinstance(other, SchemaExtensionNode)
            and (
                self.directives == other.directives
                and self.operation_type_definitions
                == other.operation_type_definitions
                and self.location == other.location
            )
        )

    def __repr__(self) -> str:
        """
        Returns the representation of a SchemaExtensionNode instance.
        :return: the representation of a SchemaExtensionNode instance
        :rtype: str
        """
        return (
            "SchemaExtensionNode(directives=%r, "
            "operation_type_definitions=%r, location=%r)"
            % (self.directives, self.operation_type_definitions, self.location)
        )
