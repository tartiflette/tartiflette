from tartiflette.language.validators.query.rule import (
    June2018ReleaseValidationRule,
)
from tartiflette.utils.errors import graphql_error_from_nodes


class LoneAnonymousOperation(June2018ReleaseValidationRule):
    """
    This validator validates that an Anonymous operation
    is the only defined operation of the document

    More details @ https://graphql.github.io/graphql-spec/June2018/#sec-Lone-Anonymous-Operation
    """

    RULE_NAME = "lone-anonymous-operation"
    RULE_LINK = "https://graphql.github.io/graphql-spec/June2018/#sec-Lone-Anonymous-Operation"
    RULE_NUMBER = "5.2.2.1"

    def validate(self, path, operations, **__):
        bad_nodes = []
        errors = []

        if len(operations) > 1:
            for operation in operations:
                if operation.name is None:
                    bad_nodes.append(operation)

        if bad_nodes:
            errors.append(
                graphql_error_from_nodes(
                    message="Anonymous operation must be the only defined operation.",
                    path=path,
                    nodes=bad_nodes,
                    extensions=self._extensions,
                )
            )

        return errors
