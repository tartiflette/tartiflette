from functools import partial
from typing import List, Optional, Union

from tartiflette.utils.errors import (
    graphql_error_from_nodes as raw_graphql_error_from_nodes,
)
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("NoUnusedVariablesRule",)


graphql_error_from_nodes = partial(
    raw_graphql_error_from_nodes,
    extensions={
        "spec": "June 2018",
        "rule": "5.8.4",
        "tag": "all-variables-used",
        "details": "https://spec.graphql.org/June2018/#sec-All-Variables-Used",
    },
)


class NoUnusedVariablesRule(ASTValidationRule):
    """
    A GraphQL operation is only valid if all variables defined by an
    operation are used, either directly or within a spread fragment.
    """

    def __init__(self, context: "ASTValidationContext") -> None:
        """
        :param context: context forwarded to the validation rule
        :type context: ASTValidationContext
        """
        super().__init__(context)
        self._variable_definitions = []

    def enter_VariableDefinition(  # pylint: disable=invalid-name
        self,
        node: "VariableDefinitionNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> None:
        """
        Collect the VariableDefinitionNode.
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
        self._variable_definitions.append(node)

    def enter_OperationDefinition(  # pylint: disable=invalid-name
        self,
        node: "OperationDefinitionNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> None:
        """
        Clear the variable definitions for the new operation definition.
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
        self._variable_definitions = []

    def leave_OperationDefinition(  # pylint: disable=invalid-name
        self,
        node: "OperationDefinitionNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> None:
        """
        Check that all variables defined by operations are used.
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
        variable_name_used = {
            usage["node"].name.value
            for usage in self.context.get_recursive_variable_usages(node)
        }

        for variable_definition in self._variable_definitions:
            variable_name = variable_definition.variable.name.value
            if variable_name not in variable_name_used:
                self.context.report_error(
                    graphql_error_from_nodes(
                        f"Variable < ${variable_name} > is never used in "
                        f"operation < {node.name.value} >."
                        if node.name
                        else f"Variable < ${variable_name} > is never used.",
                        nodes=[variable_definition],
                    )
                )
