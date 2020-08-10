from typing import Dict, List, Optional, Set, Union

from tartiflette.language.ast import (
    UnionTypeDefinitionNode,
    UnionTypeExtensionNode,
)
from tartiflette.utils.errors import graphql_error_from_nodes
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("HasMemberDefinedRule",)


class HasMemberDefinedRule(ASTValidationRule):
    """
    A Union type must include one or more member types.
    """

    def __init__(self, context: "ASTValidationContext") -> None:
        """
        :param context: context forwarded to the validation rule
        :type context: ASTValidationContext
        """
        super().__init__(context)
        self._union_with_members: Set[str] = set()

        self._known_union_definitions: Dict[
            str, List["UnionTypeDefinitionNode"]
        ] = {}
        self._known_union_extensions: Dict[
            str, List["UnionTypeExtensionNode"]
        ] = {}
        for definition_node in context.document_node.definitions:
            if isinstance(definition_node, UnionTypeDefinitionNode):
                self._known_union_definitions.setdefault(
                    definition_node.name.value, []
                ).append(definition_node)
            elif isinstance(definition_node, UnionTypeExtensionNode):
                self._known_union_extensions.setdefault(
                    definition_node.name.value, []
                ).append(definition_node)

    def enter_NamedType(  # pylint: disable=invalid-name
        self,
        node: "NamedTypeNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> None:
        """
        Mark the parent union as having member types.
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
        try:
            self._union_with_members.add(ancestors[-1].name.value)
        except Exception:  # pylint: disable=broad-except
            return

    def leave_Document(  # pylint: disable=invalid-name
        self,
        node: "DocumentNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> None:
        """
        Check that defined union has one or more members.
        :param node: the current node being visiting
        :param key: the index/key to this node from the parent node/list
        :param parent: the parent immediately above this node
        :param path: the path to get to this node from the root node
        :param ancestors: nodes and list visited before reaching parent node
        :type node: DocumentNode
        :type key: Optional[Union[int, str]]
        :type parent: Optional[Union[Node, List[Node]]]
        :type path: List[Union[int, str]]
        :type ancestors: List[Union[Node, List[Node]]]
        """
        # pylint: disable=unused-argument
        for (
            known_union_name,
            definitions,
        ) in self._known_union_definitions.items():
            if known_union_name not in self._union_with_members:
                union_extensions = self._known_union_extensions.get(
                    known_union_name, []
                )
                self.context.report_error(
                    graphql_error_from_nodes(
                        f"Union type < {known_union_name} > must define one "
                        "or more member types.",
                        nodes=definitions + union_extensions,
                    )
                )
