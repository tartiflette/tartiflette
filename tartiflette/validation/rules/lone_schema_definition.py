from typing import List, Optional, Union

from tartiflette.utils.errors import graphql_error_from_nodes
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("LoneSchemaDefinitionRule",)


class LoneSchemaDefinitionRule(ASTValidationRule):
    """
    A GraphQL document is only valid if it contains only one schema
    definition.
    """

    def __init__(self, context: "ASTValidationContext") -> None:
        """
        :param context: context forwarded to the validation rule
        :type context: ASTValidationContext
        """
        super().__init__(context)
        self._first_definition = None

    def enter_SchemaDefinition(  # pylint: disable=invalid-name
        self,
        node: "SchemaDefinitionNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> None:
        """
        Check there is only one schema definition.
        :param node: the current node being visiting
        :param key: the index/key to this node from the parent node/list
        :param parent: the parent immediately above this node
        :param path: the path to get to this node from the root node
        :param ancestors: nodes and list visited before reaching parent node
        :type node: SchemaDefinitionNode
        :type key: Optional[Union[int, str]]
        :type parent: Optional[Union[Node, List[Node]]]
        :type path: List[Union[int, str]]
        :type ancestors: List[Union[Node, List[Node]]]
        """
        # pylint: disable=unused-argument
        if self._first_definition is not None:
            self.context.report_error(
                graphql_error_from_nodes(
                    "Must provide only one schema definition.",
                    nodes=[self._first_definition, node],
                )
            )
            return
        self._first_definition = node
