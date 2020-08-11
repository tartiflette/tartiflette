from typing import List, Optional, Union

from tartiflette.language.visitor.constants import SKIP
from tartiflette.utils.errors import graphql_error_from_nodes
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("UniqueOperationTypesRule",)


class UniqueOperationTypesRule(ASTValidationRule):
    """
    A GraphQL document is only valid if it has only one type per
    operation.
    """

    def __init__(self, context: "ASTValidationContext") -> None:
        """
        :param context: context forwarded to the validation rule
        :type context: ASTValidationContext
        """
        super().__init__(context)
        self._known_operation_types = {}

    def _check_operation_type_uniqueness(
        self,
        node: ["SchemaDefinitionNode", "SchemaExtensionNode",],
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> SKIP:
        """
        Check that defined operation has been already defined.
        :param node: the current node being visiting
        :param key: the index/key to this node from the parent node/list
        :param parent: the parent immediately above this node
        :param path: the path to get to this node from the root node
        :param ancestors: nodes and list visited before reaching parent node
        :type node: [
            "SchemaDefinitionNode",
            "SchemaExtensionNode",
        ]
        :type key: Optional[Union[int, str]]
        :type parent: Optional[Union[Node, List[Node]]]
        :type path: List[Union[int, str]]
        :type ancestors: List[Union[Node, List[Node]]]
        :return: the SKIP visitor constant
        :rtype: SKIP
        """
        # pylint: disable=unused-argument
        if node.operation_type_definitions:
            for operation_type_definition in node.operation_type_definitions:
                operation_type = operation_type_definition.operation_type
                known_operation_type = self._known_operation_types.get(
                    operation_type
                )
                if known_operation_type:
                    self.context.report_error(
                        graphql_error_from_nodes(
                            f"There can be only one < {operation_type} > type "
                            "in schema.",
                            nodes=[
                                known_operation_type,
                                operation_type_definition,
                            ],
                        )
                    )
                else:
                    self._known_operation_types[
                        operation_type
                    ] = operation_type_definition
        return SKIP

    enter_SchemaDefinition = _check_operation_type_uniqueness
    enter_SchemaExtension = _check_operation_type_uniqueness
