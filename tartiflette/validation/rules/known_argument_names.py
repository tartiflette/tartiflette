from difflib import get_close_matches
from functools import partial
from typing import Dict, List, Optional, Union

from tartiflette.language.ast import DirectiveDefinitionNode
from tartiflette.language.visitor.constants import SKIP
from tartiflette.utils.errors import (
    did_you_mean,
    graphql_error_from_nodes as raw_graphql_error_from_nodes,
)
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("KnownArgumentNamesOnDirectivesRule", "KnownArgumentNamesRule")


graphql_error_from_nodes = partial(
    raw_graphql_error_from_nodes,
    extensions={
        "spec": "June 2018",
        "rule": "5.4.1",
        "tag": "argument-names",
        "details": "https://spec.graphql.org/June2018/#sec-Argument-Names",
    },
)


class KnownArgumentNamesOnDirectivesRule(ASTValidationRule):
    """
    A GraphQL directive is only valid if all supplied arguments are
    defined by that directive.
    """

    def __init__(self, context: "ASTValidationContext") -> None:
        """
        :param context: context forwarded to the validation rule
        :type context: ASTValidationContext
        """
        super().__init__(context)
        self._directive_arguments: Dict[str, List[str]] = (
            {
                directive.name: list(directive.arguments.keys())
                for directive in context.schema.directive_definitions.values()
            }
            if context.schema
            else {}
        )
        self._directive_arguments.update(
            {
                directive_definition.name.value: (
                    [
                        argument.name.value
                        for argument in directive_definition.arguments
                    ]
                    if directive_definition.arguments
                    else []
                )
                for directive_definition in context.document_node.definitions
                if isinstance(directive_definition, DirectiveDefinitionNode)
            }
        )

    def enter_Directive(  # pylint: disable=invalid-name
        self,
        node: "DirectiveNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> SKIP:
        """
        Check that directive supplied arguments are defined.
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
        :return: the SKIP visitor constant
        :rtype: SKIP
        """
        # pylint: disable=unused-argument
        directive_name = node.name.value
        known_arguments = self._directive_arguments.get(directive_name)

        if known_arguments is not None and node.arguments:
            for argument_node in node.arguments:
                argument_name = argument_node.name.value
                if argument_name not in known_arguments:
                    suggestions = get_close_matches(
                        argument_name, known_arguments, n=5
                    )
                    error_message = (
                        f"Unknown argument < {argument_name} > on directive "
                        f"< @{directive_name} >."
                    )
                    if suggestions:
                        error_message = (
                            f"{error_message} {did_you_mean(suggestions)}"
                        )
                    self.context.report_error(
                        graphql_error_from_nodes(
                            error_message, nodes=[argument_node]
                        )
                    )
        return SKIP


class KnownArgumentNamesRule(KnownArgumentNamesOnDirectivesRule):
    """
    A GraphQL field or directive are only valid if all supplied
    arguments are defined by that directive.
    """

    def enter_Argument(  # pylint: disable=invalid-name
        self,
        node: "ArgumentNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> None:
        """
        Check that argument related to a field are defined by the field.
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
        """
        # pylint: disable=unused-argument
        argument_definition = self.context.get_argument()
        field_definition = self.context.get_field_def()
        parent_type = self.context.get_parent_type()

        if not argument_definition and field_definition and parent_type:
            argument_name = node.name.value
            suggestions = get_close_matches(
                argument_name, field_definition.arguments.keys(), n=5
            )
            error_message = (
                f"Unknown argument < {argument_name} > on field "
                f"< {parent_type.name}.{field_definition.name} >."
            )
            if suggestions:
                error_message = f"{error_message} {did_you_mean(suggestions)}"
            self.context.report_error(
                graphql_error_from_nodes(error_message, nodes=[node])
            )
