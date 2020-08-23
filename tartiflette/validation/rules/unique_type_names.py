from typing import List, Optional, Union

from tartiflette.collections.unique_mapping import (
    AlreadyDefinedException,
    UniqueMapping,
)
from tartiflette.language.visitor.constants import SKIP
from tartiflette.utils.errors import graphql_error_from_nodes
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("UniqueTypeNamesRule",)


class UniqueTypeNamesRule(ASTValidationRule):
    """
    A GraphQL document is only valid if all defined types have unique
    names.
    """

    def __init__(self, context: "ASTValidationContext") -> None:
        """
        :param context: context forwarded to the validation rule
        :type context: ASTValidationContext
        """
        super().__init__(context)
        self._known_type_names = UniqueMapping()

    def _check_type_name_uniqueness(
        self,
        node: [
            "ScalarTypeDefinitionNode",
            "ObjectTypeDefinitionNode",
            "InterfaceTypeDefinitionNode",
            "UnionTypeDefinitionNode",
            "EnumTypeDefinitionNode",
            "InputObjectTypeDefinitionNode",
        ],
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> SKIP:
        """
        Check that the name of the type definition isn't already used.
        :param node: the current node being visiting
        :param key: the index/key to this node from the parent node/list
        :param parent: the parent immediately above this node
        :param path: the path to get to this node from the root node
        :param ancestors: nodes and list visited before reaching parent node
        :type node: [
            "ScalarTypeDefinitionNode",
            "ObjectTypeDefinitionNode",
            "InterfaceTypeDefinitionNode",
            "UnionTypeDefinitionNode",
            "EnumTypeDefinitionNode",
            "InputObjectTypeDefinitionNode",
        ]
        :type key: Optional[Union[int, str]]
        :type parent: Optional[Union[Node, List[Node]]]
        :type path: List[Union[int, str]]
        :type ancestors: List[Union[Node, List[Node]]]
        :return: the SKIP visitor constant
        :rtype: SKIP
        """
        # pylint: disable=unused-argument
        type_name = node.name.value
        try:
            self._known_type_names[type_name] = node.name
        except AlreadyDefinedException:
            self.context.report_error(
                graphql_error_from_nodes(
                    f"There can be only one type named < {type_name} >.",
                    nodes=[self._known_type_names[type_name], node.name],
                )
            )

        return SKIP

    enter_ScalarTypeDefinition = _check_type_name_uniqueness
    enter_ObjectTypeDefinition = _check_type_name_uniqueness
    enter_InterfaceTypeDefinition = _check_type_name_uniqueness
    enter_UnionTypeDefinition = _check_type_name_uniqueness
    enter_EnumTypeDefinition = _check_type_name_uniqueness
    enter_InputObjectTypeDefinition = _check_type_name_uniqueness
