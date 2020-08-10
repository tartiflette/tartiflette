from functools import partial
from typing import List, Optional, Union

from tartiflette.types.helpers.comparators import do_types_overlap
from tartiflette.types.helpers.definition import is_composite_type
from tartiflette.utils.errors import (
    graphql_error_from_nodes as raw_graphql_error_from_nodes,
)
from tartiflette.utils.type_from_ast import schema_type_from_ast
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("PossibleFragmentSpreadsRule",)


graphql_error_from_nodes = partial(
    raw_graphql_error_from_nodes,
    extensions={
        "spec": "June 2018",
        "rule": "5.5.2.3",
        "tag": "fragment-spread-is-possible",
        "details": (
            "https://spec.graphql.org/June2018/#sec-Fragment-spread-is-possible"
        ),
    },
)


class PossibleFragmentSpreadsRule(ASTValidationRule):
    """
    A fragment spread is only valid if the type condition could ever
    possibly be true: if there is a non-empty intersection of the
    possible parent types, and possible types which pass the type
    condition.
    """

    def _get_fragment_type(self, name: str) -> Optional["GraphQLType"]:
        """
        Fetch the GraphQL type of the type condition of the fragment.
        :param name: name of the fragment to fetch
        :type name: str
        :return: the GraphQL type of the type condition of the fragment
        :rtype: Optional[GraphQLType]
        """
        fragment = self.context.get_fragment(name)
        if fragment:
            gql_type = schema_type_from_ast(
                self.context.schema, fragment.type_condition
            )
            if is_composite_type(gql_type):
                return gql_type
        return None

    def enter_InlineFragment(  # pylint: disable=invalid-name
        self,
        node: "InlineFragmentNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> None:
        """
        Check that the inline fragment can be spread in its context.
        :param node: the current node being visiting
        :param key: the index/key to this node from the parent node/list
        :param parent: the parent immediately above this node
        :param path: the path to get to this node from the root node
        :param ancestors: nodes and list visited before reaching parent node
        :type node: InlineFragmentNode
        :type key: Optional[Union[int, str]]
        :type parent: Optional[Union[Node, List[Node]]]
        :type path: List[Union[int, str]]
        :type ancestors: List[Union[Node, List[Node]]]
        """
        # pylint: disable=unused-argument
        fragment_type = self.context.get_type()
        parent_type = self.context.get_parent_type()

        if (
            is_composite_type(fragment_type)
            and is_composite_type(parent_type)
            and not do_types_overlap(fragment_type, parent_type)
        ):
            self.context.report_error(
                graphql_error_from_nodes(
                    "Fragment cannot be spread here as objects of type "
                    f"< {parent_type} > can never be of type "
                    f"< {fragment_type} >.",
                    nodes=[node],
                )
            )

    def enter_FragmentSpread(  # pylint: disable=invalid-name
        self,
        node: "FragmentSpreadNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> None:
        """
        Check that the fragment spread can be spread in its context.
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
        fragment_type = self._get_fragment_type(fragment_name)
        parent_type = self.context.get_parent_type()

        if (
            fragment_type
            and parent_type
            and not do_types_overlap(fragment_type, parent_type)
        ):
            self.context.report_error(
                graphql_error_from_nodes(
                    f"Fragment < {fragment_name} > cannot be spread here as "
                    f"objects of type < {parent_type} > can never be of type "
                    f"< {fragment_type} >.",
                    nodes=[node],
                )
            )
