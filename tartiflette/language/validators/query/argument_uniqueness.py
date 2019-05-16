from tartiflette.language.validators.query.rule import (
    June2018ReleaseValidationRule,
)
from tartiflette.language.validators.query.utils import find_nodes_by_name
from tartiflette.utils.errors import graphql_error_from_nodes


class ArgumentUniqueness(June2018ReleaseValidationRule):
    """
    This validator validates, for a given directive or field arguments list,
    that arguments are provided only once.

    More details @ https://graphql.github.io/graphql-spec/June2018/#sec-Argument-Uniqueness
    """

    RULE_NAME = "argument-uniqueness"
    RULE_LINK = "https://graphql.github.io/graphql-spec/June2018/#sec-Argument-Uniqueness"
    RULE_NUMBER = "5.4.2"

    def validate(self, arguments, path, **__):
        errors = []
        already_tested = []

        for argument in arguments:
            if argument.name.value in already_tested:
                continue

            with_same_name = find_nodes_by_name(arguments, argument.name.value)
            if len(with_same_name) > 1:
                already_tested.append(argument.name.value)
                errors.append(
                    graphql_error_from_nodes(
                        message=f"Can't have multiple arguments named < {argument.name.value} >.",
                        path=path,
                        nodes=with_same_name,
                        extensions=self._extensions,
                    )
                )

        return errors
