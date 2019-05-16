from tartiflette.language.ast import FragmentSpreadNode
from tartiflette.language.validators.query.rule import (
    June2018ReleaseValidationRule,
)
from tartiflette.language.validators.query.utils import find_nodes_by_name
from tartiflette.utils.errors import graphql_error_from_nodes


class CycleException(Exception):
    def __init__(self, fragments, extensions):
        super().__init__()
        self.tartiflette_errors = [
            graphql_error_from_nodes(
                message="Fragment Cylcle Detected",
                path=None,
                nodes=fragments,
                extensions=extensions,
            )
        ]


class FragmentSpreadsMustNotFormCycles(June2018ReleaseValidationRule):
    """
    This validator validates that a Fragment doesnt spread itself.
    Either directly or through any other spreaded fragment.

    > I.E. : `A -> A` or `A -> B -> C -> A` aren't allowed

    More details @ https://graphql.github.io/graphql-spec/June2018/#sec-Fragment-spreads-must-not-form-cycles
    """

    RULE_NAME = "fragment-spreads-must-not-form-cycles"
    RULE_LINK = "https://graphql.github.io/graphql-spec/June2018/#sec-Fragment-spreads-must-not-form-cycles"
    RULE_NUMBER = "5.5.2.2"

    def _validate_fragment(self, fragments, fragment, spreaded):
        for selected in fragment.selection_set.selections:
            if isinstance(selected, FragmentSpreadNode):
                if selected.name.value not in spreaded:
                    spreaded.append(selected.name.value)

                    fragment = find_nodes_by_name(
                        fragments, selected.name.value
                    )
                    if not fragment:
                        continue  # Handled by another validator
                    fragment = fragment[0]

                    self._validate_fragment(fragments, fragment, spreaded)
                else:
                    raise CycleException(fragments, self._extensions)
        return

    def validate(self, fragments, **_):
        for fragment in fragments:
            try:
                self._validate_fragment(fragments, fragment, [])
            except CycleException as e:
                return e.tartiflette_errors

        return []
