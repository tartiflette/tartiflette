from typing import Dict, List, Optional, Union

from tartiflette.language.ast import (
    EnumTypeDefinitionNode,
    InterfaceTypeDefinitionNode,
    ObjectTypeDefinitionNode,
    ScalarTypeDefinitionNode,
    UnionTypeDefinitionNode,
)
from tartiflette.language.ast.base import TypeDefinitionNode
from tartiflette.language.utils import get_wrapped_named_type
from tartiflette.language.visitor.constants import SKIP
from tartiflette.utils.errors import graphql_error_from_nodes
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("ValidFieldDefinitionTypesRule",)

_OUTPUT_TYPES = (
    ScalarTypeDefinitionNode,
    ObjectTypeDefinitionNode,
    InterfaceTypeDefinitionNode,
    UnionTypeDefinitionNode,
    EnumTypeDefinitionNode,
)


class ValidFieldDefinitionTypesRule(ASTValidationRule):
    """
    Validate that field definitions are output types.
    """

    def __init__(self, context: "ASTValidationContext") -> None:
        """
        :param context: context forwarded to the validation rule
        :type context: ASTValidationContext
        """
        super().__init__(context)
        self._defined_types: Dict[str, "TypeDefinitionNode"] = {
            definition_node.name.value: definition_node
            for definition_node in context.document_node.definitions
            if isinstance(definition_node, TypeDefinitionNode)
        }

    def enter_FieldDefinition(  # pylint: disable=invalid-name
        self,
        node: "FieldDefinitionNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> SKIP:
        """
        Check that field definition is output type.
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
        :return: the SKIP visitor constant
        :rtype: SKIP
        """
        # pylint: disable=unused-argument
        parent_name = ancestors[-1].name.value
        wrapped_field_type_name = get_wrapped_named_type(node.type)
        wrapped_field_type = (
            self._defined_types.get(wrapped_field_type_name.name.value)
            if wrapped_field_type_name
            else None
        )
        if not isinstance(wrapped_field_type, _OUTPUT_TYPES):
            self.context.report_error(
                graphql_error_from_nodes(
                    f"The type of < {parent_name}.{node.name.value} > must be "
                    f"Output type but got: {node.type}.",
                    nodes=[node.type],
                )
            )
        return SKIP
