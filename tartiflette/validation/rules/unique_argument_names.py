from functools import partial
from typing import Dict, List, Optional, Union

from tartiflette.language.visitor.constants import SKIP
from tartiflette.utils.errors import (
    graphql_error_from_nodes as raw_graphql_error_from_nodes,
)
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("UniqueArgumentNamesRule",)


graphql_error_from_nodes = partial(
    raw_graphql_error_from_nodes,
    extensions={
        "spec": "June 2018",
        "rule": "5.4.2",
        "tag": "argument-uniqueness",
        "details": "http://spec.graphql.org/June2018/#sec-Argument-Uniqueness",
    },
)


class UniqueArgumentNamesRule(ASTValidationRule):
    """
    A GraphQL field or directive is only valid if all supplied arguments
    are uniquely named.
    """

    def __init__(self, context: "ASTValidationContext") -> None:
        """
        :param context: context forwarded to the validation rule
        :type context: ASTValidationContext
        """
        super().__init__(context)
        self._known_argument_names: Dict[str, "NameNode"] = {}

    def enter_Field(  # pylint: disable=invalid-name
        self,
        node: "FieldNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> None:
        """
        Clear the known argument names for the new field.
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
        self._known_argument_names: Dict[str, "NameNode"] = {}

    def enter_Directive(  # pylint: disable=invalid-name
        self,
        node: "DirectiveNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> None:
        """
        Clear the known argument names for the new directive.
        :param node: the current node being visiting
        :param key: the index/key to this node from the parent node/list
        :param parent: the parent immediately above this node
        :param path: the path to get to this node from the root node
        :param ancestors: nodes and list visited before reaching parent node
        :type node: DirectiveNode
        :type key: Optional[Union[int, str]]
        :type parent: Optional[Union[Node, List[Node]]]
        :type path: List[Union[int, str]]
        :type ancestors: List[Union[Node, List[Node]]]
        """
        # pylint: disable=unused-argument
        self._known_argument_names: Dict[str, "NameNode"] = {}

    def enter_Argument(  # pylint: disable=invalid-name
        self,
        node: "ArgumentNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> SKIP:
        """
        Check that field or directive have unique arguments.
        :param node: the current node being visiting
        :param key: the index/key to this node from the parent node/list
        :param parent: the parent immediately above this node
        :param path: the path to get to this node from the root node
        :param ancestors: nodes and list visited before reaching parent node
        :type node: ArgumentNode
        :type key: Optional[Union[int, str]]
        :type parent: Optional[Union[Node, List[Node]]]
        :type path: List[Union[int, str]]
        :type ancestors: List[Union[Node, List[Node]]]
        :return: the SKIP visitor constant
        :rtype: SKIP
        """
        # pylint: disable=unused-argument
        argument_name = node.name.value
        known_argument = self._known_argument_names.get(argument_name)
        if known_argument:
            self.context.report_error(
                graphql_error_from_nodes(
                    "There can be only one argument named "
                    f"< {argument_name} >.",
                    nodes=[known_argument, node.name],
                )
            )
        else:
            self._known_argument_names[argument_name] = node.name
        return SKIP
