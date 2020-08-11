from typing import Dict, List, Optional, Union

from tartiflette.language.ast import ObjectTypeDefinitionNode
from tartiflette.language.ast.base import TypeDefinitionNode
from tartiflette.language.visitor.constants import SKIP
from tartiflette.utils.errors import graphql_error_from_nodes
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("ValidOperationTypesRule",)

_QUERY_OPERATION_TYPE = "query"
_MUTATION_OPERATION_TYPE = "mutation"
_SUBSCRIPTION_OPERATION_TYPE = "subscription"
_DEFAULT_ROOT_OPERATION_NAMES_MAP: Dict[str, str] = {
    _QUERY_OPERATION_TYPE: "Query",
    _MUTATION_OPERATION_TYPE: "Mutation",
    _SUBSCRIPTION_OPERATION_TYPE: "Subscription",
}


class ValidOperationTypesRule(ASTValidationRule):
    """
    Validate that operation types are valid.
    """

    def __init__(self, context: "ASTValidationContext") -> None:
        """
        :param context: context forwarded to the validation rule
        :type context: ASTValidationContext
        """
        super().__init__(context)
        self._operation_type_nodes: Dict[str, "OperationDefinitionNode"] = {}
        self._known_types: Dict[str, "TypeDefinitionNode"] = {
            definition_node.name.value: definition_node
            for definition_node in context.document_node.definitions
            if isinstance(definition_node, TypeDefinitionNode)
        }

    def _check_root_operation_validness(
        self, operation_type: str, is_required: bool = False
    ) -> None:
        """
        Check that the operation type is valid.
        :param operation_type: the operation type to check
        :param is_required: whether or not the operation should be defined
        :type operation_type: str
        :type is_required: bool
        """
        defined_operation_definition_node = self._operation_type_nodes.get(
            operation_type
        )
        operation_name = (
            defined_operation_definition_node.type.name.value
            if defined_operation_definition_node
            else _DEFAULT_ROOT_OPERATION_NAMES_MAP[operation_type]
        )
        known_type = self._known_types.get(operation_name)

        if (
            not is_required
            and not defined_operation_definition_node
            and not known_type
        ):
            return

        default_operation_type_name = _DEFAULT_ROOT_OPERATION_NAMES_MAP[
            operation_type
        ]

        if not known_type and not defined_operation_definition_node:
            self.context.report_error(
                graphql_error_from_nodes(
                    f"{default_operation_type_name} root type must be "
                    "provided.",
                    nodes=[self.context.document_node],
                )
            )
        elif not isinstance(known_type, ObjectTypeDefinitionNode):
            self.context.report_error(
                graphql_error_from_nodes(
                    f"{default_operation_type_name} root type must be Object "
                    "type.",
                    nodes=[defined_operation_definition_node.type],
                )
            )

    def enter_OperationTypeDefinition(  # pylint: disable=invalid-name
        self,
        node: "OperationTypeDefinitionNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> SKIP:
        """
        Collect the OperationTypeDefinitionNode.
        :param node: the current node being visiting
        :param key: the index/key to this node from the parent node/list
        :param parent: the parent immediately above this node
        :param path: the path to get to this node from the root node
        :param ancestors: nodes and list visited before reaching parent node
        :type node: OperationTypeDefinitionNode
        :type key: Optional[Union[int, str]]
        :type parent: Optional[Union[Node, List[Node]]]
        :type path: List[Union[int, str]]
        :type ancestors: List[Union[Node, List[Node]]]
        :return: the SKIP visitor constant
        :rtype: SKIP
        """
        # pylint: disable=unused-argument
        self._operation_type_nodes[node.operation_type] = node
        return SKIP

    def leave_Document(  # pylint: disable=invalid-name
        self,
        node: "DocumentNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> None:
        """
        Check that operations are valid.
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
        self._check_root_operation_validness(
            _QUERY_OPERATION_TYPE, is_required=True
        )
        self._check_root_operation_validness(_MUTATION_OPERATION_TYPE)
        self._check_root_operation_validness(_SUBSCRIPTION_OPERATION_TYPE)
