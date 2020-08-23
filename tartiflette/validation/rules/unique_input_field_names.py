from functools import partial
from typing import List, Optional, Union

from tartiflette.collections.unique_mapping import (
    AlreadyDefinedException,
    UniqueMapping,
)
from tartiflette.utils.errors import (
    graphql_error_from_nodes as raw_graphql_error_from_nodes,
)
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("UniqueInputFieldNamesRule",)


graphql_error_from_nodes = partial(
    raw_graphql_error_from_nodes,
    extensions={
        "spec": "June 2018",
        "rule": "5.6.3",
        "tag": "input-object-field-uniqueness",
        "details": (
            "https://spec.graphql.org/June2018/#sec-Input-Object-Field-Uniqueness"
        ),
    },
)


class UniqueInputFieldNamesRule(ASTValidationRule):
    """
    A GraphQL input object value is only valid if all supplied fields
    are uniquely named.
    """

    def __init__(self, context: "ASTValidationContext") -> None:
        """
        :param context: context forwarded to the validation rule
        :type context: ASTValidationContext
        """
        super().__init__(context)
        self._known_name_stack: List[UniqueMapping] = []
        self._known_input_fields = UniqueMapping()

    def enter_ObjectValue(  # pylint: disable=invalid-name
        self,
        node: "ObjectValueNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> None:
        """
        Collect input fields.
        :param node: the current node being visiting
        :param key: the index/key to this node from the parent node/list
        :param parent: the parent immediately above this node
        :param path: the path to get to this node from the root node
        :param ancestors: nodes and list visited before reaching parent node
        :type node: ObjectValueNode
        :type key: Optional[Union[int, str]]
        :type parent: Optional[Union[Node, List[Node]]]
        :type path: List[Union[int, str]]
        :type ancestors: List[Union[Node, List[Node]]]
        """
        # pylint: disable=unused-argument
        self._known_name_stack.append(self._known_input_fields)
        self._known_input_fields = UniqueMapping()

    def leave_ObjectValue(  # pylint: disable=invalid-name
        self,
        node: "ObjectValueNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> None:
        """
        Store collected input fields.
        :param node: the current node being visiting
        :param key: the index/key to this node from the parent node/list
        :param parent: the parent immediately above this node
        :param path: the path to get to this node from the root node
        :param ancestors: nodes and list visited before reaching parent node
        :type node: ObjectValueNode
        :type key: Optional[Union[int, str]]
        :type parent: Optional[Union[Node, List[Node]]]
        :type path: List[Union[int, str]]
        :type ancestors: List[Union[Node, List[Node]]]
        """
        # pylint: disable=unused-argument
        self._known_input_fields = self._known_name_stack.pop()

    def enter_ObjectField(  # pylint: disable=invalid-name
        self,
        node: "ObjectFieldNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> None:
        """
        Check that object input fields are uniquely named.
        :param node: the current node being visiting
        :param key: the index/key to this node from the parent node/list
        :param parent: the parent immediately above this node
        :param path: the path to get to this node from the root node
        :param ancestors: nodes and list visited before reaching parent node
        :type node: ObjectFieldNode
        :type key: Optional[Union[int, str]]
        :type parent: Optional[Union[Node, List[Node]]]
        :type path: List[Union[int, str]]
        :type ancestors: List[Union[Node, List[Node]]]
        """
        # pylint: disable=unused-argument
        field_name = node.name.value
        try:
            self._known_input_fields[field_name] = node.name
        except AlreadyDefinedException:
            self.context.report_error(
                graphql_error_from_nodes(
                    "There can be only one input field named "
                    f"< {field_name} >.",
                    nodes=[self._known_input_fields[field_name], node.name],
                )
            )
