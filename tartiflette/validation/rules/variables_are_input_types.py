from functools import partial
from typing import List, Optional, Union

from tartiflette.types.helpers.definition import is_input_type
from tartiflette.utils.errors import (
    graphql_error_from_nodes as raw_graphql_error_from_nodes,
)
from tartiflette.utils.type_from_ast import schema_type_from_ast
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("VariablesAreInputTypesRule",)


graphql_error_from_nodes = partial(
    raw_graphql_error_from_nodes,
    extensions={
        "spec": "June 2018",
        "rule": "5.8.2",
        "tag": "variables-are-input-types",
        "details": (
            "https://spec.graphql.org/June2018/#sec-Variables-Are-Input-Types"
        ),
    },
)


class VariablesAreInputTypesRule(ASTValidationRule):
    """
    A GraphQL operation is only valid if all the variables it defines
    are of input types (scalar, enum, or input object).
    """

    def enter_VariableDefinition(  # pylint: disable=invalid-name
        self,
        node: "VariableDefinitionNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> None:
        """
        Check that the variable definition is an input type.
        :param node: the current node being visiting
        :param key: the index/key to this node from the parent node/list
        :param parent: the parent immediately above this node
        :param path: the path to get to this node from the root node
        :param ancestors: nodes and list visited before reaching parent node
        :type node: VariableDefinitionNode
        :type key: Optional[Union[int, str]]
        :type parent: Optional[Union[Node, List[Node]]]
        :type path: List[Union[int, str]]
        :type ancestors: List[Union[Node, List[Node]]]
        """
        # pylint: disable=unused-argument
        gql_type = schema_type_from_ast(self.context.schema, node.type)
        if gql_type and not is_input_type(gql_type):
            variable_name = node.variable.name.value
            self.context.report_error(
                graphql_error_from_nodes(
                    f"Variable < {variable_name} > cannot be non-input type "
                    f"< {gql_type} >.",
                    nodes=node.type,
                )
            )
