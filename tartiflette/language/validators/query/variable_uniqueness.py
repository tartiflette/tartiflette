from tartiflette.language.validators.query.rule import (
    June2018ReleaseValidationRule,
)
from tartiflette.language.validators.query.utils import find_nodes_by_name
from tartiflette.utils.errors import graphql_error_from_nodes


class VariableUniqueness(June2018ReleaseValidationRule):
    """
    This validator validates that variable are unique a given variable definition list.

    > No variables with the same name in an operation context.

    More details @ https://graphql.github.io/graphql-spec/June2018/#sec-Variable-Uniqueness
    """

    RULE_NAME = "variable-uniqueness"
    RULE_LINK = "https://graphql.github.io/graphql-spec/June2018/#sec-Variable-Uniqueness"
    RULE_NUMBER = "5.8.1"

    def validate(self, path, variable_definitions, **__):
        errors = []
        already_tested = []

        variables = [x.variable for x in variable_definitions]

        for variable in variables:
            if variable.name.value in already_tested:
                continue

            with_same_name = find_nodes_by_name(variables, variable.name.value)
            if len(with_same_name) > 1:
                already_tested.append(variable.name.value)
                errors.append(
                    graphql_error_from_nodes(
                        message=f"Can't have multiple variables named < {variable.name.value} >.",
                        path=path,
                        nodes=with_same_name,
                        extensions=self._extensions,
                    )
                )

        return errors
