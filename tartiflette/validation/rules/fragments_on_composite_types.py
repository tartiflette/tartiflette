from functools import partial
from typing import List, Optional, Union

from tartiflette.types.helpers.definition import is_composite_type
from tartiflette.utils.errors import (
    graphql_error_from_nodes as raw_graphql_error_from_nodes,
)
from tartiflette.utils.type_from_ast import schema_type_from_ast
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("FragmentsOnCompositeTypesRule",)


graphql_error_from_nodes = partial(
    raw_graphql_error_from_nodes,
    extensions={
        "spec": "June 2018",
        "rule": "5.5.1.3",
        "tag": "fragments-on-composite-types",
        "details": (
            "https://spec.graphql.org/June2018/#sec-Fragments-On-Composite-Types"
        ),
    },
)


class FragmentsOnCompositeTypesRule(ASTValidationRule):
    """
    Fragments use a type condition to determine if they apply, since
    fragments can only be spread into a composite type (object,
    interface, or union), the type condition must also be a composite
    type.
    """

    def enter_InlineFragment(  # pylint: disable=invalid-name
        self,
        node: "InlineFragmentNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> None:
        """
        Check that type condition of inline fragment is composite type.
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
        type_condition = node.type_condition
        if type_condition:
            gql_type = schema_type_from_ast(
                self.context.schema, type_condition
            )
            if gql_type and not is_composite_type(gql_type):
                self.context.report_error(
                    graphql_error_from_nodes(
                        f"Fragment cannot condition on non composite type < {gql_type} >.",
                        nodes=type_condition,
                    )
                )

    def enter_FragmentDefinition(  # pylint: disable=invalid-name
        self,
        node: "FragmentDefinitionNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> None:
        """
        Check that type condition of fragment definition is composite type.
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
        """
        # pylint: disable=unused-argument
        type_condition = node.type_condition
        gql_type = schema_type_from_ast(self.context.schema, type_condition)
        if gql_type and not is_composite_type(gql_type):
            self.context.report_error(
                graphql_error_from_nodes(
                    f"Fragment < {node.name.value} > cannot condition on non composite type < {gql_type} >.",
                    nodes=type_condition,
                )
            )
