from typing import Dict, List, Optional, Union

from tartiflette.language.ast import InterfaceTypeDefinitionNode
from tartiflette.language.ast.base import TypeDefinitionNode
from tartiflette.language.visitor.constants import SKIP
from tartiflette.utils.errors import graphql_error_from_nodes
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("ValidImplementTypesRule",)


class ValidImplementTypesRule(ASTValidationRule):
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
        self._defined_types: Dict[str, "TypeDefinitionNode"] = {
            definition_node.name.value: definition_node
            for definition_node in context.document_node.definitions
            if isinstance(definition_node, TypeDefinitionNode)
        }

    def _check_implements_interface(
        self,
        node: Union["ObjectTypeDefinition", "ObjectTypeExtension"],
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> SKIP:
        """
        Check that object type implements interface types.
        :param node: the current node being visiting
        :param key: the index/key to this node from the parent node/list
        :param parent: the parent immediately above this node
        :param path: the path to get to this node from the root node
        :param ancestors: nodes and list visited before reaching parent node
        :type node: Union[
            "ObjectTypeDefinition",
            "ObjectTypeExtension",
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
            for implemented_interface in node.interfaces:
                interface_name = implemented_interface.name.value
                interface_definition = self._defined_types.get(interface_name)
                if not isinstance(
                    interface_definition, InterfaceTypeDefinitionNode
                ):
                    self.context.report_error(
                        graphql_error_from_nodes(
                            f"Type < {type_name} > must only implement "
                            "Interface types, it cannot implement "
                            f"< {interface_name} >.",
                            nodes=[implemented_interface.name],
                        )
                    )
        return SKIP

    enter_ObjectTypeDefinition = _check_implements_interface
    enter_ObjectTypeExtension = _check_implements_interface
