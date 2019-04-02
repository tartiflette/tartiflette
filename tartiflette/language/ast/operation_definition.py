from typing import Any, List, Optional

from tartiflette.language.ast.base import ExecutableDefinitionNode


class OperationDefinitionNode(ExecutableDefinitionNode):
    """
    AST node representing a GraphQL operation definition.
    """

    __slots__ = (
        "operation_type",
        "name",
        "variable_definitions",
        "directives",
        "selection_set",
        "location",
    )

    def __init__(
        self,
        operation_type: str,
        selection_set: "SelectionSetNode",
        name: Optional["NameNode"] = None,
        variable_definitions: Optional[List["VariableDefinitionNode"]] = None,
        directives: Optional[List["DirectiveNode"]] = None,
        location: Optional["Location"] = None,
    ) -> None:
        """
        :param operation_type: operation type of the operation definition
        :param selection_set: selection set of the operation definition
        :param name: name of the operation definition
        :param variable_definitions: variable definitions of the operation
        definition
        :param directives: directives of the operation definition
        :param location: location of the operation definition in the query/SDL
        :type operation_type: str
        :type selection_set: SelectionSetNode
        :type name: Optional[NameNode]
        :type variable_definitions: Optional[List[VariableDefinitionNode]]
        :type directives: Optional[List[DirectiveNode]]
        :type location: Optional[Location]
        """
        self.operation_type = operation_type
        self.selection_set = selection_set
        self.name = name
        self.variable_definitions = variable_definitions
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
            isinstance(other, OperationDefinitionNode)
            and (
                self.operation_type == other.operation_type
                and self.name == other.name
                and self.variable_definitions == other.variable_definitions
                and self.directives == other.directives
                and self.selection_set == other.selection_set
                and self.location == other.location
            )
        )

    def __repr__(self) -> str:
        """
        Returns the representation of an OperationDefinitionNode instance.
        :return: the representation of an OperationDefinitionNode instance
        :rtype: str
        """
        return (
            "OperationDefinitionNode(operation_type=%r, name=%r, "
            "variable_definitions=%r, directives=%r, selection_set=%r, "
            "location=%r)"
            % (
                self.operation_type,
                self.name,
                self.variable_definitions,
                self.directives,
                self.selection_set,
                self.location,
            )
        )
