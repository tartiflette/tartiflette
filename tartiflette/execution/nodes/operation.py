from typing import Any, Dict

from tartiflette.execution.execute import (
    execute_fields,
    execute_fields_serially,
)

__all__ = ["ExecutableOperationNode"]


class ExecutableOperationNode:
    """
    Node representing a GraphQL executable operation.
    """

    def __init__(
        self,
        name: str,
        operation_type: str,
        fields: Dict[str, "ExecutableFieldNode"],
        definition: "OperationDefinitionNode",
    ) -> None:
        """
        :param name: name of the operation
        :param operation_type: operation type of the operation
        :param fields: collected executable fields of the operation
        :param definition: operation definition node of the operation
        :type name: str
        :type operation_type: str
        :type fields: Dict[str, ExecutableFieldNode]
        :type definition: OperationDefinitionNode
        """
        self.name = name
        self.type = operation_type
        self.fields = fields
        self.definition = definition
        self.allow_parallelization: bool = operation_type != "mutation"

        # TODO: retrocompatibility old execution style
        self.children = fields

    def __repr__(self) -> str:
        """
        Returns the representation of an ExecutableOperationNode instance.
        :return: the representation of an ExecutableOperationNode instance
        :rtype: str
        """
        return (
            "ExecutableOperationNode(name=%r, operation_type=%r, fields=%r, "
            "definition=%r)"
            % (self.name, self.type, self.fields, self.definition)
        )

    async def __call__(
        self, execution_context: "ExecutionContext"
    ) -> Dict[str, Any]:
        """
        TODO:
        :param execution_context: TODO:
        :type execution_context: TODO:
        :return: TODO:
        :rtype: TODO:
        """
        operation_type_name = execution_context.schema.get_operation_type(
            self.type.capitalize()
        )

        return await (
            execute_fields(execution_context, self.fields, operation_type_name)
            if self.allow_parallelization
            else execute_fields_serially(
                execution_context, self.fields, operation_type_name
            )
        )
