from typing import Dict, List, Optional, Union

from tartiflette.language.visitor.constants import SKIP
from tartiflette.utils.errors import graphql_error_from_nodes
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("UniqueFieldDefinitionNamesRule",)


class UniqueFieldDefinitionNamesRule(ASTValidationRule):
    """
    A GraphQL complex type is only valid if all its fields are uniquely
    named.
    """

    def __init__(self, context: "ASTValidationContext") -> None:
        """
        :param context: context forwarded to the validation rule
        :type context: ASTValidationContext
        """
        super().__init__(context)
        self._known_field_names: Dict[str, Dict[str, "NameNode"]] = {}

    def _check_field_uniqueness(
        self,
        node: Union[
            "InputObjectTypeDefinitionNode",
            "InputObjectTypeExtensionNode",
            "InterfaceTypeDefinitionNode",
            "InterfaceTypeExtensionNode",
            "ObjectTypeDefinitionNode",
            "ObjectTypeExtensionNode",
        ],
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> SKIP:
        """
        Check complex type has uniquely named fields.
        :param node: the current node being visiting
        :param key: the index/key to this node from the parent node/list
        :param parent: the parent immediately above this node
        :param path: the path to get to this node from the root node
        :param ancestors: nodes and list visited before reaching parent node
        :type node: Union[
            "InputObjectTypeDefinitionNode",
            "InputObjectTypeExtensionNode",
            "InterfaceTypeDefinitionNode",
            "InterfaceTypeExtensionNode",
            "ObjectTypeDefinitionNode",
            "ObjectTypeExtensionNode",
        ]
        :type key: Optional[Union[int, str]]
        :type parent: Optional[Union[Node, List[Node]]]
        :type path: List[Union[int, str]]
        :type ancestors: List[Union[Node, List[Node]]]
        :return: the SKIP visitor constant
        :rtype: SKIP
        """
        # pylint: disable=unused-argument
        if node.fields:
            type_name = node.name.value
            field_names = self._known_field_names.setdefault(type_name, {})
            for field_definition in node.fields:
                field_name = field_definition.name.value
                known_field = field_names.get(field_name)
                if known_field:
                    self.context.report_error(
                        graphql_error_from_nodes(
                            f"Field < {type_name}.{field_name} > can only be "
                            "defined once.",
                            nodes=[known_field, field_definition.name],
                        )
                    )
                else:
                    field_names[field_name] = field_definition.name
        return SKIP

    enter_InputObjectTypeDefinition = _check_field_uniqueness
    enter_InputObjectTypeExtension = _check_field_uniqueness
    enter_InterfaceTypeDefinition = _check_field_uniqueness
    enter_InterfaceTypeExtension = _check_field_uniqueness
    enter_ObjectTypeDefinition = _check_field_uniqueness
    enter_ObjectTypeExtension = _check_field_uniqueness
