from functools import partial
from typing import List, Optional, Union

from tartiflette.language.ast import NullValueNode
from tartiflette.types.helpers.comparators import is_type_sub_type_of
from tartiflette.types.helpers.definition import is_non_null_type
from tartiflette.utils.errors import (
    graphql_error_from_nodes as raw_graphql_error_from_nodes,
)
from tartiflette.utils.type_from_ast import schema_type_from_ast
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("VariablesInAllowedPositionRule",)


graphql_error_from_nodes = partial(
    raw_graphql_error_from_nodes,
    extensions={
        "spec": "June 2018",
        "rule": "5.8.5",
        "tag": "all-variable-usages-are-allowed",
        "details": (
            "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed"
        ),
    },
)


def _allowed_variable_usage(
    schema: "GraphQLSchema",
    variable_type: "GraphQLType",
    variable_default_value: Optional["ValueNode"],
    location_type: "GraphQLType",
    location_default_value: Optional["ValueNode"],
) -> bool:
    """
    Determine whether or not the variable is allowed in the location.
    :param schema: the GraphQLSchema instance linked to the query
    :param variable_type: the GraphQL type instance of the variable
    :param variable_default_value: the default value of the variable
    :param location_type: the GraphQL type of the location
    :param location_default_value: the default value of the location
    :type schema: GraphQLSchema
    :type variable_type: GraphQLType
    :type variable_default_value: Optional["ValueNode"]
    :type location_type: GraphQLType
    :type location_default_value: Optional["ValueNode"]
    :return: whether or not the variable is allowed in the location
    :rtype: bool
    """
    if is_non_null_type(location_type) and not is_non_null_type(variable_type):
        if (
            variable_default_value is None
            or isinstance(variable_default_value, NullValueNode)
        ) and location_default_value is None:
            return False
        return is_type_sub_type_of(
            schema, variable_type, location_type.wrapped_type
        )
    return is_type_sub_type_of(schema, variable_type, location_type)


class VariablesInAllowedPositionRule(ASTValidationRule):
    """
    Variables in allowed position

    Variables passed to field arguments conform to type.
    """

    def __init__(self, context: "ASTValidationContext") -> None:
        """
        :param context: context forwarded to the validation rule
        :type context: ASTValidationContext
        """
        super().__init__(context)
        self._variable_definition_map = {}

    def enter_OperationDefinition(  # pylint: disable=invalid-name
        self,
        node: "OperationDefinitionNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> None:
        """
        Clear the known variable definitions for the new operation.
        :param node: the current node being visiting
        :param key: the index/key to this node from the parent node/list
        :param parent: the parent immediately above this node
        :param path: the path to get to this node from the root node
        :param ancestors: nodes and list visited before reaching parent node
        :type node: OperationDefinitionNode
        :type key: Optional[Union[int, str]]
        :type parent: Optional[Union[Node, List[Node]]]
        :type path: List[Union[int, str]]
        :type ancestors: List[Union[Node, List[Node]]]
        """
        # pylint: disable=unused-argument
        self._variable_definition_map = {}

    def leave_OperationDefinition(  # pylint: disable=invalid-name
        self,
        node: "OperationDefinitionNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> None:
        """
        Check that variables are used in allowed position.
        :param node: the current node being visiting
        :param key: the index/key to this node from the parent node/list
        :param parent: the parent immediately above this node
        :param path: the path to get to this node from the root node
        :param ancestors: nodes and list visited before reaching parent node
        :type node: OperationDefinitionNode
        :type key: Optional[Union[int, str]]
        :type parent: Optional[Union[Node, List[Node]]]
        :type path: List[Union[int, str]]
        :type ancestors: List[Union[Node, List[Node]]]
        """
        # pylint: disable=unused-argument
        for usage in self.context.get_recursive_variable_usages(node):
            node, gql_type, default_value = (
                usage["node"],
                usage["type"],
                usage["default_value"],
            )
            variable_name = node.name.value
            variable_definition = self._variable_definition_map.get(
                variable_name
            )
            if variable_definition and gql_type:
                variable_type = schema_type_from_ast(
                    self.context.schema, variable_definition.type
                )
                if variable_type and not _allowed_variable_usage(
                    self.context.schema,
                    variable_type,
                    variable_definition.default_value,
                    gql_type,
                    default_value,
                ):
                    self.context.report_error(
                        graphql_error_from_nodes(
                            f"Variable < ${variable_name} > of type "
                            f"< {variable_type} > used in position expecting "
                            f"type < {gql_type} >.",
                            nodes=[variable_definition, node],
                        )
                    )

    def enter_VariableDefinition(  # pylint: disable=invalid-name
        self,
        node: "VariableDefinitionNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> None:
        """
        Register the definition to the known variables definitions.
        :param node: the current node being visiting
        :param key: the index/key to this node from the parent node/list
        :param parent: the parent immediately above this node
        :param path: the path to get to this node from the root node
        :param ancestors: nodes and list visited before reaching parent node
        :type node: VariableDefinitionNode
        :type key: Optional[Union[int, str]]
        :type parent: Optional[Union[Node, List[Node]]]
        :type path: List[Union[int, str]]
        :type ancestors: List[Union[Node, List[Node]]]
        """
        # pylint: disable=unused-argument
        self._variable_definition_map[node.variable.name.value] = node
