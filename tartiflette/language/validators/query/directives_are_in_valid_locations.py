from tartiflette.language.ast import (
    FieldNode,
    FragmentDefinitionNode,
    FragmentSpreadNode,
    InlineFragmentNode,
    OperationDefinitionNode,
)
from tartiflette.language.validators.query.rule import (
    June2018ReleaseValidationRule,
)
from tartiflette.utils.errors import graphql_error_from_nodes

_NODE_TO_DIRECTIVE_LOCATION_MAP = {
    FieldNode: "FIELD",
    FragmentSpreadNode: "FRAGMENT_SPREAD",
    InlineFragmentNode: "INLINE_FRAGMENT",
    FragmentDefinitionNode: "FRAGMENT_DEFINITION",
    "query": "QUERY",
    "mutation": "MUTATION",
    "subscription": "SUBSCRIPTION",
}


class DirectivesAreInValidLocations(June2018ReleaseValidationRule):
    """
    This validator validates that directive are used in a location
    that is valid for the directive.

    More details @ https://graphql.github.io/graphql-spec/June2018/#sec-Directives-Are-In-Valid-Locations
    """

    RULE_NAME = "directives-are-in-valid-locations"
    RULE_LINK = "https://graphql.github.io/graphql-spec/June2018/#sec-Directives-Are-In-Valid-Locations"
    RULE_NUMBER = "5.7.2"

    def validate(self, node, path, schema, **_):
        errors = []

        node_type = type(node)
        if isinstance(node, OperationDefinitionNode):
            node_type = node.operation_type.lower()

        for directive in node.directives:
            if not schema.has_directive(directive.name.value):
                continue  # Handled by another validator (5.7.1)

            schema_directive = schema.find_directive(directive.name.value)
            if (
                _NODE_TO_DIRECTIVE_LOCATION_MAP[node_type]
                not in schema_directive.locations
            ):
                errors.append(
                    graphql_error_from_nodes(
                        message=f"Directive < @{directive.name.value} > is not used in a valid location.",
                        nodes=[node, directive],
                        path=path,
                        extensions=self._extensions,
                    )
                )

        return errors
