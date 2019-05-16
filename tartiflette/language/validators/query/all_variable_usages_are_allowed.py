from tartiflette.language.ast import (
    ListTypeNode,
    NonNullTypeNode,
    NullValueNode,
)
from tartiflette.language.validators.query.rule import (
    June2018ReleaseValidationRule,
)
from tartiflette.language.validators.query.utils import find_field_by_name
from tartiflette.types.list import GraphQLList
from tartiflette.types.non_null import GraphQLNonNull
from tartiflette.utils.errors import graphql_error_from_nodes


def _find_args_using_var_in_spread(spreads, per_fragment, args_using_var=None):
    if not args_using_var:
        args_using_var = []

    for spread in spreads:
        args_using_var = _find_args_using_var_in_spread(
            per_fragment.get(spread.name.value, {}).get("spreads", []),
            per_fragment,
            args_using_var,
        )
        args_using_var.extend(
            per_fragment.get(spread.name.value, {}).get("args_using_var", [])
        )

    return args_using_var


def _get_args_using_var(operation, per_operation, per_fragment):
    operation_key = operation.name.value if operation.name else "None"

    args_using_var = per_operation.get(operation_key, {}).get(
        "args_using_var", []
    )

    args_using_var.extend(
        _find_args_using_var_in_spread(
            per_operation.get(operation_key, {}).get("spreads", []),
            per_fragment,
        )
    )
    return args_using_var


def _find_schema_object(arg_info, schema):
    if arg_info["is_directive"]:
        if not schema.has_directive(arg_info["node_location"]):
            return None
        return schema.find_directive(arg_info["node_location"])
    return find_field_by_name(arg_info["node_location"], schema)


def _find_schema_argument(used_arg, schema):
    schema_object = _find_schema_object(used_arg, schema)
    if not schema_object:  # handled by another validator
        return None

    for arg_name, arg in schema_object.arguments.items():
        if used_arg["arg"].name.value == arg_name:
            return arg
    return None


def _find_variable_by_name(variables, name):
    for variable in variables:
        if variable.variable.name.value == name:
            return variable
    return None


def _validate_type_compatibility(var_type, schema_type):
    if isinstance(schema_type, GraphQLNonNull):
        if not isinstance(var_type, NonNullTypeNode):
            return False

        return _validate_type_compatibility(
            var_type.type, schema_type.gql_type
        )

    if isinstance(var_type, NonNullTypeNode):
        return _validate_type_compatibility(var_type.type, schema_type)

    if isinstance(schema_type, GraphQLList):
        if not isinstance(var_type, ListTypeNode):
            return False
        return _validate_type_compatibility(
            var_type.type, schema_type.gql_type
        )

    if isinstance(var_type, ListTypeNode):
        return False

    return var_type.name.value == str(schema_type)


def _validate_usage(schema_argument, variable_used):
    if isinstance(schema_argument.gql_type, GraphQLNonNull) and not isinstance(
        variable_used.type, NonNullTypeNode
    ):
        has_variable_a_df = not isinstance(
            variable_used.default_value, (NullValueNode, type(None))
        )
        has_argument_a_df = schema_argument.default_value is not None
        if not has_variable_a_df and not has_argument_a_df:
            return False
        return _validate_type_compatibility(
            variable_used.type, schema_argument.gql_type.gql_type
        )
    return _validate_type_compatibility(
        variable_used.type, schema_argument.gql_type
    )


class AllVariableUsagesAreAllowed(June2018ReleaseValidationRule):
    """
    This will look through all variable usages used in an operation
    and check that the type of the variable matches the type of the parameters it is used at.

    More details @ https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed
    """

    RULE_NAME = "all-variable-usages-are-allowed"
    RULE_LINK = "https://graphql.github.io/graphql-spec/June2018/#sec-All-Variable-Usages-are-Allowed"
    RULE_NUMBER = "5.8.5"

    def _validate_operation(
        self, operation, per_operation, per_fragment, schema
    ):
        errors = []
        for used_arg in _get_args_using_var(
            operation, per_operation, per_fragment
        ):
            schema_argument = _find_schema_argument(used_arg, schema)
            variable_used = _find_variable_by_name(
                operation.variable_definitions,
                used_arg["arg"].value.name.value,
            )

            if not schema_argument or not variable_used:
                continue  # Handled by another validators

            if not _validate_usage(schema_argument, variable_used):
                errors.append(
                    graphql_error_from_nodes(
                        message=f"Can't use < ${variable_used.variable.name.value} / {variable_used.type} > for type < {schema_argument.gql_type} >.",
                        nodes=[variable_used, used_arg["arg"].value],
                        path=used_arg["path"],
                        extensions=self._extensions,
                    )
                )

        return errors

    def validate(
        self,
        schema,
        operations=None,
        per_operation=None,
        per_fragment=None,
        **_,
    ):

        errors = []

        if not operations:
            return []  # No operation

        if not per_operation:
            per_operation = {}

        if not per_fragment:
            per_fragment = {}

        for operation in operations:
            errors.extend(
                self._validate_operation(
                    operation, per_operation, per_fragment, schema
                )
            )

        return errors
