from tartiflette.language.ast import InlineFragmentNode
from tartiflette.language.validators.query.rule import (
    June2018ReleaseValidationRule,
)
from tartiflette.types.type import GraphQLCompositeType
from tartiflette.utils.errors import graphql_error_from_nodes


class FragmentsOnCompositeTypes(June2018ReleaseValidationRule):
    """
    This validator validates that the type of the typeCondition for a
    Fragment or an inlinespread is a valid composite type. (Object, Interface, Union)

    More details @ https://graphql.github.io/graphql-spec/June2018/#sec-Fragments-On-Composite-Types
    """

    RULE_NAME = "fragments-on-composite-types"
    RULE_LINK = "https://graphql.github.io/graphql-spec/June2018/#sec-Fragments-On-Composite-Types"
    RULE_NUMBER = "5.5.1.3"

    def validate(self, path, schema, fragment, **__):
        errors = []
        if (
            fragment.type_condition
            and schema.has_type(fragment.type_condition.name.value)
            and not isinstance(
                schema.find_type(fragment.type_condition.name.value),
                GraphQLCompositeType,
            )
        ):
            message = (
                f"Fragment {fragment.name.value}"
                if not isinstance(fragment, InlineFragmentNode)
                else f"Inline Fragment"
            )
            errors.append(
                graphql_error_from_nodes(
                    message=f"{message} cannot condition on non composite type {fragment.type_condition.name.value}.",
                    nodes=fragment,
                    path=path,
                    extensions=self._extensions,
                )
            )

        return errors
