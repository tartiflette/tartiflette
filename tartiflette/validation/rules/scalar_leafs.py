from functools import partial
from typing import List, Optional, Union

from tartiflette.types.helpers.definition import get_wrapped_type, is_leaf_type
from tartiflette.utils.errors import (
    graphql_error_from_nodes as raw_graphql_error_from_nodes,
)
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("ScalarLeafsRule",)


graphql_error_from_nodes = partial(
    raw_graphql_error_from_nodes,
    extensions={
        "spec": "June 2018",
        "rule": "5.3.3",
        "tag": "leaf-field-selections",
        "details": (
            "https://spec.graphql.org/June2018/#sec-Leaf-Field-Selections"
        ),
    },
)


class ScalarLeafsRule(ASTValidationRule):
    """
    A GraphQL document is valid only if all leaf fields (fields without
    sub selections) are of scalar or enum types.
    """

    def enter_Field(  # pylint: disable=invalid-name
        self,
        node: "FieldNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> None:
        """
        Check that the field is defined with a leaf type.
        :param node: the current node being visiting
        :param key: the index/key to this node from the parent node/list
        :param parent: the parent immediately above this node
        :param path: the path to get to this node from the root node
        :param ancestors: nodes and list visited before reaching parent node
        :type node: FieldNode
        :type key: Optional[Union[int, str]]
        :type parent: Optional[Union[Node, List[Node]]]
        :type path: List[Union[int, str]]
        :type ancestors: List[Union[Node, List[Node]]]
        """
        # pylint: disable=unused-argument
        gql_type = self.context.get_type()

        if gql_type:
            selection_set = node.selection_set
            if is_leaf_type(get_wrapped_type(gql_type)):
                if selection_set:
                    self.context.report_error(
                        graphql_error_from_nodes(
                            f"Field < {node.name.value} > must not have a "
                            f"selection since type < {gql_type} > has no "
                            "subfields.",
                            nodes=[selection_set],
                        )
                    )
            elif not selection_set:
                field_name = node.name.value
                self.context.report_error(
                    graphql_error_from_nodes(
                        f"Field < {field_name} > of type < {gql_type} > must "
                        "have a selection of subfields. Did you mean "
                        f"< {field_name} {{ ... }} >?",
                        nodes=[node],
                    )
                )
