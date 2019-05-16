from functools import partial
from typing import Any, Callable

from tartiflette.coercers.inputs.compute import get_input_coercer
from tartiflette.coercers.literals.compute import get_literal_coercer
from tartiflette.coercers.variables import variable_coercer
from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.utils.type_from_ast import schema_type_from_ast

__all__ = ("variable_definition_node_to_executable",)


class ExecutableVariableDefinition:
    """
    Node representing a GraphQL executable variable definition.
    """

    __slots__ = (
        "name",
        "graphql_type",
        "default_value",
        "coercer",
        "definition",
    )

    def __init__(
        self,
        name: str,
        graphql_type: "GraphQLType",
        default_value: Any,
        coercer: Callable,
        definition: "VariableDefinitionNode",
    ) -> None:
        """
        :param name: the name of the variable
        :param graphql_type: the GraphQLType expected for the variable value
        :param default_value: the default value of the variable
        :param coercer: callable to use when coercing the user input value
        :param definition_node: the variable definition AST node
        :type name: str
        :type graphql_type: GraphQLType
        :type default_value: Any
        :type coercer: Callable
        :type definition_node: VariableDefinitionNode
        """
        self.name = name
        self.graphql_type = graphql_type
        self.default_value = default_value
        self.coercer = partial(coercer, self)
        self.definition = definition


def variable_definition_node_to_executable(
    schema: "GraphQLSchema", variable_definition_node: "VariableDefinitionNode"
) -> "ExecutableVariableDefinition":
    """
    Converts a variable definition AST node into an executable variable
    definition.
    :param schema: the GraphQLSchema instance linked to the engine
    :param variable_definition_node: the variable definition AST node to treat
    :type schema: GraphQLSchema
    :type variable_definition_node: VariableDefinitionNode
    :return: an executable variable definition
    :rtype: ExecutableVariableDefinition
    """
    graphql_type = schema_type_from_ast(schema, variable_definition_node.type)
    return ExecutableVariableDefinition(
        name=variable_definition_node.variable.name.value,
        graphql_type=graphql_type,
        default_value=variable_definition_node.default_value
        or UNDEFINED_VALUE,
        coercer=partial(
            variable_coercer,
            input_coercer=partial(
                get_input_coercer(graphql_type), variable_definition_node
            ),
            literal_coercer=get_literal_coercer(graphql_type),
        ),
        definition=variable_definition_node,
    )
