from tartiflette.language.ast import DirectiveNode
from tartiflette.language.validators.query.rule import (
    June2018ReleaseValidationRule,
)
from tartiflette.language.validators.query.utils import (
    find_field,
    find_nodes_by_name,
)
from tartiflette.types.non_null import GraphQLNonNull
from tartiflette.utils.errors import graphql_error_from_nodes


class RequiredArguments(June2018ReleaseValidationRule):
    """
    This validator validates that field or directive arguments
    defined as non-null whithout a default value, are present in the query

    More details @ https://graphql.github.io/graphql-spec/June2018/#sec-Required-Arguments
    """

    RULE_NAME = "required-arguments"
    RULE_LINK = "https://graphql.github.io/graphql-spec/June2018/#sec-Required-Arguments"
    RULE_NUMBER = "5.4.2.1"

    def _validate_arguments(
        self, parent_node, schema_definition, path, message_suffix
    ):
        errors = []
        for schema_arg in schema_definition.arguments.values():
            if (
                isinstance(schema_arg.graphql_type, GraphQLNonNull)
                and schema_arg.default_value is None
                and not find_nodes_by_name(
                    parent_node.arguments, schema_arg.name
                )
            ):
                errors.append(
                    graphql_error_from_nodes(
                        message=f"Missing mandatory argument < {schema_arg.name} > {message_suffix}",
                        nodes=parent_node,
                        path=path,
                        extensions=self._extensions,
                    )
                )
        return errors

    def _validate_directive(self, path, schema, directive_node):
        if not schema.has_directive(directive_node.name.value):
            return []  # Handled by another validator

        schema_directive = schema.find_directive(directive_node.name.value)
        return self._validate_arguments(
            directive_node,
            schema_directive,
            path,
            f"in directive < @{directive_node.name.value} >.",
        )

    def _validate_field(self, path, schema, field, parent_type_name):
        schema_field = find_field(parent_type_name, field.name.value, schema)

        if schema_field is None:
            return []  # Handled by anoter validator

        return self._validate_arguments(
            field,
            schema_field,
            path,
            f"in field < {parent_type_name}.{field.name.value} >.",
        )

    def validate(self, path, schema, node, parent_type_name=None, **__):
        if isinstance(node, DirectiveNode):
            return self._validate_directive(path, schema, node)
        return self._validate_field(path, schema, node, parent_type_name)
