from tartiflette.language.validators.query.rule import (
    June2018ReleaseValidationRule,
)
from tartiflette.utils.errors import graphql_error_from_nodes


class DirectivesAreDefined(June2018ReleaseValidationRule):
    """
    This validator validate that a directive is defined in the schema

    More details @ https://graphql.github.io/graphql-spec/June2018/#sec-Directives-Are-Defined
    """

    RULE_NAME = "directives-are-defined"
    RULE_LINK = "https://graphql.github.io/graphql-spec/June2018/#sec-Directives-Are-Defined"
    RULE_NUMBER = "5.7.1"

    def validate(self, directive, schema, path, **_):
        if not schema.has_directive(directive.name.value):
            return [
                graphql_error_from_nodes(
                    message=f"Unknow Directive < @{directive.name.value} >.",
                    nodes=directive,
                    path=path,
                    extensions=self._extensions,
                )
            ]

        return []
