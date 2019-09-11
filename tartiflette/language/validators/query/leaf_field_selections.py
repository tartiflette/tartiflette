from tartiflette.language.validators.query.rule import (
    June2018ReleaseValidationRule,
)
from tartiflette.language.validators.query.utils import find_field_reduced_type
from tartiflette.types.type import GraphQLCompositeType
from tartiflette.utils.errors import graphql_error_from_nodes


class LeafFieldSelections(June2018ReleaseValidationRule):
    """
    This validator validates that selection set are only in used
    in fields that are of composite type. (Object, Interface, Union)

    More details @ https://graphql.github.io/graphql-spec/June2018/#sec-Leaf-Field-Selections
    """

    RULE_NAME = "leaf-field-selections"
    RULE_LINK = "https://graphql.github.io/graphql-spec/June2018/#sec-Leaf-Field-Selections"
    RULE_NUMBER = "5.3.3"

    def validate(self, path, schema, field, parent_type_name, **__):
        rtype = find_field_reduced_type(
            parent_type_name, field.name.value, schema
        )

        if not rtype:
            return (
                []
            )  # Handled by field_selections_on_objects_interfaces_and_unions_types rule
            # TODO maybe think about rule order/dependencies

        is_gql_composite_type = isinstance(rtype, GraphQLCompositeType)

        if not field.selection_set and is_gql_composite_type:
            return [
                graphql_error_from_nodes(
                    message=f"Field {field.name.value} of type {rtype.name} must have a selection of subfields.",
                    nodes=field,
                    path=path,
                    extensions=self._extensions,
                )
            ]

        if field.selection_set and not is_gql_composite_type:
            return [
                graphql_error_from_nodes(
                    message=f"Field {field.name.value} must not have a selection since type {rtype.name} has no subfields.",
                    nodes=field,
                    path=path,
                    extensions=self._extensions,
                )
            ]

        return []
