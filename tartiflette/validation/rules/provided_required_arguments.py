from functools import partial
from typing import Any, Dict, List, Optional, Union

from tartiflette.language.ast import DirectiveDefinitionNode, NonNullTypeNode
from tartiflette.language.ast.base import Node
from tartiflette.language.visitor.constants import SKIP
from tartiflette.types.non_null import GraphQLNonNull
from tartiflette.utils.errors import (
    graphql_error_from_nodes as raw_graphql_error_from_nodes,
)
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("ProvidedRequiredArgumentsOnDirectivesRule",)


graphql_error_from_nodes = partial(
    raw_graphql_error_from_nodes,
    extensions={
        "spec": "June 2018",
        "rule": "5.4.2.1",
        "tag": "required-arguments",
        "details": "https://spec.graphql.org/June2018/#sec-Required-Arguments",
    },
)


def _is_required_argument(argument: "GraphQLArgument") -> bool:
    """
    Determine whether or not a GraphQLArgument is required.
    :param argument: the GraphQLArgument instance to check
    :type argument: GraphQLArgument
    :return: whether or not a GraphQLArgument is required
    :rtype: bool
    """
    return (
        isinstance(argument.graphql_type, GraphQLNonNull)
        and argument.default_value is None
    )


def _is_required_argument_node(argument: "ArgumentNode") -> bool:
    """
    Determine whether or not an ArgumentNode is required.
    :param argument: the ArgumentNode instance to check
    :type argument: ArgumentNode
    :return: whether or not an ArgumentNode is required
    :rtype: bool
    """
    return (
        isinstance(argument.type, NonNullTypeNode)
        and argument.default_value is None
    )


class ProvidedRequiredArgumentsOnDirectivesRule(ASTValidationRule):
    """
    A directive is only valid if all required (non-null without a
    default value) field arguments have been provided.
    """

    def __init__(self, context: "ASTValidationContext") -> None:
        """
        :param context: context forwarded to the validation rule
        :type context: ASTValidationContext
        """
        super().__init__(context)
        self._directive_required_arguments: Dict[str, Dict[str, Any]] = (
            {
                directive.name: {
                    argument_name: argument
                    for argument_name, argument in directive.arguments.items()
                    if _is_required_argument(argument)
                }
                for directive in context.schema.directive_definitions.values()
            }
            if context.schema
            else {}
        )
        self._directive_required_arguments.update(
            {
                directive_definition.name.value: (
                    {
                        argument.name.value: argument
                        for argument in directive_definition.arguments
                        if _is_required_argument_node(argument)
                    }
                    if directive_definition.arguments
                    else {}
                )
                for directive_definition in context.document_node.definitions
                if isinstance(directive_definition, DirectiveDefinitionNode)
            }
        )

    def leave_Directive(  # pylint: disable=invalid-name
        self,
        node: "DirectiveNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> None:
        """
        Check that directive required arguments are provided.
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
        directive_name = node.name.value
        required_arguments = self._directive_required_arguments.get(
            directive_name
        )

        if required_arguments:
            argument_nodes = {
                argument_node.name.value: argument_node
                for argument_node in node.arguments or []
            }
            for argument_name in required_arguments:
                if argument_name not in argument_nodes:
                    required_argument = required_arguments[argument_name]
                    argument_type = (
                        required_argument.type
                        if isinstance(required_argument, Node)
                        else required_argument.graphql_type
                    )

                    self.context.report_error(
                        graphql_error_from_nodes(
                            f"Directive < @{directive_name} > argument "
                            f"< {argument_name} > of type < {argument_type} > "
                            "required, but it was not provided.",
                            nodes=[node],
                        )
                    )


class ProvidedRequiredArgumentsRule(ProvidedRequiredArgumentsOnDirectivesRule):
    """
    A field or directive is only valid if all required (non-null without
    a default value) field arguments have been provided.
    """

    def leave_Field(  # pylint: disable=invalid-name
        self,
        node: "FieldNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> Optional["SKIP"]:
        """
        Check that field required arguments are provided.
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
        :return: the SKIP visitor constant or None
        :rtype: Optional["SKIP"]
        """
        # pylint: disable=unused-argument
        field_definition = self.context.get_field_def()
        if not field_definition:
            return SKIP

        argument_nodes = node.arguments or []
        argument_node_map = {
            argument.name.value: argument for argument in argument_nodes
        }

        for (
            argument_name,
            argument_definition,
        ) in field_definition.arguments.items():
            argument_node = argument_node_map.get(argument_name)
            if not argument_node and _is_required_argument(
                argument_definition
            ):
                self.context.report_error(
                    graphql_error_from_nodes(
                        f"Field < {field_definition.name} > argument "
                        f"< {argument_name} > of type "
                        f"< {argument_definition.type} > is required, but it "
                        "was not provided.",
                        nodes=[node],
                    )
                )
        return None
