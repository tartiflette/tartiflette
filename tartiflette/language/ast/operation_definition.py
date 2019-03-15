from typing import List, Optional

from tartiflette.language.ast.base import DefinitionNode


class OperationDefinitionNode(DefinitionNode):
    """
    TODO:
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
        TODO:
        :param operation_type: TODO:
        :param selection_set: TODO:
        :param name: TODO:
        :param variable_definitions: TODO:
        :param directives: TODO:
        :param location: TODO:
        :type operation_type: TODO:
        :type selection_set: TODO:
        :type name: TODO:
        :type variable_definitions: TODO:
        :type directives: TODO:
        :type location: TODO:
        """
        self.operation_type = operation_type
        self.selection_set = selection_set
        self.name = name
        self.variable_definitions = variable_definitions
        self.directives = directives
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
        TODO:
        :return: TODO:
        :rtype: TODO:
        """
        return (
            "OperationDefinitionNode(operation_type=%r, name=%r, variable_definitions=%r, directives=%r, selection_set=%r, location=%r)"
            % (
                self.operation_type,
                self.name,
                self.variable_definitions,
                self.directives,
                self.selection_set,
                self.location,
            )
        )
