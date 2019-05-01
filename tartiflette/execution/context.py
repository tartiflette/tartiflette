from typing import Any, Dict, List, Optional, Tuple

from tartiflette.types.exceptions import GraphQLError
from tartiflette.types.helpers.definition import (
    is_input_type,
    is_non_null_type,
)
from tartiflette.utils.coerce_value import coerce_value
from tartiflette.utils.type_from_ast import schema_type_from_ast
from tartiflette.utils.value_from_ast import UndefinedValue, value_from_ast


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


def graphql_error_from_nodes(message, nodes=None):
    """
    TODO:
    :param message: TODO:
    :param nodes: TODO:
    :type message: TODO:
    :type nodes: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    if nodes is None:
        nodes = []

    if not isinstance(nodes, list):
        nodes = [nodes]

    return GraphQLError(message, locations=[node.location for node in nodes])


def coerce_variables(
    schema: "GraphQLSchema",
    variable_definitions: List["VariableDefinitionNode"],
    raw_variable_values: Dict[str, Any],
) -> Tuple[Dict[str, Any], List["GraphQLError"]]:
    """
    TODO:
    :param schema: TODO:
    :param variable_definitions: TODO:
    :param raw_variable_values: TODO:
    :type schema: TODO:
    :type variable_definitions: TODO:
    :type raw_variable_values: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    errors: List["GraphQLError"] = []
    coerced_values: Dict[str, Any] = {}

    for variable_definition in variable_definitions:
        var_name = variable_definition.variable.name.value
        var_type = schema_type_from_ast(schema, variable_definition.type)

        if not is_input_type(var_type):
            errors.append(
                graphql_error_from_nodes(
                    f"Variable < ${var_name} > expected value of type "
                    f"< {variable_definition.type} > which cannot be used as "
                    "an input type.",
                    nodes=variable_definition.type,
                )
            )
            continue

        has_value = var_name in raw_variable_values
        value = raw_variable_values[var_name] if has_value else UndefinedValue

        if not has_value and variable_definition.default_value:
            coerced_values[var_name] = value_from_ast(
                variable_definition.default_value, var_type
            )
        elif (not has_value or value is None) and is_non_null_type(var_type):
            errors.append(
                graphql_error_from_nodes(
                    (
                        f"Variable < ${var_name} > of non-null type "
                        f"< {var_type} > must not be null."
                    )
                    if has_value
                    else (
                        f"Variable < ${var_name} > of required type "
                        f"< {var_type} > was not provided."
                    ),
                    nodes=variable_definition,
                )
            )
        elif has_value:
            if value is None:
                coerced_values[var_name] = None
            else:
                coerced_value, coerce_errors = coerce_value(
                    value, var_type, variable_definition
                )
                if coerce_errors:
                    for coerce_error in coerce_errors:
                        coerce_error.message = (
                            f"Variable < ${var_name} > got invalid value "
                            f"< {value} >; {coerce_error.message}"
                        )
                    errors.extend(coerce_errors)
                else:
                    coerced_values[var_name] = coerced_value

    return coerced_values, errors


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

    variable_values, errors = coerce_variables(
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
