from typing import Dict, List, Optional, Union

from tartiflette.language.visitor.constants import SKIP
from tartiflette.utils.errors import graphql_error_from_nodes
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("UniqueEnumValueNamesRule",)


class UniqueEnumValueNamesRule(ASTValidationRule):
    """
    A GraphQL enum type is only valid if all its values are uniquely
    named.
    """

    def __init__(self, context: "ASTValidationContext") -> None:
        """
        :param context: context forwarded to the validation rule
        :type context: ASTValidationContext
        """
        super().__init__(context)
        self._known_enum_value_names: Dict[str, "NameNode"] = {}

    def _check_enum_value_uniqueness(
        self,
        node: Union["EnumTypeDefinitionNode", "EnumTypeExtensionNode"],
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> SKIP:
        """
        Check enum type has unique named values.
        :param node: the current node being visiting
        :param key: the index/key to this node from the parent node/list
        :param parent: the parent immediately above this node
        :param path: the path to get to this node from the root node
        :param ancestors: nodes and list visited before reaching parent node
        :type node: Union["EnumTypeDefinitionNode", "EnumTypeExtensionNode"]
        :type key: Optional[Union[int, str]]
        :type parent: Optional[Union[Node, List[Node]]]
        :type path: List[Union[int, str]]
        :type ancestors: List[Union[Node, List[Node]]]
        :return: the SKIP visitor constant
        :rtype: SKIP
        """
        # pylint: disable=unused-argument
        if node.values:
            enum_type_name = node.name.value
            enum_value_names = self._known_enum_value_names.setdefault(
                enum_type_name, {}
            )
            for value_definition in node.values:
                enum_value_name = value_definition.name.value
                known_enum_value = enum_value_names.get(enum_value_name)
                if known_enum_value:
                    self.context.report_error(
                        graphql_error_from_nodes(
                            "Enum value "
                            f"< {enum_type_name}.{enum_value_name} > "
                            "can only be defined once.",
                            nodes=[known_enum_value, value_definition.name],
                        )
                    )
                else:
                    enum_value_names[enum_value_name] = value_definition.name
        return SKIP

    enter_EnumTypeDefinition = _check_enum_value_uniqueness
    enter_EnumTypeExtension = _check_enum_value_uniqueness
