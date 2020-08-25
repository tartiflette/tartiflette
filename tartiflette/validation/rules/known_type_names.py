from difflib import get_close_matches
from typing import List, Optional, Set, Union

from tartiflette.constants.introspection import INTROSPECTION_TYPE_NAMES
from tartiflette.constants.scalars import BUILTIN_SCALAR_NAMES
from tartiflette.language.ast.base import (
    TypeDefinitionNode,
    TypeSystemDefinitionNode,
    TypeSystemExtensionNode,
)
from tartiflette.utils.errors import did_you_mean, graphql_error_from_nodes
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("KnownTypeNamesRule",)


_TYPE_SYSTEM_NODES = (TypeSystemDefinitionNode, TypeSystemExtensionNode)

_BUILTIN_TYPE_NAMES = set(INTROSPECTION_TYPE_NAMES + BUILTIN_SCALAR_NAMES)


def _is_sdl_node(node: Optional["Node"]) -> bool:
    """
    Determine whether or not the node is a SDL node.
    :param node: the node to check
    :type node: Node
    :return: whether or not the node is a SDL node
    :rtype: bool
    """
    return (
        node is not None
        and not isinstance(node, list)
        and isinstance(node, _TYPE_SYSTEM_NODES)
    )


def _is_builtin_type_name(type_name: str) -> bool:
    """
    Determine whether or not the type name is a builtin one.

    :param type_name: the type name to check
    :type type_name: str
    :return: whether or not the type name is a builtin one.
    :rtype: bool
    """
    return type_name in _BUILTIN_TYPE_NAMES


class KnownTypeNamesRule(ASTValidationRule):
    """
    A GraphQL document is only valid if referenced types (specifically
    variable definitions and fragment conditions) are defined by the
    type schema.
    """

    def __init__(self, context: "ASTValidationContext") -> None:
        """
        :param context: context forwarded to the validation rule
        :type context: ASTValidationContext
        """
        super().__init__(context)
        schema = context.schema
        existing_types: Set[str] = (
            set(schema.type_definitions) if schema else set()
        )
        defined_types: Set[str] = {
            definition_node.name.value
            for definition_node in context.document_node.definitions
            if isinstance(definition_node, TypeDefinitionNode)
        }
        self._known_type_names = existing_types | defined_types

    def enter_NamedType(  # pylint: disable=invalid-name
        self,
        node: "NamedTypeNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> None:
        """
        Check that the named type refer to a defined type.
        :param node: the current node being visiting
        :param key: the index/key to this node from the parent node/list
        :param parent: the parent immediately above this node
        :param path: the path to get to this node from the root node
        :param ancestors: nodes and list visited before reaching parent node
        :type node: NamedTypeNode
        :type key: Optional[Union[int, str]]
        :type parent: Optional[Union[Node, List[Node]]]
        :type path: List[Union[int, str]]
        :type ancestors: List[Union[Node, List[Node]]]
        """
        # pylint: disable=unused-argument
        type_name = node.name.value
        if type_name not in self._known_type_names:
            try:
                definition_node = ancestors[2]
            except IndexError:
                definition_node = parent

            is_sdl_node = _is_sdl_node(definition_node)
            if is_sdl_node and _is_builtin_type_name(type_name):
                return

            suggestions = get_close_matches(
                type_name,
                self._known_type_names
                if not is_sdl_node
                else self._known_type_names | _BUILTIN_TYPE_NAMES,
                n=5,
            )
            error_message = f"Unknown type < {type_name} >."
            if suggestions:
                error_message = f"{error_message} {did_you_mean(suggestions)}"
            self.context.report_error(
                graphql_error_from_nodes(
                    error_message,
                    nodes=[node],
                    extensions=(
                        {
                            "spec": "June 2018",
                            "rule": "5.5.1.2",
                            "tag": "fragment-spread-type-existence",
                            "details": "https://spec.graphql.org/June2018/#sec-Fragment-Spread-Type-Existence",
                        }
                        if not _is_sdl_node(definition_node)
                        else None
                    ),
                )
            )
