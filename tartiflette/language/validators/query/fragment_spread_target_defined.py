from tartiflette.language.validators.query.rule import (
    June2018ReleaseValidationRule,
)
from tartiflette.language.validators.query.utils import find_nodes_by_name
from tartiflette.utils.errors import graphql_error_from_nodes


class FragmentSpreadTargetDefined(June2018ReleaseValidationRule):
    """
    This validator validates that a spreaded Fragment is defined in the Query Document.

    I.E. You can't spread an unknown Fragment.

    More details @ https://graphql.github.io/graphql-spec/June2018/#sec-Fragment-spread-target-defined
    """

    RULE_NAME = "fragment-spread-target-defined"
    RULE_LINK = "https://graphql.github.io/graphql-spec/June2018/#sec-Fragment-spread-target-defined"
    RULE_NUMBER = "5.5.2.1"

    def _to_errors(self, erronous_speads, path):
        return [graphql_error_from_nodes(
                    message=f"Unknown Fragment for Spread < {spread_name} >.",
                    nodes=spreads,
                    path=path,
                    extensions=self._extensions,
                ) for spread_name, spreads in erronous_speads.items()]

    def validate(self, path, fragments, fragment_spreads=None, **__):
        erronous_speads = {}

        if not fragment_spreads:
            fragment_spreads = []

        for spread in fragment_spreads:
            if not find_nodes_by_name(fragments, spread.name.value):
                erronous_speads.setdefault(spread.name.value, []).append(
                    spread
                )

        return self._to_errors(erronous_speads, path)
