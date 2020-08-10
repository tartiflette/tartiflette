from typing import Dict, List, Optional, Set, Union

from tartiflette.language.ast import (
    EnumTypeDefinitionNode,
    EnumTypeExtensionNode,
)
from tartiflette.utils.errors import graphql_error_from_nodes
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("HasEnumValueDefinedRule",)


class HasEnumValueDefinedRule(ASTValidationRule):
    """
    An Enum type must define one or more enum values.
    """

    def __init__(self, context: "ASTValidationContext") -> None:
        """
        :param context: context forwarded to the validation rule
        :type context: ASTValidationContext
        """
        super().__init__(context)
        self._enum_with_values: Set[str] = set()

        self._known_enum_definitions: Dict[
            str, List["EnumTypeDefinitionNode"]
        ] = {}
        self._known_enum_extensions: Dict[
            str, List["EnumTypeExtensionNode"]
        ] = {}
        for definition_node in context.document_node.definitions:
            if isinstance(definition_node, EnumTypeDefinitionNode):
                self._known_enum_definitions.setdefault(
                    definition_node.name.value, []
                ).append(definition_node)
            elif isinstance(definition_node, EnumTypeExtensionNode):
                self._known_enum_extensions.setdefault(
                    definition_node.name.value, []
                ).append(definition_node)

    def enter_EnumValueDefinition(  # pylint: disable=invalid-name
        self,
        node: "EnumValueDefinitionNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> None:
        """
        Mark the parent enum type as having enum values.
        :param node: the current node being visiting
        :param key: the index/key to this node from the parent node/list
        :param parent: the parent immediately above this node
        :param path: the path to get to this node from the root node
        :param ancestors: nodes and list visited before reaching parent node
        :type node: EnumValueDefinitionNode
        :type key: Optional[Union[int, str]]
        :type parent: Optional[Union[Node, List[Node]]]
        :type path: List[Union[int, str]]
        :type ancestors: List[Union[Node, List[Node]]]
        """
        # pylint: disable=unused-argument
        self._enum_with_values.add(ancestors[-1].name.value)

    def leave_Document(  # pylint: disable=invalid-name
        self,
        node: "DocumentNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> None:
        """
        Check that defined enum types has one or more enum values.
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
        ) in self._known_enum_definitions.items():
            if known_type_name not in self._enum_with_values:
                enum_type_extensions = self._known_enum_extensions.get(
                    known_type_name, []
                )
                self.context.report_error(
                    graphql_error_from_nodes(
                        f"Enum type < {known_type_name} > must define one or "
                        "more values.",
                        nodes=definitions + enum_type_extensions,
                    )
                )
