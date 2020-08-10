from difflib import get_close_matches
from typing import Dict, List, Optional, Union

from tartiflette.language.ast import (
    EnumTypeDefinitionNode,
    EnumTypeExtensionNode,
    InputObjectTypeDefinitionNode,
    InputObjectTypeExtensionNode,
    InterfaceTypeDefinitionNode,
    InterfaceTypeExtensionNode,
    ObjectTypeDefinitionNode,
    ObjectTypeExtensionNode,
    ScalarTypeDefinitionNode,
    ScalarTypeExtensionNode,
    UnionTypeDefinitionNode,
    UnionTypeExtensionNode,
)
from tartiflette.language.ast.base import TypeDefinitionNode
from tartiflette.types.enum import GraphQLEnumType
from tartiflette.types.input_object import GraphQLInputObjectType
from tartiflette.types.interface import GraphQLInterfaceType
from tartiflette.types.object import GraphQLObjectType
from tartiflette.types.scalar import GraphQLScalarType
from tartiflette.types.union import GraphQLUnionType
from tartiflette.utils.errors import did_you_mean, graphql_error_from_nodes
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("PossibleTypeExtensionsRule",)


_EXTENSION_TO_TYPE_NAME = {
    ScalarTypeExtensionNode: "scalar",
    ObjectTypeExtensionNode: "object",
    InterfaceTypeExtensionNode: "interface",
    UnionTypeExtensionNode: "union",
    EnumTypeExtensionNode: "enum",
    InputObjectTypeExtensionNode: "input object",
}

_DEFINITION_TO_EXTENSION_CLASS = {
    ScalarTypeDefinitionNode: ScalarTypeExtensionNode,
    ObjectTypeDefinitionNode: ObjectTypeExtensionNode,
    InterfaceTypeDefinitionNode: InterfaceTypeExtensionNode,
    UnionTypeDefinitionNode: UnionTypeExtensionNode,
    EnumTypeDefinitionNode: EnumTypeExtensionNode,
    InputObjectTypeDefinitionNode: InputObjectTypeExtensionNode,
}

_GRAPHQL_TYPE_TO_EXTENSION_CLASS = {
    GraphQLScalarType: ScalarTypeExtensionNode,
    GraphQLObjectType: ObjectTypeExtensionNode,
    GraphQLInterfaceType: InterfaceTypeExtensionNode,
    GraphQLUnionType: UnionTypeExtensionNode,
    GraphQLEnumType: EnumTypeExtensionNode,
    GraphQLInputObjectType: InputObjectTypeExtensionNode,
}


class PossibleTypeExtensionsRule(ASTValidationRule):
    """
    A type extension is only valid if the type is defined and has the
    same kind.
    """

    def __init__(self, context: "ASTValidationContext") -> None:
        """
        :param context: context forwarded to the validation rule
        :type context: ASTValidationContext
        """
        super().__init__(context)
        self._known_types: Dict[str, "TypeDefinitionNode"] = {
            definition_node.name.value: definition_node
            for definition_node in context.document_node.definitions
            if isinstance(definition_node, TypeDefinitionNode)
        }

    def _check_extension_validness(
        self,
        node: Union[
            "InputObjectTypeExtensionNode",
            "InterfaceTypeExtensionNode",
            "ScalarTypeExtensionNode",
            "ObjectTypeExtensionNode",
            "UnionTypeExtensionNode",
            "EnumTypeExtensionNode",
        ],
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> None:
        """
        Check that extension is on defined type of same kind.
        :param node: the current node being visiting
        :param key: the index/key to this node from the parent node/list
        :param parent: the parent immediately above this node
        :param path: the path to get to this node from the root node
        :param ancestors: nodes and list visited before reaching parent node
        :type node: Union[
            InputObjectTypeExtensionNode,
            InterfaceTypeExtensionNode,
            ScalarTypeExtensionNode,
            ObjectTypeExtensionNode,
            UnionTypeExtensionNode,
            EnumTypeExtensionNode,
        ]
        :type key: Optional[Union[int, str]]
        :type parent: Optional[Union[Node, List[Node]]]
        :type path: List[Union[int, str]]
        :type ancestors: List[Union[Node, List[Node]]]
        """
        # pylint: disable=unused-argument
        type_name = node.name.value
        definition_node = self._known_types.get(type_name)

        if definition_node:
            expected_kind = _DEFINITION_TO_EXTENSION_CLASS.get(
                type(definition_node)
            )
            if not isinstance(node, expected_kind):
                kind = _EXTENSION_TO_TYPE_NAME.get(
                    expected_kind, "unknown type"
                )
                self.context.report_error(
                    graphql_error_from_nodes(
                        f"Cannot extend non-{kind} type < {type_name} >.",
                        nodes=[definition_node, node],
                    )
                )
        else:
            suggestions = get_close_matches(
                type_name, list(self._known_types), n=5
            )
            error_message = (
                f"Cannot extend type < {type_name} > because it is not "
                "defined."
            )
            if suggestions:
                error_message = f"{error_message} {did_you_mean(suggestions)}"
            self.context.report_error(
                graphql_error_from_nodes(error_message, nodes=[node.name])
            )

    enter_InputObjectTypeExtension = _check_extension_validness
    enter_InterfaceTypeExtension = _check_extension_validness
    enter_ScalarTypeExtension = _check_extension_validness
    enter_ObjectTypeExtension = _check_extension_validness
    enter_UnionTypeExtension = _check_extension_validness
    enter_EnumTypeExtension = _check_extension_validness
