from functools import partial
from typing import List, Optional, Union

from tartiflette.utils.errors import (
    graphql_error_from_nodes as raw_graphql_error_from_nodes,
)
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("FieldsOnCorrectTypeRule",)


graphql_error_from_nodes = partial(
    raw_graphql_error_from_nodes,
    extensions={
        "spec": "June 2018",
        "rule": "5.3.1",
        "tag": "field-selections-on-objects-interfaces-and-unions-types",
        "details": (
            "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types"
        ),
    },
)


class FieldsOnCorrectTypeRule(ASTValidationRule):
    """
    A GraphQL document is only valid if all fields selected are defined
    by the parent type, or are an allowed meta field such as __typename.
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
        Check that all fields are defined by the parent type.
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
        # pylint: disable=no-self-use,unused-argument
        parent_type = self.context.get_parent_type()
        if parent_type:
            field_definition = self.context.get_field_def()
            if not field_definition:
                # TODO: add types condition or field name suggestions here
                self.context.report_error(
                    graphql_error_from_nodes(
                        f"Cannot query field < {node.name.value} > on type "
                        f"< {parent_type.name} >.",
                        nodes=[node],
                    )
                )
