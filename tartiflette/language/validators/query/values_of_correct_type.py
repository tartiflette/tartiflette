from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import (
    DirectiveNode,
    ListValueNode,
    NullValueNode,
    ObjectValueNode,
    VariableNode,
)
from tartiflette.language.validators.query.rule import (
    June2018ReleaseValidationRule,
)
from tartiflette.language.validators.query.utils import find_field
from tartiflette.types.enum import GraphQLEnumType
from tartiflette.types.helpers.reduce_type import reduce_type
from tartiflette.types.input_object import GraphQLInputObjectType
from tartiflette.types.list import GraphQLList
from tartiflette.types.non_null import GraphQLNonNull
from tartiflette.types.scalar import GraphQLScalarType
from tartiflette.utils.errors import graphql_error_from_nodes


class ValuesOfCorrectType(June2018ReleaseValidationRule):
    """
    This validator validates that a given literal is of a valid type for a given parameter
    (in a field or a directive).

    More details @ https://graphql.github.io/graphql-spec/June2018/#sec-Values-of-Correct-Type
    """

    RULE_NAME = "values-of-correct-type"
    RULE_LINK = "https://graphql.github.io/graphql-spec/June2018/#sec-Values-of-Correct-Type"
    RULE_NUMBER = "5.6.1"

    def _validate_input_fields(
        self,
        arg,
        schema_type_name,
        schema_input_fields,
        object_node,
        errors,
        path,
        schema,
    ):  # pylint: disable=too-many-locals
        for schema_input_field in schema_input_fields:
            if (
                schema_input_field
                not in [x.name.value for x in object_node.fields]
                and isinstance(
                    schema_input_fields[schema_input_field].gql_type,
                    GraphQLNonNull,
                )
                and schema_input_fields[schema_input_field].default_value
                is None
            ):
                errors.append(
                    graphql_error_from_nodes(
                        message=f"Missing non nullable Input Field < {schema_input_field} > for Input Object < {schema_type_name} >.",
                        nodes=object_node,
                        path=path,
                        extensions=self._extensions,
                    )
                )

        for query_field_node in object_node.fields:
            if query_field_node.name.value not in schema_input_fields:
                errors.append(
                    graphql_error_from_nodes(
                        message=f"Unknown Input Field < {query_field_node.name.value} > in < {schema_type_name} > Input Object",
                        nodes=query_field_node,
                        path=path,
                        extensions=self._extensions,
                    )
                )
                continue

            c_argument_schema_type = schema_input_fields[
                query_field_node.name.value
            ].graphql_type
            r_argument_schema_type = reduce_type(c_argument_schema_type)
            if isinstance(r_argument_schema_type, str):
                r_argument_schema_type = schema.find_type(
                    r_argument_schema_type
                )

            errors = self._validate(
                r_argument_schema_type,
                c_argument_schema_type,
                arg,
                path,
                errors,
                schema,
                value_node=query_field_node.value,
                input_field=query_field_node,
            )
        return errors

    def _validate_input_object(
        self,
        arg,
        schema_argument_definition,
        object_node,
        errors,
        path,
        schema,
    ):
        if not isinstance(object_node, ObjectValueNode):
            errors.append(
                graphql_error_from_nodes(
                    message=f"Value is not a valid < {schema_argument_definition.name} > type, Object expected",
                    nodes=object_node,
                    path=path,
                    extensions=self._extensions,
                )
            )
        else:
            errors = self._validate_input_fields(
                arg,
                schema_argument_definition.name,
                schema_argument_definition.input_fields,
                object_node,
                errors,
                path,
                schema,
            )
        return errors

    def _validate(
        self,
        r_argument_schema_type,
        c_argument_schema_type,
        arg,
        path,
        errors,
        schema,
        value_node=None,
        input_field=None,
    ):  # pylint: disable=too-many-locals,too-many-arguments,too-many-branches,too-complex
        if value_node is None:
            value_node = arg.value

        if isinstance(value_node, VariableNode):
            # Handled by another Validator
            return errors

        if isinstance(c_argument_schema_type, GraphQLNonNull):
            if isinstance(value_node, NullValueNode):
                errors.append(
                    graphql_error_from_nodes(
                        message=f"Argument < {arg.name.value} > of non-null type < {c_argument_schema_type} > must not be null."
                        if not input_field
                        else f"Input Field < {input_field.name.value} > of non-null type < {c_argument_schema_type} > must not be null.",
                        nodes=arg if not input_field else input_field,
                        extensions=self._extensions,
                        path=path,
                    )
                )
                return errors

            errors = self._validate(
                r_argument_schema_type,
                c_argument_schema_type.gql_type,
                arg,
                path,
                errors,
                schema,
                value_node=value_node,
                input_field=input_field,
            )
            return errors

        if isinstance(c_argument_schema_type, GraphQLList):
            if isinstance(value_node, NullValueNode):
                return errors

            arg_values = (
                [value_node]
                if not isinstance(value_node, ListValueNode)
                else value_node.values
            )

            for arg_value in arg_values:
                if isinstance(arg_value, VariableNode):
                    continue  # Handled by another validator

                errors = self._validate(
                    r_argument_schema_type,
                    c_argument_schema_type.gql_type,
                    arg,
                    path,
                    errors,
                    schema,
                    value_node=arg_value,
                    input_field=input_field,
                )
            return errors

        if isinstance(value_node, NullValueNode):
            return errors  # Because it's not non null, null node is okay

        if isinstance(r_argument_schema_type, GraphQLScalarType) and (
            r_argument_schema_type.parse_literal(value_node) is UNDEFINED_VALUE
        ):
            errors.append(
                graphql_error_from_nodes(
                    message=f"Value {value_node.value} is not of correct type {r_argument_schema_type.name}",
                    nodes=input_field or arg,
                    extensions=self._extensions,
                    path=path,
                )
            )
            return errors

        if isinstance(r_argument_schema_type, GraphQLInputObjectType):
            errors = self._validate_input_object(
                arg=arg,
                schema_argument_definition=r_argument_schema_type,
                object_node=value_node,
                errors=errors,
                path=path,
                schema=schema,
            )
            return errors

        if isinstance(
            r_argument_schema_type, GraphQLEnumType
        ) and value_node.value not in [
            x.value for x in r_argument_schema_type.values
        ]:
            errors.append(
                graphql_error_from_nodes(
                    message=f"Value {value_node.value} is not a valid value for enum {r_argument_schema_type.name}",
                    nodes=arg,
                    path=path,
                    extensions=self._extensions,
                )
            )
            return errors

        return errors

    def _validate_arguments(
        self, schema_definition, query_node, errors, path, schema
    ):
        if not schema_definition:
            # Handled by another Validator. (5.3.1)
            return errors

        for arg in query_node.arguments:
            if not arg.name.value in schema_definition.arguments:
                continue  # Handled by another Validator (5.4.1)

            c_argument_schema_type = schema_definition.arguments[
                arg.name.value
            ].graphql_type
            r_argument_schema_type = reduce_type(c_argument_schema_type)
            if isinstance(r_argument_schema_type, str):
                r_argument_schema_type = schema.find_type(
                    r_argument_schema_type
                )

            errors = self._validate(
                r_argument_schema_type,
                c_argument_schema_type,
                arg,
                path,
                errors,
                schema,
            )
        return errors

    def _validate_field_arguments(self, path, schema, field, parent_type_name):
        schema_field = find_field(parent_type_name, field.name.value, schema)
        return self._validate_arguments(schema_field, field, [], path, schema)

    def _validate_directive_arguments(self, path, schema, directive):
        if not schema.has_directive(directive.name.value):
            return []  # Handled by another validator

        directive_schema_definition = schema.find_directive(
            directive.name.value
        )
        return self._validate_arguments(
            directive_schema_definition, directive, [], path, schema
        )

    def validate(self, path, schema, node, parent_type_name=None, **__):
        if isinstance(node, DirectiveNode):
            return self._validate_directive_arguments(path, schema, node)
        return self._validate_field_arguments(
            path, schema, node, parent_type_name
        )
