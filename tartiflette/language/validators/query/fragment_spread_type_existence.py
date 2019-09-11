from tartiflette.language.validators.query.rule import (
    June2018ReleaseValidationRule,
)
from tartiflette.utils.errors import graphql_error_from_nodes


class FragmentSpreadTypeExistence(June2018ReleaseValidationRule):
    """
    This validator validates that the type of the typeCondition of a fragment
    or inline spread is define in the schema

    More details @ https://graphql.github.io/graphql-spec/June2018/#sec-Fragment-Spread-Type-Existence
    """

    RULE_NAME = "fragment-spread-type-existence"
    RULE_LINK = "https://graphql.github.io/graphql-spec/June2018/#sec-Fragment-Spread-Type-Existence"
    RULE_NUMBER = "5.5.1.2"

    def validate(self, path, schema, fragment, **__):
        errors = []

        if fragment.type_condition and not schema.has_type(
            fragment.type_condition.name.value
        ):
            errors.append(
                graphql_error_from_nodes(
                    message=f"Unknown type {fragment.type_condition.name.value}.",
                    nodes=fragment,
                    path=path,
                    extensions=self._extensions,
                )
            )

        return errors
