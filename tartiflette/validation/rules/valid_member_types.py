from typing import Dict, List, Optional, Union

from tartiflette.language.ast import ObjectTypeDefinitionNode
from tartiflette.language.ast.base import TypeDefinitionNode
from tartiflette.utils.errors import graphql_error_from_nodes
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("ValidMemberTypesRule",)


class ValidMemberTypesRule(ASTValidationRule):
    """
    The member types of a Union type must all be Object base types;
    Scalar, Interface and Union types must not be member types of a
    Union. Similarly, wrapping types must not be member types of a
    Union.
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
        self._known_members: Dict[str, Dict[str, "NameNode"]] = {}

    def _check_member_uniqueness(
        self,
        node: Union["UnionTypeDefinition", "UnionTypeExtension"],
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> None:
        """
        Collect union member per union type.
        :param node: the current node being visiting
        :param key: the index/key to this node from the parent node/list
        :param parent: the parent immediately above this node
        :param path: the path to get to this node from the root node
        :param ancestors: nodes and list visited before reaching parent node
        :type node: Union[
            "UnionTypeDefinition",
            "UnionTypeExtension",
        ]
        :type key: Optional[Union[int, str]]
        :type parent: Optional[Union[Node, List[Node]]]
        :type path: List[Union[int, str]]
        :type ancestors: List[Union[Node, List[Node]]]
        """
        # pylint: disable=unused-argument
        if node.types:
            for member in node.types:
                self._known_members.setdefault(node.name.value, {}).update(
                    {member.name.value: member.name}
                )

    def leave_Document(  # pylint: disable=invalid-name
        self,
        node: "DocumentNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> None:
        """
        Check that union member types are object type definition.
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
        for union_name, union_members in self._known_members.items():
            for member_name, member_node in union_members.items():
                member_definition = self._defined_types.get(member_name)
                if not isinstance(member_definition, ObjectTypeDefinitionNode):
                    self.context.report_error(
                        graphql_error_from_nodes(
                            f"Union type < {union_name} > can only include "
                            "Object types, it cannot include "
                            f"< {member_name} >.",
                            nodes=[member_node],
                        )
                    )

    enter_UnionTypeDefinition = _check_member_uniqueness
    enter_UnionTypeExtension = _check_member_uniqueness
