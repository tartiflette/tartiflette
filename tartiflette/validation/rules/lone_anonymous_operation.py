from functools import partial
from typing import List, Optional, Union

from tartiflette.language.ast import OperationDefinitionNode
from tartiflette.utils.errors import (
    graphql_error_from_nodes as raw_graphql_error_from_nodes,
)
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("LoneAnonymousOperationRule",)


graphql_error_from_nodes = partial(
    raw_graphql_error_from_nodes,
    extensions={
        "spec": "June 2018",
        "rule": "5.2.2.1",
        "tag": "lone-anonymous-operation",
        "details": (
            "https://spec.graphql.org/June2018/#sec-Lone-Anonymous-Operation"
        ),
    },
)


class LoneAnonymousOperationRule(ASTValidationRule):
    """
    A GraphQL document is only valid if when it contains an anonymous
    operation (the query short-hand) that it contains only that one
    operation definition.
    """

    def __init__(self, context: "ASTValidationContext") -> None:
        """
        :param context: context forwarded to the validation rule
        :type context: ASTValidationContext
        """
        super().__init__(context)
        self._operation_count = len(
            [
                definition
                for definition in context.document_node.definitions
                if isinstance(definition, OperationDefinitionNode)
            ]
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
        Check that there is only one anonymous operation defined.
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
        if not node.name and self._operation_count > 1:
            self.context.report_error(
                graphql_error_from_nodes(
                    "This anonymous operation must be the only defined operation.",
                    nodes=[node],
                )
            )
