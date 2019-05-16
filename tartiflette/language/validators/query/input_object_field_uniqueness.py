from tartiflette.language.validators.query.rule import (
    June2018ReleaseValidationRule,
)
from tartiflette.language.validators.query.utils import find_nodes_by_name
from tartiflette.utils.errors import graphql_error_from_nodes


class InputObjectFieldUniqueness(June2018ReleaseValidationRule):
    """
    This validator validates that Field in an input object are Unique

    > No field share the same name.

    More details @ https://graphql.github.io/graphql-spec/June2018/#sec-Input-Object-Field-Uniqueness
    """

    RULE_NAME = "input-object-field-uniqueness"
    RULE_LINK = "https://graphql.github.io/graphql-spec/June2018/#sec-Input-Object-Field-Uniqueness"
    RULE_NUMBER = "5.6.3"

    def validate(self, path, input_fields, **__):
        errors = []
        already_tested = []

        for ifield in input_fields:
            if ifield.name.value in already_tested:
                continue

            with_same_name = find_nodes_by_name(
                input_fields, ifield.name.value
            )
            if len(with_same_name) > 1:
                already_tested.append(ifield.name.value)
                errors.append(
                    graphql_error_from_nodes(
                        message=f"Can't have multiple Input Field named < {ifield.name.value} >.",
                        path=path,
                        nodes=with_same_name,
                        extensions=self._extensions,
                    )
                )

        return errors
