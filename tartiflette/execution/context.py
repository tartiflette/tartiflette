from typing import Any, Dict, List, Optional, Tuple, Union

from tartiflette.coercers.variables import coerce_variables
from tartiflette.execution.collect import (
    collect_executable_variable_definitions,
)
from tartiflette.language.ast import (
    FragmentDefinitionNode,
    OperationDefinitionNode,
)
from tartiflette.types.exceptions.tartiflette import (
    MultipleException,
    TartifletteError,
)
from tartiflette.utils.errors import is_coercible_exception

__all__ = ("build_execution_context",)


class ExecutionContext:
    """
    Utility class containing all the information needed to run an end-to-end
    GraphQL request.
    """

    __slots__ = (
        "schema",
        "fragments",
        "operation",
        "context",
        "root_value",
        "variable_values",
        "errors",
    )

    def __init__(
        self,
        schema: "GraphQLSchema",
        fragments: Dict[str, "FragmentDefinitionNode"],
        operation: "OperationDefinitionNode",
        context: Optional[Any],
        root_value: Optional[Any],
        variable_values: Optional[Dict[str, Any]],
    ) -> None:
        """
        :param schema: the GraphQLSchema instance linked to the engine
        :param fragments: the dictionary of fragment definition AST node
        contained in the request
        :param operation: the AST operation definition node to execute
        :param context: value that can contain everything you need and that
        will be accessible from the resolvers
        :param root_value: an initial value corresponding to the root type
        being executed
        :param variable_values: the variables used in the GraphQL request
        :type schema: GraphQLSchema
        :type fragments: Dict[str, FragmentDefinitionNode]
        :type operation: OperationDefinitionNode
        :type context: Optional[Any]
        :type root_value: Optional[Any]
        :type variable_values: Optional[Dict[str, Any]]
        """
        # pylint: disable=too-many-arguments,too-many-locals
        self.schema = schema
        self.fragments = fragments
        self.operation = operation
        self.context = context
        self.root_value = root_value
        self.variable_values = variable_values
        self.errors: List["TartifletteError"] = []

    def add_error(
        self,
        raw_exception: Union[
            "TartifletteError", "MultipleException", Exception
        ],
        path: Optional[List[str]] = None,
        locations: Optional[List["Location"]] = None,
    ) -> None:
        """
        Adds the contents of an exception to the known execution errors.
        :param raw_exception: the raw exception to treat
        :param path: the path where the raw exception occurred
        :param locations: the locations linked to the raw exception
        :type raw_exception: Union[TartifletteError, MultipleException, Exception]
        :type path: Optional[List[str]]
        :param locations: Optional[List["Location"]]
        """
        exceptions = (
            raw_exception.exceptions
            if isinstance(raw_exception, MultipleException)
            else [raw_exception]
        )

        for exception in exceptions:
            graphql_error = (
                exception
                if is_coercible_exception(exception)
                else TartifletteError(
                    str(exception), path, locations, original_error=exception
                )
            )

            self.errors.append(graphql_error)


async def build_execution_context(
    schema: "GraphQLSchema",
    document: "DocumentNode",
    root_value: Optional[Any],
    context: Optional[Any],
    raw_variable_values: Optional[Dict[str, Any]],
    operation_name: str,
) -> Tuple[Optional["ExecutionContext"], Optional[List["TartifletteError"]]]:
    """
    Factory function to build and return an ExecutionContext instance.
    :param schema: the GraphQLSchema instance linked to the engine
    :param document: the DocumentNode instance linked to the GraphQL request
    :param root_value: an initial value corresponding to the root type being
    executed
    :param context: value that can contain everything you need and that will be
    accessible from the resolvers
    :param raw_variable_values: the variables used in the GraphQL request
    :param operation_name: the operation name to execute
    :type schema: GraphQLSchema
    :type document: DocumentNode
    :type root_value: Optional[Any]
    :type context: Optional[Any]
    :type raw_variable_values: Optional[Dict[str, Any]]
    :type operation_name: str
    :return: an ExecutionContext instance
    :rtype: Tuple[Optional[ExecutionContext], Optional[List[TartifletteError]]]
    """
    # pylint: disable=too-many-arguments,too-many-locals
    errors: List["TartifletteError"] = []
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
            TartifletteError(
                f"Unknown operation named < {operation_name} >."
                if operation_name
                else "Must provide an operation."
            )
        )
    elif has_multiple_assumed_operations:
        errors.append(
            TartifletteError(
                "Must provide operation name if query contains multiple operations."
            )
        )

    variable_values: Dict[str, Any] = {}
    if operation:
        executable_variable_definitions = collect_executable_variable_definitions(
            schema, operation
        )

        variable_values, variable_errors = await coerce_variables(
            executable_variable_definitions, raw_variable_values or {}, context
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
