from functools import partial
from typing import List, Optional, Union

from tartiflette.language.ast import (
    FragmentDefinitionNode,
    OperationDefinitionNode,
    SchemaDefinitionNode,
    SchemaExtensionNode,
)
from tartiflette.language.visitor.constants import SKIP
from tartiflette.utils.errors import (
    graphql_error_from_nodes as raw_graphql_error_from_nodes,
)
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("ExecutableDefinitionsRule",)


graphql_error_from_nodes = partial(
    raw_graphql_error_from_nodes,
    extensions={
        "spec": "June 2018",
        "rule": "5.1.1",
        "tag": "executable-definitions",
        "details": (
            "https://spec.graphql.org/June2018/#sec-Executable-Definitions"
        ),
    },
)


class ExecutableDefinitionsRule(ASTValidationRule):
    """
    A GraphQL document is only valid for execution if all definitions
    are either operation or fragment definitions.
    """

    def enter_Document(  # pylint: disable=invalid-name
        self,
        node: "DocumentNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> SKIP:
        """
        Check that all definitions are operation or fragment definitions.
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
        :return: the SKIP visitor constant
        :rtype: SKIP
        """
        # pylint: disable=unused-argument
        for definition in node.definitions:
            if not isinstance(
                definition, (OperationDefinitionNode, FragmentDefinitionNode)
            ):
                definition_name = (
                    "schema"
                    if isinstance(
                        definition, (SchemaDefinitionNode, SchemaExtensionNode)
                    )
                    else definition.name.value
                )
                self.context.report_error(
                    graphql_error_from_nodes(
                        f"The < {definition_name} > definition is not "
                        "executable.",
                        nodes=[definition],
                    )
                )
        return SKIP
