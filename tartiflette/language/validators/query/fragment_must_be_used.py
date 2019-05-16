from tartiflette.language.validators.query.rule import (
    June2018ReleaseValidationRule,
)
from tartiflette.language.validators.query.utils import find_nodes_by_name
from tartiflette.utils.errors import graphql_error_from_nodes


class FragmentMustBeUsed(June2018ReleaseValidationRule):
    """
    This validator validates that a defined fragment is at least spread once in the document.

    Mode details @ https://graphql.github.io/graphql-spec/June2018/#sec-Fragments-Must-Be-Used
    """

    RULE_NAME = "fragment-must-be-used"
    RULE_LINK = "https://graphql.github.io/graphql-spec/June2018/#sec-Fragments-Must-Be-Used"
    RULE_NUMBER = "5.5.1.4"

    def validate(self, path, fragments, fragment_spreads=None, **__):
        errors = []

        if not fragment_spreads:
            fragment_spreads = []

        for fragment in fragments:
            if not find_nodes_by_name(fragment_spreads, fragment.name.value):
                errors.append(
                    graphql_error_from_nodes(
                        message=f"Fragment < {fragment.name.value} > is never used.",
                        nodes=fragment,
                        path=path,
                        extensions=self._extensions,
                    )
                )

        return errors
