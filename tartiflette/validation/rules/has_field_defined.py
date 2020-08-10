from typing import Dict, List, Optional, Set, Union

from tartiflette.language.ast import (
    InterfaceTypeDefinitionNode,
    InterfaceTypeExtensionNode,
    ObjectTypeDefinitionNode,
    ObjectTypeExtensionNode,
)
from tartiflette.utils.errors import graphql_error_from_nodes
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("HasFieldDefinedRule",)


class HasFieldDefinedRule(ASTValidationRule):
    """
    An Object or Interface type must define one or more fields.
    """

    def __init__(self, context: "ASTValidationContext") -> None:
        """
        :param context: context forwarded to the validation rule
        :type context: ASTValidationContext
        """
        super().__init__(context)
        self._types_with_fields: Set[str] = set()

        self._known_type_definitions: Dict[
            str, List["TypeDefinitionNode"]
        ] = {}
        self._known_type_extensions: Dict[str, List["TypeExtensionNode"]] = {}
        for definition_node in context.document_node.definitions:
            if isinstance(
                definition_node,
                (InterfaceTypeDefinitionNode, ObjectTypeDefinitionNode),
            ):
                self._known_type_definitions.setdefault(
                    definition_node.name.value, []
                ).append(definition_node)
            elif isinstance(
                definition_node,
                (InterfaceTypeExtensionNode, ObjectTypeExtensionNode),
            ):
                self._known_type_extensions.setdefault(
                    definition_node.name.value, []
                ).append(definition_node)

    def enter_FieldDefinition(  # pylint: disable=invalid-name
        self,
        node: "FieldDefinitionNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> None:
        """
        Mark the parent type as having fields.
        :param node: the current node being visiting
        :param key: the index/key to this node from the parent node/list
        :param parent: the parent immediately above this node
        :param path: the path to get to this node from the root node
        :param ancestors: nodes and list visited before reaching parent node
        :type node: FieldDefinitionNode
        :type key: Optional[Union[int, str]]
        :type parent: Optional[Union[Node, List[Node]]]
        :type path: List[Union[int, str]]
        :type ancestors: List[Union[Node, List[Node]]]
        """
        # pylint: disable=unused-argument
        self._types_with_fields.add(ancestors[-1].name.value)

    def leave_Document(  # pylint: disable=invalid-name
        self,
        node: "DocumentNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> None:
        """
        Check that defined types has one or more fields.
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
            known_type_name,
            definitions,
        ) in self._known_type_definitions.items():
            if known_type_name not in self._types_with_fields:
                type_extensions = self._known_type_extensions.get(
                    known_type_name, []
                )
                self.context.report_error(
                    graphql_error_from_nodes(
                        f"Type < {known_type_name} > must define one or more "
                        "fields.",
                        nodes=definitions + type_extensions,
                    )
                )
