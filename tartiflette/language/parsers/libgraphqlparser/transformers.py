from typing import List, Optional, Union

from tartiflette.language.ast import (
    ArgumentNode,
    BooleanValueNode,
    DirectiveNode,
    DocumentNode,
    EnumValueNode,
    FieldNode,
    FloatValueNode,
    FragmentDefinitionNode,
    FragmentSpreadNode,
    InlineFragmentNode,
    IntValueNode,
    ListTypeNode,
    ListValueNode,
    Location,
    NamedTypeNode,
    NameNode,
    NonNullTypeNode,
    NullValueNode,
    ObjectFieldNode,
    ObjectValueNode,
    OperationDefinitionNode,
    SelectionSetNode,
    StringValueNode,
    VariableDefinitionNode,
    VariableNode,
)


def _parse_location(location_ast) -> "Location":
    """
    TODO:
    :param location_ast: TODO:
    :type location_ast: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    return Location(
        line=location_ast["start"]["line"],
        column=location_ast["start"]["column"],
        line_end=location_ast["end"]["line"],
        column_end=location_ast["end"]["column"],
    )


def _parse_name(name_ast) -> "NameNode":
    """
    TODO:
    :param name_ast: TODO:
    :type name_ast: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    return NameNode(
        value=name_ast["value"], location=_parse_location(name_ast["loc"])
    )


def _parse_named_type(named_type_ast) -> "NamedTypeNode":
    """
    TODO:
    :param named_type_ast: TODO:
    :type named_type_ast: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    return NamedTypeNode(
        name=_parse_name(named_type_ast["name"]),
        location=_parse_location(named_type_ast["loc"]),
    )


def _parse_variable(variable_ast) -> "VariableNode":
    """
    TODO:
    :param variable_ast: TODO:
    :type variable_ast: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    return VariableNode(
        name=_parse_name(variable_ast["name"]),
        location=_parse_location(variable_ast["loc"]),
    )


def _parse_boolean_value(boolean_value_ast) -> "BooleanValueNode":
    """
    TODO:
    :param boolean_value_ast: TODO:
    :type boolean_value_ast: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    return BooleanValueNode(
        value=boolean_value_ast["value"],
        location=_parse_location(boolean_value_ast["loc"]),
    )


def _parse_enum_value(enum_value_ast) -> "EnumValueNode":
    """
    TODO:
    :param enum_value_ast: TODO:
    :type enum_value_ast: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    return EnumValueNode(
        value=enum_value_ast["value"],
        location=_parse_location(enum_value_ast["loc"]),
    )


def _parse_float_value(float_value_ast) -> "FloatValueNode":
    """
    TODO:
    :param float_value_ast: TODO:
    :type float_value_ast: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    return FloatValueNode(
        value=float_value_ast["value"],
        location=_parse_location(float_value_ast["loc"]),
    )


def _parse_int_value(int_value_ast) -> "IntValueNode":
    """
    TODO:
    :param int_value_ast: TODO:
    :type int_value_ast: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    return IntValueNode(
        value=int_value_ast["value"],
        location=_parse_location(int_value_ast["loc"]),
    )


def _parse_values(
    values_ast
) -> List[
    Union[
        "BooleanValueNode",
        "EnumValueNode",
        "FloatValueNode",
        "IntValueNode",
        "ListValueNode",
        "NullValueNode",
        "ObjectValueNode",
        "StringValueNode",
        "VariableNode",
    ]
]:
    """
    TODO:
    :param values_ast: TODO:
    :type values_ast: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    if values_ast:
        return [_parse_value(value) for value in values_ast]
    return []


def _parse_list_value(list_value_ast) -> "ListValueNode":
    """
    TODO:
    :param list_value_ast: TODO:
    :type list_value_ast: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    return ListValueNode(
        values=_parse_values(list_value_ast["values"]),
        location=_parse_location(list_value_ast["loc"]),
    )


def _parse_null_value(null_value_ast) -> "NullValueNode":
    """
    TODO:
    :param null_value_ast: TODO:
    :type null_value_ast: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    return NullValueNode(location=_parse_location(null_value_ast["loc"]))


def _parse_object_field(object_field_ast) -> "ObjectFieldNode":
    """
    TODO:
    :param object_field_ast: TODO:
    :type object_field_ast: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    return ObjectFieldNode(
        name=_parse_name(object_field_ast["name"]),
        value=_parse_value(object_field_ast["value"]),
        location=_parse_location(object_field_ast["loc"]),
    )


def _parse_object_fields(object_fields_ast) -> List["ObjectFieldNode"]:
    """
    TODO:
    :param object_fields_ast: TODO:
    :type object_fields_ast: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    if object_fields_ast:
        return [
            _parse_object_field(object_field)
            for object_field in object_fields_ast
        ]
    return []


def _parse_object_value(object_value_ast) -> "ObjectValueNode":
    """
    TODO:
    :param object_value_ast: TODO:
    :type object_value_ast: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    return ObjectValueNode(
        fields=_parse_object_fields(object_value_ast["fields"]),
        location=_parse_location(object_value_ast["loc"]),
    )


def _parse_string_value(string_value_ast) -> "StringValueNode":
    """
    TODO:
    :param string_value_ast: TODO:
    :type string_value_ast: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    return StringValueNode(
        value=string_value_ast["value"],
        location=_parse_location(string_value_ast["loc"]),
    )


_VALUE_PARSER_MAPPING = {
    "BooleanValue": _parse_boolean_value,
    "EnumValue": _parse_enum_value,
    "FloatValue": _parse_float_value,
    "IntValue": _parse_int_value,
    "ListValue": _parse_list_value,
    "NullValue": _parse_null_value,
    "ObjectValue": _parse_object_value,
    "StringValue": _parse_string_value,
    "Variable": _parse_variable,
}


def _parse_value(
    value_ast
) -> Optional[
    Union[
        "BooleanValueNode",
        "EnumValueNode",
        "FloatValueNode",
        "IntValueNode",
        "ListValueNode",
        "NullValueNode",
        "ObjectValueNode",
        "StringValueNode",
        "VariableNode",
    ]
]:
    """
    TODO:
    :param value_ast: TODO:
    :type value_ast: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    if value_ast:
        return _VALUE_PARSER_MAPPING[value_ast["kind"]](value_ast)
    return None


def _parse_argument(argument_ast) -> "ArgumentNode":
    """
    TODO:
    :param argument_ast: TODO:
    :type argument_ast: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    return ArgumentNode(
        name=_parse_name(argument_ast["name"]),
        value=_parse_value(argument_ast["value"]),
        location=_parse_location(argument_ast["loc"]),
    )


def _parse_arguments(arguments_ast) -> List["ArgumentNode"]:
    """
    TODO:
    :param arguments_ast: TODO:
    :type arguments_ast: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    if arguments_ast:
        return [_parse_argument(argument) for argument in arguments_ast]
    return []


def _parse_directive(directive_ast) -> "DirectiveNode":
    """
    TODO:
    :param directive_ast: TODO:
    :type directive_ast: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    return DirectiveNode(
        name=_parse_name(directive_ast["name"]),
        arguments=_parse_arguments(directive_ast["arguments"]),
        location=_parse_location(directive_ast["loc"]),
    )


def _parse_directives(directives_ast) -> List["DirectiveNode"]:
    """
    TODO:
    :param directives_ast: TODO:
    :type directives_ast: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    if directives_ast:
        return [_parse_directive(directive) for directive in directives_ast]
    return []


def _parse_field(field_ast) -> "FieldNode":
    """
    TODO:
    :param field_ast: TODO:
    :type field_ast: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    return FieldNode(
        alias=_parse_name(field_ast["alias"]) if field_ast["alias"] else None,
        name=_parse_name(field_ast["name"]),
        arguments=_parse_arguments(field_ast["arguments"]),
        directives=_parse_directives(field_ast["directives"]),
        selection_set=_parse_selection_set(field_ast["selectionSet"]),
        location=_parse_location(field_ast["loc"]),
    )


def _parse_fragment_spread(fragment_spread_ast) -> "FragmentSpreadNode":
    """
    TODO:
    :param fragment_spread_ast: TODO:
    :type fragment_spread_ast: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    return FragmentSpreadNode(
        name=_parse_name(fragment_spread_ast["name"]),
        directives=_parse_directives(fragment_spread_ast["directives"]),
        location=_parse_location(fragment_spread_ast["loc"]),
    )


def _parse_inline_fragment(inline_fragment_ast) -> "InlineFragmentNode":
    """
    TODO:
    :param inline_fragment_ast: TODO:
    :type inline_fragment_ast: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    return InlineFragmentNode(
        directives=_parse_directives(inline_fragment_ast["directives"]),
        type_condition=_parse_named_type(inline_fragment_ast["typeCondition"])
        if inline_fragment_ast["typeCondition"]
        else None,
        selection_set=_parse_selection_set(
            inline_fragment_ast["selectionSet"]
        ),
        location=_parse_location(inline_fragment_ast["loc"]),
    )


_SELECTION_PARSER_MAPPING = {
    "Field": _parse_field,
    "FragmentSpread": _parse_fragment_spread,
    "InlineFragment": _parse_inline_fragment,
}


def _parse_selection(
    selection_ast
) -> Union["FieldNode", "FragmentSpreadNode", "InlineFragmentNode"]:
    """
    TODO:
    :param selection_ast: TODO:
    :type selection_ast: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    return _SELECTION_PARSER_MAPPING[selection_ast["kind"]](selection_ast)


def _parse_selections(
    selections_ast
) -> List[Union["FieldNode", "FragmentSpreadNode", "InlineFragmentNode"]]:
    """
    TODO:
    :param selections_ast: TODO:
    :type selections_ast: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    if selections_ast:
        return [_parse_selection(selection) for selection in selections_ast]
    return []


def _parse_selection_set(selection_set_ast) -> Optional["SelectionSetNode"]:
    """
    TODO:
    :param selection_set_ast: TODO:
    :type selection_set_ast: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    if selection_set_ast:
        return SelectionSetNode(
            selections=_parse_selections(selection_set_ast["selections"]),
            location=_parse_location(selection_set_ast["loc"]),
        )
    return None


def _parse_fragment_definition(
    fragment_definition_ast
) -> "FragmentDefinitionNode":
    """
    TODO:
    :param fragment_definition_ast: TODO:
    :type fragment_definition_ast: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    return FragmentDefinitionNode(
        name=_parse_name(fragment_definition_ast["name"]),
        type_condition=_parse_named_type(
            fragment_definition_ast["typeCondition"]
        ),
        directives=_parse_directives(fragment_definition_ast["directives"]),
        selection_set=_parse_selection_set(
            fragment_definition_ast["selectionSet"]
        ),
        location=_parse_location(fragment_definition_ast["loc"]),
    )


def _parse_type(
    type_ast
) -> Union["ListTypeNode", "NonNullTypeNode", "NamedTypeNode"]:
    """
    TODO:
    :param type_ast: TODO:
    :type type_ast: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    if type_ast["kind"] == "ListType":
        return ListTypeNode(
            type=_parse_type(type_ast["type"]),
            location=_parse_location(type_ast["loc"]),
        )
    if type_ast["kind"] == "NonNullType":
        return NonNullTypeNode(
            type=_parse_type(type_ast["type"]),
            location=_parse_location(type_ast["loc"]),
        )
    return _parse_named_type(type_ast)


def _parse_variable_definition(
    variable_definition_ast
) -> "VariableDefinitionNode":
    """
    TODO:
    :param variable_definition_ast: TODO:
    :type variable_definition_ast: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    return VariableDefinitionNode(
        variable=_parse_variable(variable_definition_ast["variable"]),
        type=_parse_type(variable_definition_ast["type"]),
        default_value=_parse_value(variable_definition_ast["defaultValue"]),
        location=_parse_location(variable_definition_ast["loc"]),
    )


def _parse_variable_definitions(
    variable_definitions_ast
) -> List["VariableDefinitionNode"]:
    """
    TODO:
    :param variable_definitions_ast: TODO:
    :type variable_definitions_ast: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    if variable_definitions_ast:
        return [
            _parse_variable_definition(variable_definition)
            for variable_definition in variable_definitions_ast
        ]
    return []


def _parse_operation_definition(
    operation_definition_ast
) -> "OperationDefinitionNode":
    """
    TODO:
    :param operation_definition_ast: TODO:
    :type operation_definition_ast: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    return OperationDefinitionNode(
        operation_type=operation_definition_ast["operation"],
        name=_parse_name(operation_definition_ast["name"])
        if operation_definition_ast["name"]
        else None,
        variable_definitions=_parse_variable_definitions(
            operation_definition_ast["variableDefinitions"]
        ),
        directives=_parse_directives(operation_definition_ast["directives"]),
        selection_set=_parse_selection_set(
            operation_definition_ast["selectionSet"]
        ),
        location=_parse_location(operation_definition_ast["loc"]),
    )


_DEFINITION_PARSER_MAPPING = {
    "FragmentDefinition": _parse_fragment_definition,
    "OperationDefinition": _parse_operation_definition,
}


def _parse_definition(
    definition_ast
) -> Union["FragmentDefinitionNode", "OperationDefinitionNode"]:
    """
    TODO:
    :param definition_ast: TODO:
    :type definition_ast: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    return _DEFINITION_PARSER_MAPPING[definition_ast["kind"]](definition_ast)


def _parse_definitions(
    definitions_ast
) -> List[Union["FragmentDefinitionNode", "OperationDefinitionNode"]]:
    """
    TODO:
    :param definitions_ast: TODO:
    :type definitions_ast: TODO:
    :return: TODO:
    :rtype: TODO:
    """
    if definitions_ast:
        return [
            _parse_definition(definition) for definition in definitions_ast
        ]
    return []


def document_from_ast_json(document_ast) -> "DocumentNode":
    """
    TODO:
    :param document_ast: TODO:
    :type document_ast: TODO:
    :return: TODO:
    :rtype: TODO:

    :Example:
    TODO:
    """
    return DocumentNode(
        definitions=_parse_definitions(document_ast["definitions"]),
        location=_parse_location(document_ast["loc"]),
    )
