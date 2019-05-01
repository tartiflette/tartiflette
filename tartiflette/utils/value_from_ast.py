from typing import Any, Dict, Optional, Union

from tartiflette.language.ast import (
    EnumValueNode,
    ListValueNode,
    NullValueNode,
    ObjectValueNode,
    VariableNode,
)
from tartiflette.types.helpers.definition import (
    is_enum_type,
    is_input_object_type,
    is_list_type,
    is_non_null_type,
    is_scalar_type,
)

UndefinedValue = object()


def is_invalid(value) -> bool:
    """
    TODO:
    :param value: TODO:
    :type value: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    return value is UndefinedValue


def is_missing_variable(value_node, variables) -> bool:
    """
    TODO:
    :param value_node: TODO:
    :param variables: TODO:
    :type value_node: TODO:
    :type variables: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    return isinstance(value_node, VariableNode) and (
        not variables
        or value_node.name.value not in variables
        or is_invalid(variables[value_node.name.value])
    )


def value_from_ast(
    value_node: Union["ValueNode", "VariableNode"],
    schema_type: "GraphQLType",
    variables: Optional[Dict[str, Any]] = None,
) -> Any:
    """
    TODO:
    :param value_node: TODO:
    :param schema_type: TODO:
    :param variables: TODO:
    :type value_node: TODO:
    :type schema_type: TODO:
    :type variables: TODO:
    :return: TODO:
    :rtype: TODO:
    """

    if not value_node:
        # When there is no node, then there is also no defined value.
        return UndefinedValue

    if is_non_null_type(schema_type):
        if isinstance(value_node, NullValueNode):
            return UndefinedValue
        return value_from_ast(value_node, schema_type.ofType, variables)

    if isinstance(value_node, NullValueNode):
        return None

    if isinstance(value_node, VariableNode):
        var_name = value_node.name.value
        if not variables:
            return UndefinedValue

        value = variables.get(var_name, UndefinedValue)
        if is_invalid(value):
            return UndefinedValue

        if value is None and is_non_null_type(schema_type):
            return UndefinedValue
        return value

    if is_list_type(schema_type):
        item_type = schema_type.ofType
        if isinstance(value_node, ListValueNode):
            coerced_values = []
            for item_node in value_node.values:
                if is_missing_variable(item_node, variables):
                    if is_non_null_type(item_type):
                        return UndefinedValue
                    coerced_values.append(None)
                else:
                    item_value = value_from_ast(
                        item_node, item_type, variables
                    )
                    if is_invalid(item_value):
                        return UndefinedValue
                    coerced_values.append(item_value)
            return coerced_values

        coerced_value = value_from_ast(value_node, item_type, variables)
        if is_invalid(coerced_value):
            return UndefinedValue
        return [coerced_value]

    if is_input_object_type(schema_type):
        if not isinstance(value_node, ObjectValueNode):
            return UndefinedValue

        field_nodes = {
            field_node.name.value: field_node
            for field_node in value_node.fields
        }
        fields = schema_type.arguments

        coerced_object = {}
        for field_name, field in fields.items():
            if field_name not in field_nodes or is_missing_variable(
                field_nodes[field_name].value, variables
            ):
                # TODO: at schema build we should use UndefinedValue for
                # `default_value` attribute of a field to know if a field has
                # a defined default value (since default value could be `None`)
                # once done, we should check for `UndefinedValue` here.
                if field.default_value is not None:
                    coerced_object[field_name] = field.default_value
                # TODO: check if `gql_type` is the correct attr to call here
                elif is_non_null_type(field.gql_type):
                    return UndefinedValue
                continue

            field_value = value_from_ast(
                field_nodes[field_name].value, field.get_gql_type(), variables
            )
            if is_invalid(field_value):
                return UndefinedValue
            coerced_object[field_name] = field_value
        return coerced_object

    if is_enum_type(schema_type):
        if not isinstance(value_node, EnumValueNode):
            return UndefinedValue

        try:
            return schema_type.get_value(value_node.value)
        except KeyError:
            return UndefinedValue

    if is_scalar_type(schema_type):
        try:
            value = schema_type.parse_literal(value_node)
            if not is_invalid(value):
                return value
        except Exception:
            pass
        return UndefinedValue

    raise Exception(f"Unexpected input type: {schema_type}.")
