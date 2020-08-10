from functools import partial
from typing import List, Optional, Union

from tartiflette.language.visitor.constants import SKIP
from tartiflette.utils.errors import (
    graphql_error_from_nodes as raw_graphql_error_from_nodes,
)
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("NoFragmentCyclesRule",)


graphql_error_from_nodes = partial(
    raw_graphql_error_from_nodes,
    extensions={
        "spec": "June 2018",
        "rule": "5.5.2.2",
        "tag": "fragment-spreads-must-not-form-cycles",
        "details": (
            "https://spec.graphql.org/June2018/#sec-Fragment-spreads-must-not-form-cycles"
        ),
    },
)


class NoFragmentCyclesRule(ASTValidationRule):
    """
    The graph of fragment spreads must not form any cycles including
    spreading itself.
    """

    def __init__(self, context: "ASTValidationContext") -> None:
        """
        :param context: context forwarded to the validation rule
        :type context: ASTValidationContext
        """
        super().__init__(context)
        self._visited_fragments = set()
        self._spread_path = []
        self._spread_path_index_by_name = {}

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

    def _detect_cycle_recursive(self, node: "FragmentDefinitionNode") -> None:
        """
        CHeck if there is any cycles fragment spreads.
        :param node: the current node being visiting
        :type node: FragmentDefinitionNode
        """
        fragment_name = node.name.value
        if fragment_name in self._visited_fragments:
            return

        self._visited_fragments.add(fragment_name)

        spread_nodes = self.context.get_fragment_spreads(node.selection_set)
        if not spread_nodes:
            return

        self._spread_path_index_by_name[fragment_name] = len(self._spread_path)

        for spread_node in spread_nodes:
            spread_name = spread_node.name.value
            cycle_index = self._spread_path_index_by_name.get(spread_name)

            self._spread_path.append(spread_node)
            if cycle_index is None:
                spread_fragment = self.context.get_fragment(spread_name)
                if spread_fragment:
                    self._detect_cycle_recursive(spread_fragment)
            else:
                cycle_path = self._spread_path[cycle_index:]
                via_path = ", ".join(
                    f"< {s.name.value} >" for s in cycle_path[:-1]
                )
                self.context.report_error(
                    graphql_error_from_nodes(
                        f"Cannot spread fragment < {spread_name} > within "
                        f"itself" + (f" via {via_path}." if via_path else "."),
                        nodes=cycle_path,
                    )
                )
            self._spread_path.pop()

        del self._spread_path_index_by_name[fragment_name]

    def enter_FragmentDefinition(  # pylint: disable=invalid-name
        self,
        node: "FragmentDefinitionNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> SKIP:
        """
        CHeck if there is any cycles fragment spreads.
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
        self._detect_cycle_recursive(node)
        return SKIP
