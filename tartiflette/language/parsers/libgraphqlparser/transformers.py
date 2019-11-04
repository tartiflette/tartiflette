from typing import List, Optional, Union

from tartiflette.coercers.common import Path
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
from tartiflette.language.validators import Validators
from tartiflette.language.validators.query import RULE_SET
from tartiflette.language.validators.query.utils import (
    get_schema_field_type_name,
)

__all__ = ("document_from_ast_json",)


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


def _parse_variable(
    variable_ast: dict, validators: Validators, *_
) -> "VariableNode":
    """
    Creates and returns a VariableNode instance from a variable's JSON AST
    libgraphqlparser representation.
    :param variable_ast: variable's JSON AST libgraphqlparser representation
    :type variable_ast: dict
    :param validators: the validators to use in order to validate this definition
    :type validators: Validators
    :param _: Ignored parameters
    :return: a VariableNode instance equivalent to the JSON AST representation
    :rtype: VariableNode
    """

    variable = VariableNode(
        name=_parse_name(variable_ast["name"]),
        location=_parse_location(variable_ast["loc"]),
    )

    if not validators.ctx.get("in_variable_definitions", False):
        if validators.ctx["in_operation"]:
            validators.ctx["per_operation"][
                validators.ctx["current_operation_name"]
            ].setdefault("used_vars", []).append(variable)
        else:
            validators.ctx["per_fragment"][
                validators.ctx["current_fragment_name"]
            ].setdefault("used_vars", []).append(variable)

    return variable


def _parse_boolean_value(boolean_value_ast: dict, *_) -> "BooleanValueNode":
    """
    Creates and returns a BooleanValueNode instance from a boolean value's JSON
    AST libgraphqlparser representation.
    :param boolean_value_ast: boolean value's JSON AST libgraphqlparser
    representation
    :param _: Ignored parameter
    :type boolean_value_ast: dict
    :return: a BooleanValueNode instance equivalent to the JSON AST
    representation
    :rtype: BooleanValueNode
    """
    return BooleanValueNode(
        value=boolean_value_ast["value"],
        location=_parse_location(boolean_value_ast["loc"]),
    )


def _parse_enum_value(enum_value_ast: dict, *_) -> "EnumValueNode":
    """
    Creates and returns an EnumValueNode instance from an enum value's JSON AST
    libgraphqlparser representation.
    :param enum_value_ast: enum value's JSON AST libgraphqlparser
    representation
    :param _: Ignored parameter
    :type enum_value_ast: dict
    :return: an EnumValueNode instance equivalent to the JSON AST
    representation
    :rtype: EnumValueNode
    """
    return EnumValueNode(
        value=enum_value_ast["value"],
        location=_parse_location(enum_value_ast["loc"]),
    )


def _parse_float_value(float_value_ast: dict, *_) -> "FloatValueNode":
    """
    Creates and returns a FloatValueNode instance from a float value's JSON AST
    libgraphqlparser representation.
    :param float_value_ast: float value's JSON AST libgraphqlparser
    representation
    :param _: Ignored parameter
    :type float_value_ast: dict
    :return: a FloatValueNode instance equivalent to the JSON AST
    representation
    :rtype: FloatValueNode
    """
    return FloatValueNode(
        value=float_value_ast["value"],
        location=_parse_location(float_value_ast["loc"]),
    )


def _parse_int_value(int_value_ast: dict, *_) -> "IntValueNode":
    """
    Creates and returns an IntValueNode instance from an int value's JSON AST
    libgraphqlparser representation.
    :param int_value_ast: int value's JSON AST libgraphqlparser representation
    :type int_value_ast: dict
    :param _: Ignored parameter
    :return: an IntValueNode instance equivalent to the JSON AST representation
    :rtype: IntValueNode
    """
    return IntValueNode(
        value=int_value_ast["value"],
        location=_parse_location(int_value_ast["loc"]),
    )


def _parse_values(
    values_ast: Optional[List[dict]], validators: Validators, path: Path
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
    :param validators: the validators to use in order to validate this definition
    :type validators: Validators
    :param path: a Path object that contains the current field path
    :type path: Path
    :return: a list of ValueNode instances equivalent to the JSON AST
    representation
    :rtype: List[Union[BooleanValueNode, EnumValueNode, FloatValueNode, IntValueNode, ListValueNode, NullValueNode, ObjectValueNode, StringValueNode, VariableNode]]
    """
    if values_ast:
        return [_parse_value(value, validators, path) for value in values_ast]
    return []


def _parse_list_value(
    list_value_ast: dict, validators: Validators, path: Path
) -> "ListValueNode":
    """
    Creates and returns a ListValueNode instance from a list value's JSON AST
    libgraphqlparser representation.
    :param list_value_ast: list value's JSON AST libgraphqlparser
    representation
    :type list_value_ast: dict
    :param validators: the validators to use in order to validate this definition
    :type validators: Validators
    :param path: a Path object that contains the current field path
    :type path: Path
    :return: a ListValueNode instance equivalent to the JSON AST representation
    :rtype: ListValueNode
    """
    return ListValueNode(
        values=_parse_values(list_value_ast["values"], validators, path),
        location=_parse_location(list_value_ast["loc"]),
    )


def _parse_null_value(null_value_ast: dict, *_) -> "NullValueNode":
    """
    Creates and returns a NullValueNode instance from a null value's JSON AST
    libgraphqlparser representation.
    :param null_value_ast: null value's JSON AST libgraphqlparser
    representation
    :type null_value_ast: dict
    :param _: Ignored parameter
    :return: a NullValueNode instance equivalent to the JSON AST representation
    :rtype: NullValueNode
    """
    return NullValueNode(location=_parse_location(null_value_ast["loc"]))


def _parse_object_field(
    object_field_ast: dict, validators: Validators, path: Path
) -> "ObjectFieldNode":
    """
    Creates and returns an ObjectFieldNode instance from an object field's JSON
    AST libgraphqlparser representation.
    :param object_field_ast: object field's JSON AST libgraphqlparser
    representation
    :type object_field_ast: dict
    :param validators: the validators to use in order to validate this definition
    :type validators: Validators
    :param path: a Path object that contains the current field path
    :type path: Path
    :return: an ObjectFieldNode instance equivalent to the JSON AST
    representation
    :rtype: ObjectFieldNode
    """
    return ObjectFieldNode(
        name=_parse_name(object_field_ast["name"]),
        value=_parse_value(object_field_ast["value"], validators, path),
        location=_parse_location(object_field_ast["loc"]),
    )


def _parse_object_fields(
    object_fields_ast: Optional[List[dict]], validators: Validators, path: Path
) -> List["ObjectFieldNode"]:
    """
    Creates and returns a list of ObjectFieldNode instances from a list of
    object field's JSON AST libgraphqlparser representation.
    :param object_fields_ast: list of object field's JSON AST libgraphqlparser
    representation
    :param validators: the validators to use in order to validate this definition
    :type validators: Validators
    :param path: a Path object that contains the current field path
    :type path: Path
    :type object_fields_ast: Optional[List[dict]]
    :return: a list of ObjectFieldNode instances equivalent to the JSON AST
    representation
    :rtype: List[ObjectFieldNode]
    """
    if object_fields_ast:
        object_fields = [
            _parse_object_field(object_field, validators, path)
            for object_field in object_fields_ast
        ]

        validators.validate(
            "input-object-field-uniqueness",
            input_fields=object_fields,
            path=path,
        )

        return object_fields
    return []


def _parse_object_value(
    object_value_ast: dict, validators: Validators, path: Path
) -> "ObjectValueNode":
    """
    Creates and returns an ObjectValueNode instance from an object value's JSON
    AST libgraphqlparser representation.
    :param object_value_ast: object value's JSON AST libgraphqlparser
    representation
    :type object_value_ast: dict
    :param validators: the validators to use in order to validate this definition
    :type validators: Validators
    :param path: a Path object that contains the current field path
    :type path: Path
    :return: an ObjectValueNode instance equivalent to the JSON AST
    representation
    :rtype: ObjectValueNode
    """
    return ObjectValueNode(
        fields=_parse_object_fields(
            object_value_ast["fields"], validators, path
        ),
        location=_parse_location(object_value_ast["loc"]),
    )


def _parse_string_value(string_value_ast: dict, *_) -> "StringValueNode":
    """
    Creates and returns a StringValueNode instance from a string value's JSON
    AST libgraphqlparser representation.
    :param string_value_ast: string value's JSON AST libgraphqlparser
    representation
    :type string_value_ast: dict
    :param _: Ignored parameter
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
    value_ast: Optional[dict], validators: Validators, path: Path
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
    :param validators: the validators to use in order to validate this definition
    :type validators: Validators
    :param path: a Path object that contains the current field path
    :type path: Path
    :return: a ValueNode instance equivalent to the JSON AST representation
    :rtype: Optional[Union[BooleanValueNode, EnumValueNode, FloatValueNode, IntValueNode, ListValueNode, NullValueNode, ObjectValueNode, StringValueNode, VariableNode]]
    """
    if value_ast:
        return _VALUE_PARSER_MAPPING[value_ast["kind"]](
            value_ast, validators, path
        )
    return None


def _parse_argument(
    argument_ast: dict, validators: Validators, path: Path
) -> "ArgumentNode":
    """
    Creates and returns an ArgumentNode instance from an argument's JSON AST
    libgraphqlparser representation.
    :param argument_ast: argument's JSON AST libgraphqlparser representation
    :type argument_ast: dict
    :param validators: the validators to use in order to validate this definition
    :type validators: Validators
    :param path: a Path object that contains the current field path
    :type path: Path
    :return: an ArgumentNode instance equivalent to the JSON AST representation
    :rtype: ArgumentNode
    """
    arg = ArgumentNode(
        name=_parse_name(argument_ast["name"]),
        value=_parse_value(argument_ast["value"], validators, path),
        location=_parse_location(argument_ast["loc"]),
    )

    if isinstance(arg.value, VariableNode):
        loca = (
            validators.ctx["current_directive_name"]
            if validators.ctx.get("in_directive", False)
            else validators.ctx["current_field_name"]
        )

        if validators.ctx["in_operation"]:
            validators.ctx["per_operation"][
                validators.ctx["current_operation_name"]
            ].setdefault("args_using_var", []).append(
                {
                    "arg": arg,
                    "node_location": loca,
                    "is_directive": validators.ctx.get("in_directive", False),
                    "path": path,
                }
            )
        else:
            validators.ctx["per_fragment"][
                validators.ctx["current_fragment_name"]
            ].setdefault("args_using_var", []).append(
                {
                    "arg": arg,
                    "node_location": loca,
                    "is_directive": validators.ctx.get("in_directive", False),
                    "path": path,
                }
            )

    return arg


def _parse_arguments(
    arguments_ast: Optional[List[dict]], validators: "Validators", path: "Path"
) -> List["ArgumentNode"]:
    """
    Creates and returns a list of ArgumentNode instances from a list of
    argument's JSON AST libgraphqlparser representation.
    :param arguments_ast: list of argument's JSON AST libgraphqlparser
    representation
    :type arguments_ast: Optional[List[dict]]
    :param validators: the Validators object that will be used to validate these arguments
    :param path: a Path object that contains the current field path
    :type validators: Validators
    :type path: Path
    :return: a list of ArgumentNode instances equivalent to the JSON AST
    representation
    :rtype: List[ArgumentNode]
    """
    if arguments_ast:
        arguments = [
            _parse_argument(argument, validators, path)
            for argument in arguments_ast
        ]
        validators.validate(
            rule="argument-uniqueness", arguments=arguments, path=path
        )
        return arguments
    return []


def _parse_directive(
    directive_ast: dict, validators: "Validators", path: "Path"
) -> "DirectiveNode":
    """
    Creates and returns a DirectiveNode instance from a directive's JSON AST
    libgraphqlparser representation.
    :param directive_ast: directive's JSON AST libgraphqlparser representation
    :type directive_ast: dict
    :param validators: the Validators object that will be used to validate these arguments
    :param path: a Path object that contains the current field path
    :type validators: Validators
    :type path: Path
    :return: a DirectiveNode instance equivalent to the JSON AST representation
    :rtype: DirectiveNode
    """
    name = _parse_name(directive_ast["name"])
    validators.ctx["in_directive"] = True
    validators.ctx["current_directive_name"] = name.value

    directive = DirectiveNode(
        name=name,
        arguments=_parse_arguments(
            directive_ast["arguments"], validators, path
        ),
        location=_parse_location(directive_ast["loc"]),
    )

    validators.ctx["in_directive"] = False

    validators.validate(
        rule="values-of-correct-type", node=directive, path=path
    )

    validators.validate(rule="argument-names", node=directive, path=path)

    validators.validate(rule="required-arguments", node=directive, path=path)

    validators.validate(
        rule="directives-are-defined", directive=directive, path=path
    )

    return directive


def _parse_directives(
    directives_ast: Optional[List[dict]],
    validators: "Validators",
    path: "Path",
) -> List["DirectiveNode"]:
    """
    Creates and returns a list of DirectiveNode instances from a list of
    directive's JSON AST libgraphqlparser representation.
    :param directives_ast: list of directive's JSON AST libgraphqlparser
    representation
    :type directives_ast: Optional[List[dict]]
    :param validators: the Validators object that will be used to validate these arguments
    :param path: a Path object that contains the current field path
    :type validators: Validators
    :type path: Path
    :return: a list of DirectiveNode instances equivalent to the JSON AST
    representation
    :rtype: List[DirectiveNode]
    """
    if directives_ast:
        directives = [
            _parse_directive(directive, validators, path)
            for directive in directives_ast
        ]

        validators.validate(
            rule="directives-are-unique-per-location",
            directives=directives,
            path=path,
        )

        return directives
    return []


def _parse_field(
    field_ast: dict, validators: "Validators", path: "Path"
) -> "FieldNode":
    """
    Creates and returns a FieldNode instance from a field's JSON AST
    libgraphqlparser representation.
    :param field_ast: field's JSON AST libgraphqlparser representation
    :type field_ast: dict
    :param validators: the Validators object that will be used to validate these arguments
    :param path: a Path object that contains the current field path
    :type validators: Validators
    :type path: Path
    :return: a FieldNode instance equivalent to the JSON AST representation
    :rtype: FieldNode
    """

    name = _parse_name(field_ast["name"])
    path = Path(prev=path, key=name.value)
    parent_type_name = validators.ctx["parent_type_name"]

    validators.ctx["parent_type_name"] = get_schema_field_type_name(
        parent_type_name, name.value, validators.schema
    )

    validators.ctx["in_directive"] = False
    validators.ctx["current_field_name"] = f"{parent_type_name}.{name}"

    field = FieldNode(
        alias=_parse_name(field_ast["alias"]) if field_ast["alias"] else None,
        name=name,
        arguments=_parse_arguments(field_ast["arguments"], validators, path),
        directives=_parse_directives(
            field_ast["directives"], validators, path
        ),
        selection_set=_parse_selection_set(
            field_ast["selectionSet"], validators, path
        ),
        location=_parse_location(field_ast["loc"]),
    )

    validators.ctx["parent_type_name"] = parent_type_name

    validators.validate(
        rule="directives-are-in-valid-locations", node=field, path=path
    )

    validators.validate(
        rule="field-selections-on-objects-interfaces-and-unions-types",
        field=field,
        path=path,
    )

    validators.validate(rule="leaf-field-selections", field=field, path=path)

    validators.validate(rule="values-of-correct-type", node=field, path=path)

    validators.validate(rule="argument-names", node=field, path=path)

    validators.validate(rule="required-arguments", node=field, path=path)

    return field


def _parse_fragment_spread(
    fragment_spread_ast: dict, validators: "Validators", path: "Path"
) -> "FragmentSpreadNode":
    """
    Creates and returns a FragmentSpreadNode instance from a fragment spread's
    JSON AST libgraphqlparser representation.
    :param fragment_spread_ast: fragment spread's JSON AST libgraphqlparser
    representation
    :type fragment_spread_ast: dict
    :param validators: the Validators object that will be used to validate these arguments
    :param path: a Path object that contains the current field path
    :type validators: Validators
    :type path: Path
    :return: a FragmentSpreadNode instance equivalent to the JSON AST
    representation
    :rtype: FragmentSpreadNode
    """
    fragment_spead = FragmentSpreadNode(
        name=_parse_name(fragment_spread_ast["name"]),
        directives=_parse_directives(
            fragment_spread_ast["directives"], validators, path
        ),
        location=_parse_location(fragment_spread_ast["loc"]),
    )

    validators.validate(
        rule="directives-are-in-valid-locations",
        node=fragment_spead,
        path=path,
    )

    validators.ctx.setdefault("fragment_spreads", []).append(fragment_spead)
    validators.ctx.setdefault("spreaded_in", {}).setdefault(
        validators.ctx["parent_type_name"], []
    ).append({"spread": fragment_spead, "path": path})

    if validators.ctx["in_operation"]:
        validators.ctx["per_operation"][
            validators.ctx["current_operation_name"]
        ].setdefault("spreads", []).append(fragment_spead)
    else:
        validators.ctx["per_fragment"][
            validators.ctx["current_fragment_name"]
        ].setdefault("spreads", []).append(fragment_spead)

    return fragment_spead


def _parse_inline_fragment(
    inline_fragment_ast: dict, validators: "Validators", path: "Path"
) -> "InlineFragmentNode":
    """
    Creates and returns an InlineFragmentNode instance from an inline spread's
    JSON AST libgraphqlparser representation.
    :param inline_fragment_ast: inline spread's JSON AST libgraphqlparser
    representation
    :type inline_fragment_ast: dict
    :param validators: the Validators object that will be used to validate these arguments
    :param path: a Path object that contains the current field path
    :type validators: Validators
    :type path: Path
    :return: an InlineFragmentNode instance equivalent to the JSON AST
    representation
    :rtype: InlineFragmentNode
    """

    parent_type_name = validators.ctx["parent_type_name"]

    type_cond = (
        _parse_named_type(inline_fragment_ast["typeCondition"])
        if inline_fragment_ast["typeCondition"]
        else None
    )
    if type_cond:
        validators.ctx["parent_type_name"] = type_cond.name.value

    inline_frag = InlineFragmentNode(
        directives=_parse_directives(
            inline_fragment_ast["directives"], validators, path
        ),
        type_condition=type_cond,
        selection_set=_parse_selection_set(
            inline_fragment_ast["selectionSet"], validators, path
        ),
        location=_parse_location(inline_fragment_ast["loc"]),
    )

    validators.validate(
        rule="directives-are-in-valid-locations", node=inline_frag, path=path
    )

    validators.validate(
        rule="fragment-spread-type-existence", fragment=inline_frag, path=path
    )
    validators.validate(
        rule="fragments-on-composite-types", fragment=inline_frag, path=path
    )

    validators.ctx.setdefault("inlined_in", {}).setdefault(
        validators.ctx["parent_type_name"], []
    ).append(inline_frag)
    validators.ctx["parent_type_name"] = parent_type_name

    return inline_frag


_SELECTION_PARSER_MAPPING = {
    "Field": _parse_field,
    "FragmentSpread": _parse_fragment_spread,
    "InlineFragment": _parse_inline_fragment,
}


def _parse_selection(
    selection_ast: dict, validators: "Validators", path: "Path"
) -> Union["FieldNode", "FragmentSpreadNode", "InlineFragmentNode"]:
    """
    Creates and returns a SelectionNode instance from a selection's JSON AST
    libgraphqlparser representation.
    :param selection_ast: selection's JSON AST libgraphqlparser representation
    :type selection_ast: dict
    :param validators: the Validators object that will be used to validate these arguments
    :param path: a Path object that contains the current field path
    :type validators: Validators
    :type path: Path
    :return: a SelectionNode instance equivalent to the JSON AST representation
    :rtype: Union[FieldNode, FragmentSpreadNode, InlineFragmentNode]
    """
    return _SELECTION_PARSER_MAPPING[selection_ast["kind"]](
        selection_ast, validators, path
    )


def _parse_selections(
    selections_ast: Optional[List[dict]], validators: Validators, path: Path
) -> List[Union["FieldNode", "FragmentSpreadNode", "InlineFragmentNode"]]:
    """
    Creates and returns a list of SelectionNode instances from a list of
    selection's JSON AST libgraphqlparser representation.
    :param selections_ast: list of selection's JSON AST libgraphqlparser
    representation
    :type selections_ast: Optional[List[dict]]
    :param validators: the Validators object that will be used to validate these arguments
    :param path: a Path object that contains the current field path
    :type validators: Validators
    :type path: Path
    :return: a list of SelectionNode instances equivalent to the JSON AST
    representation
    :rtype: List[Union[FieldNode, FragmentSpreadNode, InlineFragmentNode]]
    """

    if selections_ast:
        return [
            _parse_selection(selection, validators, path)
            for selection in selections_ast
        ]
    return []


def _parse_selection_set(
    selection_set_ast: Optional[dict], validators: Validators, path: Path
) -> Optional["SelectionSetNode"]:
    """
    Creates and returns a SelectionSetNode instance from a selection set's JSON
    AST libgraphqlparser representation.
    :param selection_set_ast: selection set's JSON AST libgraphqlparser
    representation
    :type selection_set_ast: Optional[dict]
    :param validators: the Validators object that will be used to validate these arguments
    :param path: a Path object that contains the current field path
    :type validators: Validators
    :type path: Path
    :return: a SelectionSetNode instance equivalent to the JSON AST
    representation
    :rtype: Optional[SelectionSetNode]
    """
    if selection_set_ast:
        return SelectionSetNode(
            selections=_parse_selections(
                selection_set_ast["selections"], validators, path
            ),
            location=_parse_location(selection_set_ast["loc"]),
        )
    return None


def _parse_fragment_definition(
    fragment_definition_ast: dict, validators: "Validators", path: Path
) -> "FragmentDefinitionNode":
    """
    Creates and returns a FragmentDefinitionNode instance from a fragment
    definition's JSON AST libgraphqlparser representation.
    :param fragment_definition_ast: fragment definition's JSON AST
    libgraphqlparser representation
    :type fragment_definition_ast: dict
    :param validators: the Validators object that will be used to validate these arguments
    :param path: a Path object that contains the current field path
    :type validators: Validators
    :type path: Path
    :return: a FragmentDefinitionNode instance equivalent to the JSON AST
    representation
    :rtype: FragmentDefinitionNode
    """

    parent_type_name = validators.ctx.get("parent_type_name")
    name = _parse_name(fragment_definition_ast["name"])
    type_cond = _parse_named_type(fragment_definition_ast["typeCondition"])
    validators.ctx["parent_type_name"] = type_cond.name.value
    validators.ctx["in_operation"] = False
    validators.ctx["current_fragment_name"] = name.value
    validators.ctx.setdefault("per_fragment", {}).setdefault(name.value, {})

    fragment = FragmentDefinitionNode(
        name=name,
        type_condition=type_cond,
        directives=_parse_directives(
            fragment_definition_ast["directives"], validators, path
        ),
        selection_set=_parse_selection_set(
            fragment_definition_ast["selectionSet"], validators, path
        ),
        location=_parse_location(fragment_definition_ast["loc"]),
    )

    validators.validate(
        rule="directives-are-in-valid-locations", node=fragment, path=path
    )

    validators.validate(
        rule="fragment-spread-type-existence", fragment=fragment, path=path
    )
    validators.validate(
        rule="fragments-on-composite-types", fragment=fragment, path=path
    )

    validators.ctx["parent_type_name"] = parent_type_name

    return fragment


def _parse_type(
    type_ast: dict,
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
    variable_definition_ast: dict, validators: Validators, path: Path
) -> "VariableDefinitionNode":
    """
    Creates and returns a VariableDefinitionNode instance from a variable
    definition's JSON AST libgraphqlparser representation.
    :param variable_definition_ast: variable definition's JSON AST
    libgraphqlparser representation
    :type variable_definition_ast: dict
    :param validators: the Validators object that will be used to validate these arguments
    :param path: a Path object that contains the current field path
    :type validators: Validators
    :type path: Path
    :return: a VariableDefinitionNode instance equivalent to the JSON AST
    representation
    :rtype: VariableDefinitionNode
    """
    variable = VariableDefinitionNode(
        variable=_parse_variable(
            variable_definition_ast["variable"], validators
        ),
        type=_parse_type(variable_definition_ast["type"]),
        default_value=_parse_value(
            variable_definition_ast["defaultValue"], validators, path
        ),
        location=_parse_location(variable_definition_ast["loc"]),
    )

    validators.validate(
        rule="variables-are-input-types", variable=variable, path=path
    )

    return variable


def _parse_variable_definitions(
    variable_definitions_ast: Optional[List[dict]],
    validators: Validators,
    path: Path,
) -> List["VariableDefinitionNode"]:
    """
    Creates and returns a list of VariableDefinitionNode instances from a list
    of variable definition's JSON AST libgraphqlparser representation.
    :param variable_definitions_ast: list of variable definition's JSON AST
    libgraphqlparser representation
    :type variable_definitions_ast: Optional[List[dict]]
    :param validators: the Validators object that will be used to validate these arguments
    :param path: a Path object that contains the current field path
    :type validators: Validators
    :type path: Path
    :return: a list of VariableDefinitionNode instances equivalent to the JSON
    AST representation
    :rtype: List[VariableDefinitionNode]
    """
    if variable_definitions_ast:
        validators.ctx["in_variable_definitions"] = True
        variables = [
            _parse_variable_definition(variable_definition, validators, path)
            for variable_definition in variable_definitions_ast
        ]
        validators.ctx["in_variable_definitions"] = False

        validators.validate(
            rule="variable-uniqueness",
            variable_definitions=variables,
            path=path,
        )

        return variables
    return []


def _get_operation_type_name(operation_type, schema):
    return getattr(schema, f"{operation_type.lower()}_operation_name")


def _parse_operation_definition(
    operation_definition_ast: dict, validators: "Validators", path: Path
) -> "OperationDefinitionNode":
    """
    Creates and returns an OperationDefinitionNode instance from an operation
    definition's JSON AST libgraphqlparser representation.
    :param operation_definition_ast: operation definition's JSON AST
    libgraphqlparser representation
    :type operation_definition_ast: dict
    :param validators: the Validators object that will be used to validate these arguments
    :param path: a Path object that contains the current field path
    :type validators: Validators
    :type path: Path
    :return: an OperationDefinitionNode instance equivalent to the JSON AST
    representation
    :rtype: OperationDefinitionNode
    """
    operation_type = operation_definition_ast["operation"]
    name = (
        _parse_name(operation_definition_ast["name"])
        if operation_definition_ast["name"]
        else None
    )

    validators.ctx["parent_type_name"] = _get_operation_type_name(
        operation_type, validators.schema
    )
    validators.ctx["in_operation"] = True
    validators.ctx["current_operation_name"] = name.value if name else "None"
    validators.ctx.setdefault("per_operation", {}).setdefault(
        name.value if name else "None", {}
    )

    operation = OperationDefinitionNode(
        operation_type=operation_type,
        name=name,
        variable_definitions=_parse_variable_definitions(
            operation_definition_ast["variableDefinitions"], validators, path
        ),
        directives=_parse_directives(
            operation_definition_ast["directives"], validators, path
        ),
        selection_set=_parse_selection_set(
            operation_definition_ast["selectionSet"], validators, path
        ),
        location=_parse_location(operation_definition_ast["loc"]),
    )

    validators.validate(
        rule="directives-are-in-valid-locations", node=operation, path=path
    )

    return operation


_DEFINITION_PARSER_MAPPING = {
    "FragmentDefinition": _parse_fragment_definition,
    "OperationDefinition": _parse_operation_definition,
}


def _parse_definition(
    definition_ast: dict, validators: "Validators", path: Path
) -> Union["FragmentDefinitionNode", "OperationDefinitionNode"]:
    """
    Creates and returns a DefinitionNode instance from a definition's JSON AST
    libgraphqlparser representation.
    :param definition_ast: definition's JSON AST libgraphqlparser
    representation
    :type definition_ast: dict
    :param validators: the Validators object that will be used to validate these arguments
    :param path: a Path object that contains the current field path
    :type validators: Validators
    :type path: Path
    :return: a DefinitionNode instance equivalent to the JSON AST
    representation
    :rtype: Union[FragmentDefinitionNode, OperationDefinitionNode]
    """
    return _DEFINITION_PARSER_MAPPING[definition_ast["kind"]](
        definition_ast, validators, path
    )


def _parse_definitions(
    definitions_ast: Optional[List[dict]],
    validators: Validators,
    path: Path = None,
) -> List[Union["FragmentDefinitionNode", "OperationDefinitionNode"]]:
    """
    Creates and returns a list of DefinitionNode instances from a list of
    definition's JSON AST libgraphqlparser representation.
    :param definitions_ast: list of definition's JSON AST libgraphqlparser
    representation
    :type definitions_ast: Optional[List[dict]]
    :param validators: the Validators object that will be used to validate these arguments
    :param path: a Path object that contains the current field path
    :type validators: Validators
    :type path: Path
    :return: a list of DefinitionNode instances equivalent to the JSON AST
    representation
    :rtype: List[Union[FragmentDefinitionNode, OperationDefinitionNode]]
    """

    parsed_def = {"FragmentDefinition": [], "OperationDefinition": []}

    if definitions_ast:
        for definition in definitions_ast:
            parsed_def[definition["kind"]].append(
                _parse_definition(definition, validators, path)
            )

    validators.validate(
        rule="fragment-spreads-must-not-form-cycles",
        fragments=parsed_def["FragmentDefinition"],
        path=None,
    )

    validators.validate(
        rule="operation-name-uniqueness",
        operations=parsed_def["OperationDefinition"],
        path=path,
    )
    validators.validate(
        rule="lone-anonymous-operation",
        operations=parsed_def["OperationDefinition"],
        path=path,
    )

    validators.validate(
        rule="single-root-field", definitions=parsed_def, path=path
    )

    validators.validate(
        rule="fragment-name-uniqueness",
        fragments=parsed_def["FragmentDefinition"],
        path=path,
    )

    validators.validate(
        rule="fragment-spread-target-defined",
        fragments=parsed_def["FragmentDefinition"],
        path=path,
    )

    validators.validate(
        rule="fragment-must-be-used",
        fragments=parsed_def["FragmentDefinition"],
        path=path,
    )

    validators.validate(
        rule="fragment-spread-is-possible",
        fragments=parsed_def["FragmentDefinition"],
        path=path,
    )

    validators.validate(
        rule="all-variable-uses-defined",
        operations=parsed_def["OperationDefinition"],
        path=path,
    )

    validators.validate(
        rule="all-variables-used",
        operations=parsed_def["OperationDefinition"],
        path=path,
    )

    validators.validate(
        rule="all-variable-usages-are-allowed",
        operations=parsed_def["OperationDefinition"],
        path=path,
    )

    return parsed_def["FragmentDefinition"] + parsed_def["OperationDefinition"]


def document_from_ast_json(
    document_ast: dict, query: Union[str, bytes], schema: "GraphQLSchema"
) -> "DocumentNode":
    """
    Creates and returns a DocumentNode instance from a document's JSON AST
    libgraphqlparser representation.
    :param document_ast: document's JSON AST libgraphqlparser representation
    :param query: query to parse and transform into a DocumentNode
    :param schema: the GraphQLSchema instance linked to the engine
    :type document_ast: dict
    :type query: Union[str, bytes]
    :type schema: GraphQLSchema
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
    >>> },
    >>> '''
    >>> {
    >>>   hello
    >>> }
    >>> ''')
    """

    validators = Validators(schema, RULE_SET)

    definitions = _parse_definitions(document_ast["definitions"], validators)

    validators.validate(
        rule="executable-definitions", definitions=definitions, path=None
    )

    return DocumentNode(
        definitions=definitions,
        validators=validators,
        hash_id=hash(query),
        location=_parse_location(document_ast["loc"]),
    )
