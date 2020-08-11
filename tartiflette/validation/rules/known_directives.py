from typing import Dict, List, Optional, Union

from tartiflette.constants.directive_locations import (
    ARGUMENT_DEFINITION,
    ENUM,
    ENUM_VALUE,
    FIELD,
    FIELD_DEFINITION,
    FRAGMENT_DEFINITION,
    FRAGMENT_SPREAD,
    INLINE_FRAGMENT,
    INPUT_FIELD_DEFINITION,
    INPUT_OBJECT,
    INTERFACE,
    MUTATION,
    OBJECT,
    QUERY,
    SCALAR,
    SCHEMA,
    SUBSCRIPTION,
    UNION,
    VARIABLE_DEFINITION,
)
from tartiflette.language.ast import (
    DirectiveDefinitionNode,
    EnumTypeDefinitionNode,
    EnumTypeExtensionNode,
    EnumValueDefinitionNode,
    FieldDefinitionNode,
    FieldNode,
    FragmentDefinitionNode,
    FragmentSpreadNode,
    InlineFragmentNode,
    InputObjectTypeDefinitionNode,
    InputObjectTypeExtensionNode,
    InputValueDefinitionNode,
    InterfaceTypeDefinitionNode,
    InterfaceTypeExtensionNode,
    ObjectTypeDefinitionNode,
    ObjectTypeExtensionNode,
    OperationDefinitionNode,
    ScalarTypeDefinitionNode,
    ScalarTypeExtensionNode,
    SchemaDefinitionNode,
    SchemaExtensionNode,
    UnionTypeDefinitionNode,
    UnionTypeExtensionNode,
    VariableDefinitionNode,
)
from tartiflette.language.ast.base import Node
from tartiflette.language.visitor.constants import OK
from tartiflette.utils.errors import graphql_error_from_nodes
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("KnownDirectivesRule",)

_OPERATION_DIRECTIVE_LOCATIONS = {
    "query": QUERY,
    "mutation": MUTATION,
    "subscription": SUBSCRIPTION,
}

_DIRECTIVE_LOCATIONS = {
    FieldNode: FIELD,
    FragmentSpreadNode: FRAGMENT_SPREAD,
    InlineFragmentNode: INLINE_FRAGMENT,
    FragmentDefinitionNode: FRAGMENT_DEFINITION,
    VariableDefinitionNode: VARIABLE_DEFINITION,
    SchemaDefinitionNode: SCHEMA,
    SchemaExtensionNode: SCHEMA,
    ScalarTypeDefinitionNode: SCALAR,
    ScalarTypeExtensionNode: SCALAR,
    ObjectTypeDefinitionNode: OBJECT,
    ObjectTypeExtensionNode: OBJECT,
    FieldDefinitionNode: FIELD_DEFINITION,
    InterfaceTypeDefinitionNode: INTERFACE,
    InterfaceTypeExtensionNode: INTERFACE,
    UnionTypeDefinitionNode: UNION,
    UnionTypeExtensionNode: UNION,
    EnumTypeDefinitionNode: ENUM,
    EnumTypeExtensionNode: ENUM,
    EnumValueDefinitionNode: ENUM_VALUE,
    InputObjectTypeDefinitionNode: INPUT_OBJECT,
    InputObjectTypeExtensionNode: INPUT_OBJECT,
}


def _get_directive_location_for_ast_path(
    ancestors: List[Union[Node, List[Node]]]
) -> Optional[str]:
    """
    Fetch the location of the directive depending on its ancestors.
    :param ancestors: nodes and list visited before reaching parent node
    :type ancestors: List[Union[Node, List[Node]]]
    :return: the location of the directive if found
    :rtype: Optional[str]
    """
    applied_to = ancestors[-1]
    if isinstance(applied_to, Node):
        if isinstance(applied_to, OperationDefinitionNode):
            return _OPERATION_DIRECTIVE_LOCATIONS.get(
                applied_to.operation_type
            )
        if isinstance(applied_to, InputValueDefinitionNode):
            return (
                INPUT_FIELD_DEFINITION
                if isinstance(ancestors[-3], InputObjectTypeDefinitionNode)
                else ARGUMENT_DEFINITION
            )
        return _DIRECTIVE_LOCATIONS.get(type(applied_to))
    return None


class KnownDirectivesRule(ASTValidationRule):
    """
    A GraphQL document is only valid if all `@directives` are known by
    the schema and legally positioned.
    """

    def __init__(self, context: "ASTValidationContext") -> None:
        """
        :param context: context forwarded to the validation rule
        :type context: ASTValidationContext
        """
        super().__init__(context)
        self._directive_location_map: Dict[str, List[str]] = (
            {
                directive.name: directive.locations
                for directive in context.schema.directive_definitions.values()
            }
            if context.schema
            else {}
        )
        self._directive_location_map.update(
            {
                directive_definition.name.value: [
                    location.value
                    for location in directive_definition.locations
                ]
                for directive_definition in context.document_node.definitions
                if isinstance(directive_definition, DirectiveDefinitionNode)
            }
        )

    def enter_Directive(  # pylint: disable=invalid-name
        self,
        node: "DirectiveNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> OK:
        """
        Check that directive are known defined and legally positioned.
        :param node: the current node being visiting
        :param key: the index/key to this node from the parent node/list
        :param parent: the parent immediately above this node
        :param path: the path to get to this node from the root node
        :param ancestors: nodes and list visited before reaching parent node
        :type node: DirectiveNode
        :type key: Optional[Union[int, str]]
        :type parent: Optional[Union[Node, List[Node]]]
        :type path: List[Union[int, str]]
        :type ancestors: List[Union[Node, List[Node]]]
        :return: the OK visitor constant
        :rtype: OK
        """
        # pylint: disable=unused-argument
        directive_name = node.name.value
        directive_locations = self._directive_location_map.get(directive_name)
        if not directive_locations:
            self.context.report_error(
                graphql_error_from_nodes(
                    f"Unknown directive < @{directive_name} >.",
                    nodes=[node],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.1",
                        "tag": "directives-are-defined",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-Defined",
                    },
                )
            )
            return OK

        candidate_location = _get_directive_location_for_ast_path(ancestors)
        if (
            candidate_location
            and candidate_location not in directive_locations
        ):
            self.context.report_error(
                graphql_error_from_nodes(
                    f"Directive < @{directive_name} > may not be used on "
                    f"{candidate_location}.",
                    nodes=[node],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.7.2",
                        "tag": "directives-are-in-valid-locations",
                        "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-In-Valid-Locations",
                    },
                )
            )
        return OK
