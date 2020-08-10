from functools import partial
from typing import List, Optional, Union

from tartiflette.language.ast import FragmentSpreadNode, InlineFragmentNode
from tartiflette.utils.errors import (
    graphql_error_from_nodes as raw_graphql_error_from_nodes,
)
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("SingleFieldSubscriptionsRule",)


graphql_error_from_nodes = partial(
    raw_graphql_error_from_nodes,
    extensions={
        "spec": "June 2018",
        "rule": "5.2.3.1",
        "tag": "single-root-field",
        "details": "https://spec.graphql.org/June2018/#sec-Single-root-field",
    },
)


class SingleFieldSubscriptionsRule(ASTValidationRule):
    """
    A GraphQL subscription is valid only if it contains a single root
    field.
    """

    def _validate_selections(
        self,
        operation_node: "OperationDefinitionNode",
        selections: List["Node"],
    ) -> None:
        """
        Check a selections and its sub-selections to check there no more
        than one field selected.
        :param operation_node: the OperationDefinitionNode to check
        :param selections: list of nodes from selections
        :type operation_node: OperationDefinitionNode
        :type selections: List["Node"]
        """
        if len(selections) != 1:
            self.context.report_error(
                graphql_error_from_nodes(
                    (
                        f"Subscription < {operation_node.name.value} >"
                        if operation_node.name
                        else "Anonymous Subscription"
                    )
                    + " must select only one top level field.",
                    nodes=selections[1:],
                )
            )

        selection = selections[0]
        if isinstance(selection, InlineFragmentNode):
            self._validate_selections(
                operation_node, selection.selection_set.selections
            )
        elif isinstance(selection, FragmentSpreadNode):
            fragment_definition = self.context.get_fragment(
                selection.name.value
            )
            self._validate_selections(
                operation_node, fragment_definition.selection_set.selections
            )

    def enter_OperationDefinition(  # pylint: disable=invalid-name
        self,
        node: "OperationDefinitionNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> None:
        """
        Check that subscription operation contains a single root field.
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
        if node.operation_type == "subscription":
            self._validate_selections(node, node.selection_set.selections)
