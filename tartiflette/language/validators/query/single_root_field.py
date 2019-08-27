from tartiflette.language.ast import FragmentSpreadNode, InlineFragmentNode
from tartiflette.language.validators.query.rule import (
    June2018ReleaseValidationRule,
)
from tartiflette.utils.errors import graphql_error_from_nodes


def _find_fragment(fragments, name):
    for frag in fragments:
        if frag.name.value == name:
            return frag

    return None


class SingleRootField(June2018ReleaseValidationRule):
    """
    This validator validates that Subscription Operation does only contains one root field after complete fragment spreading.

    More details @ https://graphql.github.io/graphql-spec/June2018/#sec-Single-root-field
    """

    RULE_NAME = "single-root-field"
    RULE_LINK = "https://graphql.github.io/graphql-spec/June2018/#sec-Single-root-field"
    RULE_NUMBER = "5.2.3.1"

    def _validate_selection_set(
        self, operation, selection_set, fragments, path
    ):
        nb_selections = len(selection_set.selections)
        if nb_selections > 1:
            message = f"{f'Subcription {operation.name.value}' if operation.name else 'Anonymous Subscription'}"
            return [
                graphql_error_from_nodes(
                    message=f"{message} must select only one top level field.",
                    nodes=[operation, selection_set],
                    path=path,
                    extensions=self._extensions,
                )
            ]

        if nb_selections == 1:
            selected = selection_set.selections[0]
            if isinstance(selected, FragmentSpreadNode):
                frag = _find_fragment(fragments, selected.name.value)

                if not frag:
                    return []  # Handled by another validator

                return self._validate_selection_set(
                    operation, frag.selection_set, fragments, path
                )

            if isinstance(selected, InlineFragmentNode):
                return self._validate_selection_set(
                    operation, selected.selection_set, fragments, path
                )

        return []

    def validate(self, path, definitions, **__):
        for operation in definitions["OperationDefinition"]:
            if operation.operation_type == "subscription":
                return self._validate_selection_set(
                    operation,
                    operation.selection_set,
                    definitions["FragmentDefinition"],
                    path,
                )

        return []
