from typing import List, Optional, Union

from tartiflette.collections.unique_mapping import (
    AlreadyDefinedException,
    UniqueMapping,
)
from tartiflette.language.visitor.constants import SKIP
from tartiflette.utils.errors import graphql_error_from_nodes
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("UniqueDirectiveNamesRule",)


class UniqueDirectiveNamesRule(ASTValidationRule):
    """
    A GraphQL document is only valid if all defined directives have
    unique names.
    """

    def __init__(self, context: "ASTValidationContext") -> None:
        """
        :param context: context forwarded to the validation rule
        :type context: ASTValidationContext
        """
        super().__init__(context)
        self._known_directive_names = UniqueMapping()

    def enter_DirectiveDefinition(  # pylint: disable=invalid-name
        self,
        node: "DirectiveDefinitionNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> SKIP:
        """
        Check that all directive definitions have unique names.
        :param node: the current node being visiting
        :param key: the index/key to this node from the parent node/list
        :param parent: the parent immediately above this node
        :param path: the path to get to this node from the root node
        :param ancestors: nodes and list visited before reaching parent node
        :type node: DirectiveDefinitionNode
        :type key: Optional[Union[int, str]]
        :type parent: Optional[Union[Node, List[Node]]]
        :type path: List[Union[int, str]]
        :type ancestors: List[Union[Node, List[Node]]]
        :return: the SKIP visitor constant
        :rtype: SKIP
        """
        # pylint: disable=unused-argument
        directive_name = node.name.value

        try:
            self._known_directive_names[directive_name] = node.name
        except AlreadyDefinedException:
            self.context.report_error(
                graphql_error_from_nodes(
                    "There can be only one directive named "
                    f"< @{directive_name} >.",
                    nodes=[
                        self._known_directive_names[directive_name],
                        node.name,
                    ],
                )
            )

        return SKIP
