from typing import Any, List, Optional

from tartiflette.language.ast.base import TypeSystemExtensionNode


class SchemaExtensionNode(TypeSystemExtensionNode):
    """
    TODO:
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
        TODO:
        :param directives: TODO:
        :param operation_type_definitions: TODO:
        :param location: TODO:
        :type directives: Optional[List[DirectiveNode]]
        :type operation_type_definitions: Optional[List[OperationTypeDefinitionNode]]
        :type location: Optional[Location]
        """
        self.directives = directives
        self.operation_type_definitions = operation_type_definitions
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
        TODO:
        :return: TODO:
        :rtype: str
        """
        return (
            "SchemaExtensionNode(directives=%r, operation_type_definitions=%r, location=%r)"
            % (self.directives, self.operation_type_definitions, self.location)
        )
