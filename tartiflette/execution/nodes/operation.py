from typing import Dict, List, Optional


class ExecutableOperationNode:
    """
    Node representing a GraphQL executable operation.
    """

    def __init__(
        self,
        name: str,
        operation_type: str,
        variable_definitions: Optional[List["VariableDefinitionNode"]],
        fields: Dict[str, "ExecutableFieldNode"],
        definition: "OperationDefinitionNode",
    ) -> None:
        """
        :param name: name of the operation
        :param operation_type: operation type of the operation
        :param variable_definitions: variable definitions of the operation
        :param fields: collected executable fields of the operation
        :param definition: operation definition node of the operation
        :type name: str
        :type operation_type: str
        :type variable_definitions: Optional[List[VariableDefinitionNode]]
        :type fields: Dict[str, ExecutableFieldNode]
        :type definition: OperationDefinitionNode
        """
        self.name = name
        self.type = operation_type
        self.variable_definitions = variable_definitions
        self.fields = fields
        self.definition = definition
        self.allow_parallelization: bool = operation_type != "mutation"

    def __repr__(self) -> str:
        """
        Returns the representation of an ExecutableOperationNode instance.
        :return: the representation of an ExecutableOperationNode instance
        :rtype: str
        """
        return (
            "ExecutableOperationNode(name=%r, operation_type=%r, "
            "variable_definitions=%r, fields=%r, definition=%r)"
            % (
                self.name,
                self.type,
                self.variable_definitions,
                self.fields,
                self.definition,
            )
        )
