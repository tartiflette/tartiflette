from collections import defaultdict
from typing import List, Optional, Union

from tartiflette.collections.unique_mapping import (
    AlreadyDefinedException,
    UniqueMapping,
)
from tartiflette.language.visitor.constants import SKIP
from tartiflette.utils.errors import graphql_error_from_nodes
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("UniqueInterfaceImplementationRule",)


class UniqueInterfaceImplementationRule(ASTValidationRule):
    """
    An object type may declare that it implements one or more unique
    interfaces.
    """

    def __init__(self, context: "ASTValidationContext") -> None:
        """
        :param context: context forwarded to the validation rule
        :type context: ASTValidationContext
        """
        super().__init__(context)
        self._known_implements = defaultdict(UniqueMapping)

    def _check_implements_unique_interfaces(
        self,
        node: Union["ObjectTypeDefinitionNode", "ObjectTypeExtensionNode",],
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> SKIP:
        """
        Check that object type implements unique interfaces.
        :param node: the current node being visiting
        :param key: the index/key to this node from the parent node/list
        :param parent: the parent immediately above this node
        :param path: the path to get to this node from the root node
        :param ancestors: nodes and list visited before reaching parent node
        :type node: Union[
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
        if node.interfaces:
            type_name = node.name.value
            implemented = self._known_implements[type_name]

            for implemented_interface in node.interfaces:
                interface_name = implemented_interface.name.value
                try:
                    implemented[interface_name] = implemented_interface.name
                except AlreadyDefinedException:
                    self.context.report_error(
                        graphql_error_from_nodes(
                            f"Type < {type_name} > can only implement "
                            f"< {interface_name} > once.",
                            nodes=[
                                implemented[interface_name],
                                implemented_interface.name,
                            ],
                        )
                    )
        return SKIP

    enter_ObjectTypeDefinition = _check_implements_unique_interfaces
    enter_ObjectTypeExtension = _check_implements_unique_interfaces
