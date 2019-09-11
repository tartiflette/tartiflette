from tartiflette.language.utils import get_wrapped_named_type
from tartiflette.language.validators.query.rule import (
    June2018ReleaseValidationRule,
)
from tartiflette.types.type import GraphQLInputType
from tartiflette.utils.errors import graphql_error_from_nodes


class VariablesAreInputTypes(June2018ReleaseValidationRule):
    """
    This validator validate that variable type is one of [Scalar, Enum, InputType]

    More details @ https://graphql.github.io/graphql-spec/June2018/#sec-Variables-Are-Input-Types
    """

    RULE_NAME = "variables-are-input-types"
    RULE_LINK = "https://graphql.github.io/graphql-spec/June2018/#sec-Variables-Are-Input-Types"
    RULE_NUMBER = "5.8.2"

    def validate(self, variable, path, schema, **__):
        var_type = get_wrapped_named_type(variable.type)

        if schema.has_type(var_type.name.value) and not isinstance(
            schema.find_type(var_type.name.value), GraphQLInputType
        ):
            return [
                graphql_error_from_nodes(
                    message=f"Variable {variable.variable.name.value} cannot be non-input type {var_type.name.value}.",
                    path=path,
                    nodes=variable,
                    extensions=self._extensions,
                )
            ]

        return []
