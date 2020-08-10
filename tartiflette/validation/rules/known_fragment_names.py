from functools import partial
from typing import List, Optional, Union

from tartiflette.utils.errors import (
    graphql_error_from_nodes as raw_graphql_error_from_nodes,
)
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("KnownFragmentNamesRule",)


graphql_error_from_nodes = partial(
    raw_graphql_error_from_nodes,
    extensions={
        "spec": "June 2018",
        "rule": "5.5.2.1",
        "tag": "fragment-spread-target-defined",
        "details": "https://spec.graphql.org/June2018/#sec-Fragment-spread-target-defined",
    },
)


class KnownFragmentNamesRule(ASTValidationRule):
    """
    A GraphQL document is only valid if all `...Fragment` fragment
    spreads refer to fragments defined in the same document.
    """

    def enter_FragmentSpread(  # pylint: disable=invalid-name
        self,
        node: "FragmentSpreadNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> None:
        """
        Check that fragment spreads refer to a defined fragment.
        :param node: the current node being visiting
        :param key: the index/key to this node from the parent node/list
        :param parent: the parent immediately above this node
        :param path: the path to get to this node from the root node
        :param ancestors: nodes and list visited before reaching parent node
        :type node: FragmentSpreadNode
        :type key: Optional[Union[int, str]]
        :type parent: Optional[Union[Node, List[Node]]]
        :type path: List[Union[int, str]]
        :type ancestors: List[Union[Node, List[Node]]]
        """
        # pylint: disable=unused-argument
        fragment_name = node.name.value
        fragment = self.context.get_fragment(fragment_name)
        if not fragment:
            self.context.report_error(
                graphql_error_from_nodes(
                    f"Unknown fragment < {fragment_name} >.",
                    nodes=[node.name],
                )
            )
