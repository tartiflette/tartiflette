from tartiflette.language.validators.query.rule import (
    June2018ReleaseValidationRule,
)
from tartiflette.language.validators.query.utils import find_field_reduced_type
from tartiflette.utils.errors import graphql_error_from_nodes


class FieldSelectionsOnObjectsInterfacesAndUnionsTypes(
    June2018ReleaseValidationRule
):
    """
    This validator validates that a selected field exists
    (is defined by the schema) in the context of it's parent.

    More details @ https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types
    """

    RULE_NAME = "field-selections-on-objects-interfaces-and-unions-types"
    RULE_LINK = "https://graphql.github.io/graphql-spec/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types"
    RULE_NUMBER = "5.3.1"

    def validate(self, path, schema, field, parent_type_name, **__):
        graphql_type = find_field_reduced_type(
            parent_type_name, field.name.value, schema
        )

        if field.name.value.startswith("__"):
            return []

        if graphql_type is None:
            return [
                graphql_error_from_nodes(
                    message=f"Field {field.name.value} doesn't exist on {parent_type_name or 'Root'}",
                    nodes=field,
                    path=path,
                    extensions=self._extensions,
                )
            ]

        return []
