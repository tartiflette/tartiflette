from typing import Any, Dict, List, Optional, Tuple

from tartiflette.execution.values import get_variable_values
from tartiflette.types.exceptions import GraphQLError

__all__ = ["build_execution_context"]


class ExecutionContext:
    """
    TODO:
    """

    def __init__(
        self,
        schema: "GraphQLSchema",
        operation: "ExecutableOperationNode",
        context: Optional[Any],
        root_value: Optional[Any],
        variable_values: Optional[Dict[str, Any]],
    ) -> None:
        """
        :param schema: TODO:
        :param operation: TODO:
        :param context: TODO:
        :param root_value: TODO:
        :param variable_values: TODO:
        :type schema: TODO:
        :type operation: TODO:
        :type context: TODO:
        :type root_value: TODO:
        :type variable_values: TODO:
        """
        self.schema = schema
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
    operation_name: str,
    executable_operations: Dict[str, "ExecutableOperationNode"],
    context: Optional[Any],
    root_value: Optional[Any],
    raw_variable_values: Optional[Dict[str, Any]],
) -> Tuple[Optional["ExecutionContext"], Optional[List["GraphQLError"]]]:
    """
    TODO:
    :param schema: TODO:
    :param operation_name: TODO:
    :param executable_operations: TODO:
    :param context: TODO:
    :param root_value: TODO:
    :param raw_variable_values: TODO:
    :type schema: TODO:
    :type operation_name: TODO:
    :type executable_operations: TODO:
    :type context: TODO:
    :type root_value: TODO:
    :type raw_variable_values: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    if not executable_operations:
        return (
            None,
            [GraphQLError(f"Unknown operation named < {operation_name} >.")],
        )

    try:
        operation = executable_operations[operation_name]
    except KeyError:
        if operation_name or len(executable_operations) != 1:
            return (
                None,
                [
                    GraphQLError(
                        f"Unknown operation named < {operation_name} >."
                        if operation_name is not None
                        else "Must provide operation name if query contains "
                        "multiple operations."
                    )
                ],
            )

        operation = executable_operations[
            list(executable_operations.keys())[0]
        ]

    variable_values, errors = get_variable_values(
        schema,
        operation.definition.variable_definitions or [],
        raw_variable_values or {},
    )

    if errors:
        return None, errors

    return (
        ExecutionContext(
            schema=schema,
            operation=operation,
            context=context,
            root_value=root_value,
            variable_values=variable_values,
        ),
        None,
    )
