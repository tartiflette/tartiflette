from tartiflette.language.validators.query.rule import (
    June2018ReleaseValidationRule,
)
from tartiflette.language.validators.query.utils import find_nodes_by_name
from tartiflette.utils.errors import graphql_error_from_nodes


class FragmentNameUniqueness(June2018ReleaseValidationRule):
    """
    This validator validates that a Fragment name is only used once which
    means that you can't have 2 Fragments defined with the same name.

    More details @ https://graphql.github.io/graphql-spec/June2018/#sec-Fragment-Name-Uniqueness
    """

    RULE_NAME = "fragment-name-uniqueness"
    RULE_LINK = "https://graphql.github.io/graphql-spec/June2018/#sec-Fragment-Name-Uniqueness"
    RULE_NUMBER = "5.5.1.1"

    def validate(self, path, fragments, **__):
        errors = []
        already_tested = []

        for fragment in fragments:
            if fragment.name.value in already_tested:
                continue

            with_same_name = find_nodes_by_name(fragments, fragment.name.value)
            if len(with_same_name) > 1:
                already_tested.append(fragment.name.value)
                errors.append(
                    graphql_error_from_nodes(
                        message=f"Can't have multiple fragments named < {fragment.name.value} >.",
                        path=path,
                        nodes=with_same_name,
                        extensions=self._extensions,
                    )
                )

        return errors
