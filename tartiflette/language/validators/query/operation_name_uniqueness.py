from tartiflette.language.validators.query.rule import (
    June2018ReleaseValidationRule,
)
from tartiflette.language.validators.query.utils import find_nodes_by_name
from tartiflette.utils.errors import graphql_error_from_nodes


class OperationNameUniqueness(June2018ReleaseValidationRule):
    """
    This validator validates that no operations are defined with the same name.

    More details @ https://graphql.github.io/graphql-spec/June2018/#sec-Operation-Name-Uniqueness
    """

    RULE_NAME = "operation-name-uniqueness"
    RULE_LINK = "https://graphql.github.io/graphql-spec/June2018/#sec-Operation-Name-Uniqueness"
    RULE_NUMBER = "5.2.1.1"

    def validate(self, path, operations, **__):
        errors = []
        already_tested = []

        for operation in operations:
            if not operation.name or operation.name.value in already_tested:
                continue

            with_same_name = find_nodes_by_name(
                operations, operation.name.value
            )
            if len(with_same_name) > 1:
                already_tested.append(operation.name.value)
                errors.append(
                    graphql_error_from_nodes(
                        message=f"Can't have multiple operations named < {operation.name.value} >.",
                        path=path,
                        nodes=with_same_name,
                        extensions=self._extensions,
                    )
                )

        return errors
