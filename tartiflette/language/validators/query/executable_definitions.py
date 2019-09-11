from tartiflette.language.ast.base import ExecutableDefinitionNode
from tartiflette.language.validators.query.rule import (
    June2018ReleaseValidationRule,
)
from tartiflette.utils.errors import graphql_error_from_nodes


class ExecutableDefinition(June2018ReleaseValidationRule):
    """
    This validator validates that a document only contains executable definitions

    I.E. no schema type system in a Query.

    More details @ https://graphql.github.io/graphql-spec/June2018/#sec-Executable-Definitions
    """

    RULE_NAME = "executable-definitions"
    RULE_LINK = "https://graphql.github.io/graphql-spec/June2018/#sec-Executable-Definitions"
    RULE_NUMBER = "5.1.1"

    def validate(self, definitions, path, **__):
        bad_nodes = [
            x
            for x in definitions
            if not isinstance(x, ExecutableDefinitionNode)
        ]
        if bad_nodes:
            return [
                graphql_error_from_nodes(
                    message="Theses definitions are not executable.",
                    path=path,
                    nodes=bad_nodes,
                    extensions=self._extensions,
                )
            ]

        return []
