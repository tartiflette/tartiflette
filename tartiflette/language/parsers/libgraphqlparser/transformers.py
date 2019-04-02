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


def _parse_location(location_ast: dict) -> "Location":
    """
    Creates and returns a Location instance from a location's JSON AST
    libgraphqlparser representation.
    :param location_ast: location's JSON AST libgraphqlparser representation
    :type location_ast: dict
    :return: a Location instance equivalent to the JSON AST representation
    :rtype: Location
    """
    return Location(
        line=location_ast["start"]["line"],
        column=location_ast["start"]["column"],
        line_end=location_ast["end"]["line"],
        column_end=location_ast["end"]["column"],
    )


def _parse_name(name_ast: dict) -> "NameNode":
    """
    Creates and returns a NameNode instance from a name's JSON AST
    libgraphqlparser representation.
    :param name_ast: name's JSON AST libgraphqlparser representation
    :type name_ast: dict
    :return: a NameNode instance equivalent to the JSON AST representation
    :rtype: NameNode
    """
    return NameNode(
        value=name_ast["value"], location=_parse_location(name_ast["loc"])
    )


def _parse_named_type(named_type_ast: dict) -> "NamedTypeNode":
    """
    Creates and returns a NamedTypeNode instance from a named type's JSON AST
    libgraphqlparser representation.
    :param named_type_ast: named type's JSON AST libgraphqlparser
    representation
    :type named_type_ast: dict
    :return: a NamedTypeNode instance equivalent to the JSON AST representation
    :rtype: NamedTypeNode
    """
    return NamedTypeNode(
        name=_parse_name(named_type_ast["name"]),
        location=_parse_location(named_type_ast["loc"]),
    )


def _parse_variable(variable_ast: dict) -> "VariableNode":
    """
    Creates and returns a VariableNode instance from a variable's JSON AST
    libgraphqlparser representation.
    :param variable_ast: variable's JSON AST libgraphqlparser representation
    :type variable_ast: dict
    :return: a VariableNode instance equivalent to the JSON AST representation
    :rtype: VariableNode
    """
    return VariableNode(
        name=_parse_name(variable_ast["name"]),
        location=_parse_location(variable_ast["loc"]),
    )


def _parse_boolean_value(boolean_value_ast: dict) -> "BooleanValueNode":
    """
    Creates and returns a BooleanValueNode instance from a boolean value's JSON
    AST libgraphqlparser representation.
    :param boolean_value_ast: boolean value's JSON AST libgraphqlparser
    representation
    :type boolean_value_ast: dict
    :return: a BooleanValueNode instance equivalent to the JSON AST
    representation
    :rtype: BooleanValueNode
    """
    return BooleanValueNode(
        value=boolean_value_ast["value"],
        location=_parse_location(boolean_value_ast["loc"]),
    )


def _parse_enum_value(enum_value_ast: dict) -> "EnumValueNode":
    """
    Creates and returns an EnumValueNode instance from an enum value's JSON AST
    libgraphqlparser representation.
    :param enum_value_ast: enum value's JSON AST libgraphqlparser
    representation
    :type enum_value_ast: dict
    :return: an EnumValueNode instance equivalent to the JSON AST
    representation
    :rtype: EnumValueNode
    """
    return EnumValueNode(
        value=enum_value_ast["value"],
        location=_parse_location(enum_value_ast["loc"]),
    )


def _parse_float_value(float_value_ast: dict) -> "FloatValueNode":
    """
    Creates and returns a FloatValueNode instance from a float value's JSON AST
    libgraphqlparser representation.
    :param float_value_ast: float value's JSON AST libgraphqlparser
    representation
    :type float_value_ast: dict
    :return: a FloatValueNode instance equivalent to the JSON AST
    representation
    :rtype: FloatValueNode
    """
    return FloatValueNode(
        value=float(float_value_ast["value"]),
        location=_parse_location(float_value_ast["loc"]),
    )


def _parse_int_value(int_value_ast: dict) -> "IntValueNode":
    """
    Creates and returns an IntValueNode instance from an int value's JSON AST
    libgraphqlparser representation.
    :param int_value_ast: int value's JSON AST libgraphqlparser representation
    :type int_value_ast: dict
    :return: an IntValueNode instance equivalent to the JSON AST representation
    :rtype: IntValueNode
    """
    return IntValueNode(
        value=int(int_value_ast["value"]),
        location=_parse_location(int_value_ast["loc"]),
    )


def _parse_values(
    values_ast: Optional[List[dict]]
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
    Creates and returns a list of ValueNode instances from a list of value's
    JSON AST libgraphqlparser representation.
    :param values_ast: list of value's JSON AST libgraphqlparser representation
    :type values_ast: Optional[List[dict]]
    :return: a list of ValueNode instances equivalent to the JSON AST
    representation
    :rtype: List[Union[BooleanValueNode, EnumValueNode, FloatValueNode, IntValueNode, ListValueNode, NullValueNode, ObjectValueNode, StringValueNode, VariableNode]]
    """
    if values_ast:
        return [_parse_value(value) for value in values_ast]
    return []


def _parse_list_value(list_value_ast: dict) -> "ListValueNode":
    """
    Creates and returns a ListValueNode instance from a list value's JSON AST
    libgraphqlparser representation.
    :param list_value_ast: list value's JSON AST libgraphqlparser
    representation
    :type list_value_ast: dict
    :return: a ListValueNode instance equivalent to the JSON AST representation
    :rtype: ListValueNode
    """
    return ListValueNode(
        values=_parse_values(list_value_ast["values"]),
        location=_parse_location(list_value_ast["loc"]),
    )


def _parse_null_value(null_value_ast: dict) -> "NullValueNode":
    """
    Creates and returns a NullValueNode instance from a null value's JSON AST
    libgraphqlparser representation.
    :param null_value_ast: null value's JSON AST libgraphqlparser
    representation
    :type null_value_ast: dict
    :return: a NullValueNode instance equivalent to the JSON AST representation
    :rtype: NullValueNode
    """
    return NullValueNode(location=_parse_location(null_value_ast["loc"]))


def _parse_object_field(object_field_ast: dict) -> "ObjectFieldNode":
    """
    Creates and returns an ObjectFieldNode instance from an object field's JSON
    AST libgraphqlparser representation.
    :param object_field_ast: object field's JSON AST libgraphqlparser
    representation
    :type object_field_ast: dict
    :return: an ObjectFieldNode instance equivalent to the JSON AST
    representation
    :rtype: ObjectFieldNode
    """
    return ObjectFieldNode(
        name=_parse_name(object_field_ast["name"]),
        value=_parse_value(object_field_ast["value"]),
        location=_parse_location(object_field_ast["loc"]),
    )


def _parse_object_fields(
    object_fields_ast: Optional[List[dict]]
) -> List["ObjectFieldNode"]:
    """
    Creates and returns a list of ObjectFieldNode instances from a list of
    object field's JSON AST libgraphqlparser representation.
    :param object_fields_ast: list of object field's JSON AST libgraphqlparser
    representation
    :type object_fields_ast: Optional[List[dict]]
    :return: a list of ObjectFieldNode instances equivalent to the JSON AST
    representation
    :rtype: List[ObjectFieldNode]
    """
    if object_fields_ast:
        return [
            _parse_object_field(object_field)
            for object_field in object_fields_ast
        ]
    return []


def _parse_object_value(object_value_ast: dict) -> "ObjectValueNode":
    """
    Creates and returns an ObjectValueNode instance from an object value's JSON
    AST libgraphqlparser representation.
    :param object_value_ast: object value's JSON AST libgraphqlparser
    representation
    :type object_value_ast: dict
    :return: an ObjectValueNode instance equivalent to the JSON AST
    representation
    :rtype: ObjectValueNode
    """
    return ObjectValueNode(
        fields=_parse_object_fields(object_value_ast["fields"]),
        location=_parse_location(object_value_ast["loc"]),
    )


def _parse_string_value(string_value_ast: dict) -> "StringValueNode":
    """
    Creates and returns a StringValueNode instance from a string value's JSON
    AST libgraphqlparser representation.
    :param string_value_ast: string value's JSON AST libgraphqlparser
    representation
    :type string_value_ast: dict
    :return: a StringValueNode instance equivalent to the JSON AST
    representation
    :rtype: StringValueNode
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
    value_ast: Optional[dict]
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
    Creates and returns a ValueNode instance from a value's JSON AST
    libgraphqlparser representation.
    :param value_ast: value's JSON AST libgraphqlparser representation
    :type value_ast: Optional[dict]
    :return: a ValueNode instance equivalent to the JSON AST representation
    :rtype: Optional[Union[BooleanValueNode, EnumValueNode, FloatValueNode, IntValueNode, ListValueNode, NullValueNode, ObjectValueNode, StringValueNode, VariableNode]]
    """
    if value_ast:
        return _VALUE_PARSER_MAPPING[value_ast["kind"]](value_ast)
    return None


def _parse_argument(argument_ast: dict) -> "ArgumentNode":
    """
    Creates and returns an ArgumentNode instance from an argument's JSON AST
    libgraphqlparser representation.
    :param argument_ast: argument's JSON AST libgraphqlparser representation
    :type argument_ast: dict
    :return: an ArgumentNode instance equivalent to the JSON AST representation
    :rtype: ArgumentNode
    """
    return ArgumentNode(
        name=_parse_name(argument_ast["name"]),
        value=_parse_value(argument_ast["value"]),
        location=_parse_location(argument_ast["loc"]),
    )


def _parse_arguments(
    arguments_ast: Optional[List[dict]]
) -> List["ArgumentNode"]:
    """
    Creates and returns a list of ArgumentNode instances from a list of
    argument's JSON AST libgraphqlparser representation.
    :param arguments_ast: list of argument's JSON AST libgraphqlparser
    representation
    :type arguments_ast: Optional[List[dict]]
    :return: a list of ArgumentNode instances equivalent to the JSON AST
    representation
    :rtype: List[ArgumentNode]
    """
    if arguments_ast:
        return [_parse_argument(argument) for argument in arguments_ast]
    return []


def _parse_directive(directive_ast: dict) -> "DirectiveNode":
    """
    Creates and returns a DirectiveNode instance from a directive's JSON AST
    libgraphqlparser representation.
    :param directive_ast: directive's JSON AST libgraphqlparser representation
    :type directive_ast: dict
    :return: a DirectiveNode instance equivalent to the JSON AST representation
    :rtype: DirectiveNode
    """
    return DirectiveNode(
        name=_parse_name(directive_ast["name"]),
        arguments=_parse_arguments(directive_ast["arguments"]),
        location=_parse_location(directive_ast["loc"]),
    )


def _parse_directives(
    directives_ast: Optional[List[dict]]
) -> List["DirectiveNode"]:
    """
    Creates and returns a list of DirectiveNode instances from a list of
    directive's JSON AST libgraphqlparser representation.
    :param directives_ast: list of directive's JSON AST libgraphqlparser
    representation
    :type directives_ast: Optional[List[dict]]
    :return: a list of DirectiveNode instances equivalent to the JSON AST
    representation
    :rtype: List[DirectiveNode]
    """
    if directives_ast:
        return [_parse_directive(directive) for directive in directives_ast]
    return []


def _parse_field(field_ast: dict) -> "FieldNode":
    """
    Creates and returns a FieldNode instance from a field's JSON AST
    libgraphqlparser representation.
    :param field_ast: field's JSON AST libgraphqlparser representation
    :type field_ast: dict
    :return: a FieldNode instance equivalent to the JSON AST representation
    :rtype: FieldNode
    """
    return FieldNode(
        alias=_parse_name(field_ast["alias"]) if field_ast["alias"] else None,
        name=_parse_name(field_ast["name"]),
        arguments=_parse_arguments(field_ast["arguments"]),
        directives=_parse_directives(field_ast["directives"]),
        selection_set=_parse_selection_set(field_ast["selectionSet"]),
        location=_parse_location(field_ast["loc"]),
    )


def _parse_fragment_spread(fragment_spread_ast: dict) -> "FragmentSpreadNode":
    """
    Creates and returns a FragmentSpreadNode instance from a fragment spread's
    JSON AST libgraphqlparser representation.
    :param fragment_spread_ast: fragment spread's JSON AST libgraphqlparser
    representation
    :type fragment_spread_ast: dict
    :return: a FragmentSpreadNode instance equivalent to the JSON AST
    representation
    :rtype: FragmentSpreadNode
    """
    return FragmentSpreadNode(
        name=_parse_name(fragment_spread_ast["name"]),
        directives=_parse_directives(fragment_spread_ast["directives"]),
        location=_parse_location(fragment_spread_ast["loc"]),
    )


def _parse_inline_fragment(inline_fragment_ast: dict) -> "InlineFragmentNode":
    """
    Creates and returns an InlineFragmentNode instance from an inline spread's
    JSON AST libgraphqlparser representation.
    :param inline_fragment_ast: inline spread's JSON AST libgraphqlparser
    representation
    :type inline_fragment_ast: dict
    :return: an InlineFragmentNode instance equivalent to the JSON AST
    representation
    :rtype: InlineFragmentNode
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
    selection_ast: dict
) -> Union["FieldNode", "FragmentSpreadNode", "InlineFragmentNode"]:
    """
    Creates and returns a SelectionNode instance from a selection's JSON AST
    libgraphqlparser representation.
    :param selection_ast: selection's JSON AST libgraphqlparser representation
    :type selection_ast: dict
    :return: a SelectionNode instance equivalent to the JSON AST representation
    :rtype: Union[FieldNode, FragmentSpreadNode, InlineFragmentNode]
    """
    return _SELECTION_PARSER_MAPPING[selection_ast["kind"]](selection_ast)


def _parse_selections(
    selections_ast: Optional[List[dict]]
) -> List[Union["FieldNode", "FragmentSpreadNode", "InlineFragmentNode"]]:
    """
    Creates and returns a list of SelectionNode instances from a list of
    selection's JSON AST libgraphqlparser representation.
    :param selections_ast: list of selection's JSON AST libgraphqlparser
    representation
    :type selections_ast: Optional[List[dict]]
    :return: a list of SelectionNode instances equivalent to the JSON AST
    representation
    :rtype: List[Union[FieldNode, FragmentSpreadNode, InlineFragmentNode]]
    """
    if selections_ast:
        return [_parse_selection(selection) for selection in selections_ast]
    return []


def _parse_selection_set(
    selection_set_ast: Optional[dict]
) -> Optional["SelectionSetNode"]:
    """
    Creates and returns a SelectionSetNode instance from a selection set's JSON
    AST libgraphqlparser representation.
    :param selection_set_ast: selection set's JSON AST libgraphqlparser
    representation
    :type selection_set_ast: Optional[dict]
    :return: a SelectionSetNode instance equivalent to the JSON AST
    representation
    :rtype: Optional[SelectionSetNode]
    """
    if selection_set_ast:
        return SelectionSetNode(
            selections=_parse_selections(selection_set_ast["selections"]),
            location=_parse_location(selection_set_ast["loc"]),
        )
    return None


def _parse_fragment_definition(
    fragment_definition_ast: dict
) -> "FragmentDefinitionNode":
    """
    Creates and returns a FragmentDefinitionNode instance from a fragment
    definition's JSON AST libgraphqlparser representation.
    :param fragment_definition_ast: fragment definition's JSON AST
    libgraphqlparser representation
    :type fragment_definition_ast: dict
    :return: a FragmentDefinitionNode instance equivalent to the JSON AST
    representation
    :rtype: FragmentDefinitionNode
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
    type_ast: dict
) -> Union["ListTypeNode", "NonNullTypeNode", "NamedTypeNode"]:
    """
    Creates and returns a TypeNode from a type's JSON AST libgraphqlparser
    representation.
    :param type_ast: type's JSON AST libgraphqlparser representation
    :type type_ast: dict
    :return: a TypeNode instance equivalent to the JSON AST representation
    :rtype: Union[ListTypeNode, NonNullTypeNode, NamedTypeNode]
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
    variable_definition_ast: dict
) -> "VariableDefinitionNode":
    """
    Creates and returns a VariableDefinitionNode instance from a variable
    definition's JSON AST libgraphqlparser representation.
    :param variable_definition_ast: variable definition's JSON AST
    libgraphqlparser representation
    :type variable_definition_ast: dict
    :return: a VariableDefinitionNode instance equivalent to the JSON AST
    representation
    :rtype: VariableDefinitionNode
    """
    return VariableDefinitionNode(
        variable=_parse_variable(variable_definition_ast["variable"]),
        type=_parse_type(variable_definition_ast["type"]),
        default_value=_parse_value(variable_definition_ast["defaultValue"]),
        location=_parse_location(variable_definition_ast["loc"]),
    )


def _parse_variable_definitions(
    variable_definitions_ast: Optional[List[dict]]
) -> List["VariableDefinitionNode"]:
    """
    Creates and returns a list of VariableDefinitionNode instances from a list
    of variable definition's JSON AST libgraphqlparser representation.
    :param variable_definitions_ast: list of variable definition's JSON AST
    libgraphqlparser representation
    :type variable_definitions_ast: Optional[List[dict]]
    :return: a list of VariableDefinitionNode instances equivalent to the JSON
    AST representation
    :rtype: List[VariableDefinitionNode]
    """
    if variable_definitions_ast:
        return [
            _parse_variable_definition(variable_definition)
            for variable_definition in variable_definitions_ast
        ]
    return []


def _parse_operation_definition(
    operation_definition_ast: dict
) -> "OperationDefinitionNode":
    """
    Creates and returns an OperationDefinitionNode instance from an operation
    definition's JSON AST libgraphqlparser representation.
    :param operation_definition_ast: operation definition's JSON AST
    libgraphqlparser representation
    :type operation_definition_ast: dict
    :return: an OperationDefinitionNode instance equivalent to the JSON AST
    representation
    :rtype: OperationDefinitionNode
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
    definition_ast: dict
) -> Union["FragmentDefinitionNode", "OperationDefinitionNode"]:
    """
    Creates and returns a DefinitionNode instance from a definition's JSON AST
    libgraphqlparser representation.
    :param definition_ast: definition's JSON AST libgraphqlparser
    representation
    :type definition_ast: dict
    :return: a DefinitionNode instance equivalent to the JSON AST
    representation
    :rtype: Union[FragmentDefinitionNode, OperationDefinitionNode]
    """
    return _DEFINITION_PARSER_MAPPING[definition_ast["kind"]](definition_ast)


def _parse_definitions(
    definitions_ast: Optional[List[dict]]
) -> List[Union["FragmentDefinitionNode", "OperationDefinitionNode"]]:
    """
    Creates and returns a list of DefinitionNode instances from a list of
    definition's JSON AST libgraphqlparser representation.
    :param definitions_ast: list of definition's JSON AST libgraphqlparser
    representation
    :type definitions_ast: Optional[List[dict]]
    :return: a list of DefinitionNode instances equivalent to the JSON AST
    representation
    :rtype: List[Union[FragmentDefinitionNode, OperationDefinitionNode]]
    """
    if definitions_ast:
        return [
            _parse_definition(definition) for definition in definitions_ast
        ]
    return []


def document_from_ast_json(document_ast: dict) -> "DocumentNode":
    """
    Creates and returns a DocumentNode instance from a document's JSON AST
    libgraphqlparser representation.
    :param document_ast: document's JSON AST libgraphqlparser representation
    :type document_ast: dict
    :return: a DocumentNode instance equivalent to the JSON AST representation
    :rtype: DocumentNode

    :Example:

    >>> from tartiflette.language.parsers.libgraphqlparser.transformers import (
    >>>     document_from_ast_json
    >>> )
    >>>
    >>>
    >>> document = document_from_ast_json({
    >>>     "kind": "Document",
    >>>     "loc": {
    >>>         "start": {"line": 2, "column": 13},
    >>>         "end": {"line": 4, "column": 14},
    >>>     },
    >>>     "definitions": [
    >>>         {
    >>>             "kind": "OperationDefinition",
    >>>             "loc": {
    >>>                 "start": {"line": 2, "column": 13},
    >>>                 "end": {"line": 4, "column": 14},
    >>>             },
    >>>             "operation": "query",
    >>>             "name": None,
    >>>             "variableDefinitions": None,
    >>>             "directives": None,
    >>>             "selectionSet": {
    >>>                 "kind": "SelectionSet",
    >>>                 "loc": {
    >>>                     "start": {"line": 2, "column": 13},
    >>>                     "end": {"line": 4, "column": 14},
    >>>                 },
    >>>                 "selections": [
    >>>                     {
    >>>                         "kind": "Field",
    >>>                         "loc": {
    >>>                             "start": {"line": 3, "column": 15},
    >>>                             "end": {"line": 3, "column": 20},
    >>>                         },
    >>>                         "alias": None,
    >>>                         "name": {
    >>>                             "kind": "Name",
    >>>                             "loc": {
    >>>                                 "start": {"line": 3, "column": 15},
    >>>                                 "end": {"line": 3, "column": 20},
    >>>                             },
    >>>                             "value": "hello",
    >>>                         },
    >>>                         "arguments": None,
    >>>                         "directives": None,
    >>>                         "selectionSet": None,
    >>>                     }
    >>>                 ],
    >>>             },
    >>>         }
    >>>     ],
    >>> })
    """
    return DocumentNode(
        definitions=_parse_definitions(document_ast["definitions"]),
        location=_parse_location(document_ast["loc"]),
    )
