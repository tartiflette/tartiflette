from typing import Dict, List, Optional, Set, Union

from tartiflette.language.ast import (
    InputObjectTypeDefinitionNode,
    InputObjectTypeExtensionNode,
)
from tartiflette.utils.errors import graphql_error_from_nodes
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("HasInputFieldDefinedRule",)


class HasInputFieldDefinedRule(ASTValidationRule):
    """
    An Input Object type must define one or more input fields.
    """

    def __init__(self, context: "ASTValidationContext") -> None:
        """
        :param context: context forwarded to the validation rule
        :type context: ASTValidationContext
        """
        super().__init__(context)
        self._types_with_fields: Set[str] = set()

        self._known_type_definitions: Dict[
            str, List["InputObjectTypeDefinitionNode"]
        ] = {}
        self._known_type_extensions: Dict[
            str, List["InputObjectTypeExtensionNode"]
        ] = {}
        for definition_node in context.document_node.definitions:
            if isinstance(definition_node, InputObjectTypeDefinitionNode):
                self._known_type_definitions.setdefault(
                    definition_node.name.value, []
                ).append(definition_node)
            elif isinstance(definition_node, InputObjectTypeExtensionNode):
                self._known_type_extensions.setdefault(
                    definition_node.name.value, []
                ).append(definition_node)

    def enter_InputValueDefinition(  # pylint: disable=invalid-name
        self,
        node: "InputValueDefinitionNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> None:
        """
        Mark the parent input object as having input fields.
        :param node: the current node being visiting
        :param key: the index/key to this node from the parent node/list
        :param parent: the parent immediately above this node
        :param path: the path to get to this node from the root node
        :param ancestors: nodes and list visited before reaching parent node
        :type node: InputValueDefinitionNode
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
        Check that defined input object has one or more input fields.
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
                        f"Input Object type < {known_type_name} > must define "
                        "one or more fields.",
                        nodes=definitions + type_extensions,
                    )
                )
