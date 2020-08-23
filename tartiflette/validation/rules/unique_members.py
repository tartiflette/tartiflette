from collections import defaultdict
from typing import List, Optional, Union

from tartiflette.collections.unique_mapping import (
    AlreadyDefinedException,
    UniqueMapping,
)
from tartiflette.language.visitor.constants import SKIP
from tartiflette.utils.errors import graphql_error_from_nodes
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("UniqueMembersRule",)


class UniqueMembersRule(ASTValidationRule):
    """
    A Union type must include one or more unique member types.
    """

    def __init__(self, context: "ASTValidationContext") -> None:
        """
        :param context: context forwarded to the validation rule
        :type context: ASTValidationContext
        """
        super().__init__(context)
        self._known_members = defaultdict(UniqueMapping)

    def _check_member_uniqueness(
        self,
        node: Union["UnionTypeDefinitionNode", "UnionTypeExtensionNode",],
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> SKIP:
        """
        Check that members of union type are unique.
        :param node: the current node being visiting
        :param key: the index/key to this node from the parent node/list
        :param parent: the parent immediately above this node
        :param path: the path to get to this node from the root node
        :param ancestors: nodes and list visited before reaching parent node
        :type node: Union[
            "UnionTypeDefinitionNode",
            "UnionTypeExtensionNode",
        ]
        :type key: Optional[Union[int, str]]
        :type parent: Optional[Union[Node, List[Node]]]
        :type path: List[Union[int, str]]
        :type ancestors: List[Union[Node, List[Node]]]
        :return: the SKIP visitor constant
        :rtype: SKIP
        """
        # pylint: disable=unused-argument
        if node.types:
            union_name = node.name.value
            member_names = self._known_members[union_name]
            for member in node.types:
                member_name = member.name.value
                try:
                    member_names[member_name] = member.name
                except AlreadyDefinedException:
                    self.context.report_error(
                        graphql_error_from_nodes(
                            f"Union type < {union_name} > can only include "
                            f"type < {member_name} > once.",
                            nodes=[member_names[member_name], member.name],
                        )
                    )
        return SKIP

    enter_UnionTypeDefinition = _check_member_uniqueness
    enter_UnionTypeExtension = _check_member_uniqueness
