from functools import partial
from typing import List, Optional, Union

from tartiflette.utils.errors import (
    graphql_error_from_nodes as raw_graphql_error_from_nodes,
)
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("UniqueVariableNamesRule",)


graphql_error_from_nodes = partial(
    raw_graphql_error_from_nodes,
    extensions={
        "spec": "June 2018",
        "rule": "5.8.1",
        "tag": "variable-uniqueness",
        "details": (
            "https://spec.graphql.org/June2018/#sec-Variable-Uniqueness"
        ),
    },
)


class UniqueVariableNamesRule(ASTValidationRule):
    """
    A GraphQL operation is only valid if all its variables are uniquely
    named.
    """

    def __init__(self, context: "ASTValidationContext") -> None:
        """
        :param context: context forwarded to the validation rule
        :type context: ASTValidationContext
        """
        super().__init__(context)
        self._known_variable_names = {}

    def enter_OperationDefinition(  # pylint: disable=invalid-name
        self,
        node: "OperationDefinitionNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> None:
        """
        Clear the known variable names for the new operation definition.
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
        self._known_variable_names = {}

    def enter_VariableDefinition(  # pylint: disable=invalid-name
        self,
        node: "VariableDefinitionNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> None:
        """
        Check that the name of the variable isn't already used.
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
        variable_name = node.variable.name.value
        known_variable = self._known_variable_names.get(variable_name)
        if known_variable:
            self.context.report_error(
                graphql_error_from_nodes(
                    f"There can be only one variable named < ${variable_name} >.",
                    nodes=[known_variable, node.variable.name],
                )
            )
        else:
            self._known_variable_names[variable_name] = node.variable.name
