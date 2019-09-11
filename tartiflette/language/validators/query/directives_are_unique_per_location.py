from tartiflette.language.validators.query.rule import (
    June2018ReleaseValidationRule,
)
from tartiflette.language.validators.query.utils import find_nodes_by_name
from tartiflette.utils.errors import graphql_error_from_nodes


class DirectivesAreUniquePerLocation(June2018ReleaseValidationRule):
    """
    This validator validates that a directive is used only once per location

    More details @ https://graphql.github.io/graphql-spec/June2018/#sec-Directives-Are-Unique-Per-Location
    """

    RULE_NAME = "directives-are-unique-per-location"
    RULE_LINK = "https://graphql.github.io/graphql-spec/June2018/#sec-Directives-Are-Unique-Per-Location"
    RULE_NUMBER = "5.7.3"

    def validate(self, directives, path, **_):
        errors = []
        already_tested = []

        for directive in directives:
            if directive.name.value in already_tested:
                continue

            with_same_name = find_nodes_by_name(
                directives, directive.name.value
            )
            if len(with_same_name) > 1:
                already_tested.append(directive.name.value)
                errors.append(
                    graphql_error_from_nodes(
                        message=f"Can't have multiple directives named < {directive.name.value} > in the same location.",
                        path=path,
                        nodes=with_same_name,
                        extensions=self._extensions,
                    )
                )

        return errors
