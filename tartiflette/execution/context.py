from typing import Any, Dict, List, Optional, Tuple

from tartiflette.execution.values import get_variable_values
from tartiflette.language.ast import (
    FragmentDefinitionNode,
    OperationDefinitionNode,
)
from tartiflette.types.exceptions import GraphQLError

__all__ = ["build_execution_context"]


class ExecutionContext:
    """
    TODO:
    """

    def __init__(
        self,
        schema: "GraphQLSchema",
        fragments: Dict[str, "FragmentDefinitionNode"],
        operation: "ExecutableOperationNode",
        context: Optional[Any],
        root_value: Optional[Any],
        variable_values: Optional[Dict[str, Any]],
    ) -> None:
        """
        :param schema: TODO:
        :param fragments: TODO:
        :param operation: TODO:
        :param context: TODO:
        :param root_value: TODO:
        :param variable_values: TODO:
        :type schema: TODO:
        :type fragments: TODO:
        :type operation: TODO:
        :type context: TODO:
        :type root_value: TODO:
        :type variable_values: TODO:
        """
        self.schema = schema
        self.fragments = fragments
        self.operation = operation
        self.context = context
        self.root_value = root_value
        self.variable_values = variable_values
        self.errors = []

        # TODO: retrocompatibility
        self.is_introspection: bool = False

    def add_error(self, error: Exception) -> None:
        """
        TODO:
        :param error: TODO:
        :type error: TODO:
        :return: TODO:
        :rtype: TODO:
        """
        self.errors.append(error)


def build_execution_context(
    schema: "GraphQLSchema",
    document: "DocumentNode",
    root_value: Optional[Any],
    context: Optional[Any],
    raw_variable_values: Optional[Dict[str, Any]],
    operation_name: str,
) -> Tuple[Optional["ExecutionContext"], Optional[List["GraphQLError"]]]:
    """
    TODO:
    :param schema: TODO:
    :param document: TODO:
    :param root_value: TODO:
    :param context: TODO:
    :param raw_variable_values: TODO:
    :param operation_name: TODO:
    :type schema: TODO:
    :type document: TODO:
    :type root_value: TODO:
    :type context: TODO:
    :type raw_variable_values: TODO:
    :type operation_name: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    errors: List["GraphQLError"] = []
    operation: Optional["OperationDefinitionNode"] = None
    fragments: Dict[str, "FragmentDefinitionNode"] = {}

    has_multiple_assumed_operations = False
    for definition in document.definitions:
        if isinstance(definition, OperationDefinitionNode):
            if not operation_name and operation:
                has_multiple_assumed_operations = True
            elif not operation_name or (
                definition.name and definition.name.value == operation_name
            ):
                operation = definition
        if isinstance(definition, FragmentDefinitionNode):
            fragments[definition.name.value] = definition

    if not operation:
        errors.append(
            GraphQLError(
                f"Unknown operation named < {operation_name} >."
                if operation_name
                else "Must provide an operation."
            )
        )
    elif has_multiple_assumed_operations:
        errors.append(
            GraphQLError(
                "Must provide operation name if query contains multiple operations."
            )
        )

    variable_values: Dict[str, Any] = {}
    if operation:
        variable_values, variable_errors = get_variable_values(
            schema,
            operation.variable_definitions or [],
            raw_variable_values or {},
        )

        if variable_errors:
            errors.extend(variable_errors)

    if errors:
        return None, errors

    return (
        ExecutionContext(
            schema=schema,
            fragments=fragments,
            operation=operation,
            context=context,
            root_value=root_value,
            variable_values=variable_values,
        ),
        None,
    )
