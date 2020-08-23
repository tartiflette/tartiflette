from functools import partial
from typing import List, Optional, Union

from tartiflette.collections.unique_mapping import (
    AlreadyDefinedException,
    UniqueMapping,
)
from tartiflette.language.visitor.constants import SKIP
from tartiflette.utils.errors import (
    graphql_error_from_nodes as raw_graphql_error_from_nodes,
)
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("UniqueFragmentNamesRule",)


graphql_error_from_nodes = partial(
    raw_graphql_error_from_nodes,
    extensions={
        "spec": "June 2018",
        "rule": "5.5.1.1",
        "tag": "fragment-name-uniqueness",
        "details": (
            "https://spec.graphql.org/June2018/#sec-Fragment-Name-Uniqueness"
        ),
    },
)


class UniqueFragmentNamesRule(ASTValidationRule):
    """
    A GraphQL document is only valid if all defined fragments have
    unique names.
    """

    def __init__(self, context: "ASTValidationContext") -> None:
        """
        :param context: context forwarded to the validation rule
        :type context: ASTValidationContext
        """
        super().__init__(context)
        self._known_fragment_names = UniqueMapping()

    def enter_OperationDefinition(  # pylint: disable=invalid-name
        self,
        node: "OperationDefinitionNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> SKIP:
        """
        Skip the visit of OperationDefinitionNode.
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
        :return: the SKIP visitor constant
        :rtype: SKIP
        """
        # pylint: disable=no-self-use,unused-argument
        return SKIP

    def enter_FragmentDefinition(  # pylint: disable=invalid-name
        self,
        node: "FragmentDefinitionNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> SKIP:
        """
        Check that fragment definitions have unique names.
        :param node: the current node being visiting
        :param key: the index/key to this node from the parent node/list
        :param parent: the parent immediately above this node
        :param path: the path to get to this node from the root node
        :param ancestors: nodes and list visited before reaching parent node
        :type node: FragmentDefinitionNode
        :type key: Optional[Union[int, str]]
        :type parent: Optional[Union[Node, List[Node]]]
        :type path: List[Union[int, str]]
        :type ancestors: List[Union[Node, List[Node]]]
        :return: the SKIP visitor constant
        :rtype: SKIP
        """
        # pylint: disable=unused-argument
        fragment_name = node.name.value
        try:
            self._known_fragment_names[fragment_name] = node.name
        except AlreadyDefinedException:
            self.context.report_error(
                graphql_error_from_nodes(
                    f"There can be only one fragment named < {fragment_name} >.",
                    nodes=[
                        self._known_fragment_names[fragment_name],
                        node.name,
                    ],
                )
            )
        return SKIP
