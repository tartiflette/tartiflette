from collections import defaultdict
from functools import partial
from typing import Dict, List, Optional, Union

from tartiflette.language.ast import SchemaDefinitionNode, SchemaExtensionNode
from tartiflette.language.ast.base import TypeDefinitionNode, TypeExtensionNode
from tartiflette.utils.errors import (
    graphql_error_from_nodes as raw_graphql_error_from_nodes,
)
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("UniqueDirectivesPerLocationRule",)


graphql_error_from_nodes = partial(
    raw_graphql_error_from_nodes,
    extensions={
        "spec": "June 2018",
        "rule": "5.7.3",
        "tag": "directives-are-unique-per-location",
        "details": (
            "https://spec.graphql.org/June2018/#sec-Directives-Are-Unique-Per-Location"
        ),
    },
)


class UniqueDirectivesPerLocationRule(ASTValidationRule):
    """
    A GraphQL document is only valid if directives at a given location
    are uniquely named.
    """

    def __init__(self, context: "ASTValidationContext") -> None:
        """
        :param context: context forwarded to the validation rule
        :type context: ASTValidationContext
        """
        super().__init__(context)
        self._schema_directives: Dict[str, "DirectiveNode"] = {}
        self._type_directives_map: Dict[
            str, Dict[str, "DirectiveNode"]
        ] = defaultdict(dict)

    def enter(
        self,
        node: "Node",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> None:
        """
        Check that directives at a given location are uniquely named.
        :param node: the current node being visiting
        :param key: the index/key to this node from the parent node/list
        :param parent: the parent immediately above this node
        :param path: the path to get to this node from the root node
        :param ancestors: nodes and list visited before reaching parent node
        :type node: "Node""
        :type key: Optional[Union[int, str]]
        :type parent: Optional[Union[Node, List[Node]]]
        :type path: List[Union[int, str]]
        :type ancestors: List[Union[Node, List[Node]]]
        """
        # pylint: disable=unused-argument
        # Many different AST nodes may contain directives. Rather than listing
        # them all, just listen for entering any node, and check to see if it
        # defines any directives.
        directives = getattr(node, "directives", None)
        if directives:
            if isinstance(node, (SchemaDefinitionNode, SchemaExtensionNode)):
                known_directives = self._schema_directives
            elif isinstance(node, (TypeDefinitionNode, TypeExtensionNode)):
                known_directives = self._type_directives_map[node.name.value]
            else:
                known_directives = {}

            for directive in directives:
                directive_name = directive.name.value
                known_directive = known_directives.get(directive_name)
                if known_directive:
                    self.context.report_error(
                        graphql_error_from_nodes(
                            f"The directive < @{directive_name} > can only be "
                            "used once at this location.",
                            nodes=[known_directive, directive],
                        )
                    )
                else:
                    known_directives[directive_name] = directive
