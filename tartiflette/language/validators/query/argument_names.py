from tartiflette.language.ast import DirectiveNode
from tartiflette.language.validators.query.rule import (
    June2018ReleaseValidationRule,
)
from tartiflette.language.validators.query.utils import find_field
from tartiflette.utils.errors import graphql_error_from_nodes


class ArgumentNames(June2018ReleaseValidationRule):
    """
    This validator will look at all arguments of a field or a directive and
    validates that they are defined in the schema.

    More details @ https://graphql.github.io/graphql-spec/June2018/#sec-Argument-Names
    """

    RULE_NAME = "argument-names"
    RULE_LINK = (
        "https://graphql.github.io/graphql-spec/June2018/#sec-Argument-Names"
    )
    RULE_NUMBER = "5.4.1"

    def _validate_directive_arguments(self, query_node, path, schema):
        errors = []
        if not schema.has_directive(query_node.name.value):
            return []  # Handled by another Validator

        schema_directive = schema.find_directive(query_node.name.value)

        for argument in query_node.arguments:
            if argument.name.value not in schema_directive.arguments:
                errors.append(
                    graphql_error_from_nodes(
                        message=f"Provided Argument < {argument.name.value} > doesn't exist on directive < @{schema_directive.name} >.",
                        nodes=argument,
                        path=path,
                        extensions=self._extensions,
                    )
                )

        return errors

    def _validate_field_arguments(
        self, query_field, path, schema, parent_type_name
    ):
        errors = []

        schema_field = find_field(
            parent_type_name, query_field.name.value, schema
        )

        if not schema_field:
            return []  # Handled somewhere else.

        for query_field_argument in query_field.arguments:
            if query_field_argument.name.value not in schema_field.arguments:
                errors.append(
                    graphql_error_from_nodes(
                        message=f"Provided Argument < {query_field_argument.name.value} > doesn't exist on field < {parent_type_name}.{schema_field.name} >.",
                        nodes=query_field_argument,
                        path=path,
                        extensions=self._extensions,
                    )
                )

        return errors

    def validate(self, node, path, schema, parent_type_name=None, **__):
        if isinstance(node, DirectiveNode):
            return self._validate_directive_arguments(node, path, schema)
        return self._validate_field_arguments(
            node, path, schema, parent_type_name
        )
