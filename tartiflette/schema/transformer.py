from functools import partial
from typing import Any, Dict, List, Optional, Union


from tartiflette.language.ast import ListTypeNode, NonNullTypeNode, ObjectTypeExtensionNode
from tartiflette.language.parsers.lark import parse_to_document
from tartiflette.schema.schema import GraphQLSchema
from tartiflette.types.argument import GraphQLArgument
from tartiflette.types.directive import GraphQLDirective
from tartiflette.types.enum import GraphQLEnumType, GraphQLEnumValue
from tartiflette.types.field import GraphQLField
from tartiflette.types.input_field import GraphQLInputField
from tartiflette.types.input_object import GraphQLInputObjectType
from tartiflette.types.interface import GraphQLInterfaceType
from tartiflette.types.list import GraphQLList
from tartiflette.types.non_null import GraphQLNonNull
from tartiflette.types.object import GraphQLObjectType
from tartiflette.types.scalar import GraphQLScalarType
from tartiflette.types.union import GraphQLUnionType

__all__ = ("schema_from_sdl",)


def parse_name(
    name_node: "NameNode", schema: "GraphQLSchema"
) -> Optional[str]:
    """
    Returns the value of an AST name node.
    :param name_node: AST name node to treat
    :param schema: the GraphQLSchema instance linked to the engine
    :type name_node: NameNode
    :type schema: GraphQLSchema
    :return: the name value
    :rtype: Optional[str]
    """
    # pylint: disable=unused-argument
    return name_node.value if name_node else None


def parse_named_type(
    named_type_node: "NamedTypeNode", schema: "GraphQLSchema"
) -> Optional[str]:
    """
    Returns the value of the name of an AST named type node.
    :param named_type_node: AST named type node to treat
    :param schema: the GraphQLSchema instance linked to the engine
    :type named_type_node: NamedTypeNode
    :type schema: GraphQLSchema
    :return: the name value
    :rtype: Optional[str]
    """
    if not named_type_node:
        return None
    return parse_name(named_type_node.name, schema)


def parse_boolean_value(
    boolean_value_node: "BooleanValueNode", schema: "GraphQLSchema"
) -> Optional[bool]:
    """
    Returns the value of an AST boolean value node.
    :param boolean_value_node: AST boolean value node to treat
    :param schema: the GraphQLSchema instance linked to the engine
    :type boolean_value_node: BooleanValueNode
    :type schema: GraphQLSchema
    :return: the boolean value
    :rtype: Optional[bool]
    """
    # pylint: disable=unused-argument
    return boolean_value_node.value if boolean_value_node else None


def parse_enum_value(
    enum_value_node: "EnumValueNode", schema: "GraphQLSchema"
) -> Optional[str]:
    """
    Returns the value of an AST enum value node.
    :param enum_value_node: AST enum value node to treat
    :param schema: the GraphQLSchema instance linked to the engine
    :type enum_value_node: EnumValueNode
    :type schema: GraphQLSchema
    :return: the enum value
    :rtype: Optional[str]
    """
    # pylint: disable=unused-argument
    return enum_value_node.value if enum_value_node else None


def parse_float_value(
    float_value_node: "FloatValueNode", schema: "GraphQLSchema"
) -> Optional[float]:
    """
    Returns the value of an AST float value node.
    :param float_value_node: AST float value node to treat
    :param schema: the GraphQLSchema instance linked to the engine
    :type float_value_node: FloatValueNode
    :type schema: GraphQLSchema
    :return: the float value
    :rtype: Optional[float]
    """
    # pylint: disable=unused-argument
    return float_value_node.value if float_value_node else None


def parse_int_value(
    int_value_node: "IntValueNode", schema: "GraphQLSchema"
) -> Optional[int]:
    """
    Returns the value of an AST int value node.
    :param int_value_node: AST int value node to treat
    :param schema: the GraphQLSchema instance linked to the engine
    :type int_value_node: IntValueNode
    :type schema: GraphQLSchema
    :return: the int value
    :rtype: Optional[int]
    """
    # pylint: disable=unused-argument
    return int_value_node.value if int_value_node else None


def parse_string_value(
    string_value_node: "StringValueNode", schema: "GraphQLSchema"
) -> Optional[str]:
    """
    Returns the value of an AST string value node.
    :param string_value_node: AST string value node to treat
    :param schema: the GraphQLSchema instance linked to the engine
    :type string_value_node: StringValueNode
    :type schema: GraphQLSchema
    :return: the string value
    :rtype: Optional[str]
    """
    # pylint: disable=unused-argument
    return string_value_node.value if string_value_node else None


def parse_list_value(
    list_value_node: "ListValueNode", schema: "GraphQLSchema"
) -> Optional[List[Any]]:
    """
    Returns the value of an AST list value node.
    :param list_value_node: AST list value node to treat
    :param schema: the GraphQLSchema instance linked to the engine
    :type list_value_node: ListValueNode
    :type schema: GraphQLSchema
    :return: the list value
    :rtype: Optional[List[Any]]
    """
    if not list_value_node:
        return None
    return [parse_value(value, schema) for value in list_value_node.values]


def parse_null_value(
    null_value_node: "NullValueNode", schema: "GraphQLSchema"
) -> None:
    """
    Returns the value of an AST null value node.
    :param null_value_node: AST null value node to treat
    :param schema: the GraphQLSchema instance linked to the engine
    :type null_value_node: NullValueNode
    :type schema: GraphQLSchema
    """
    # pylint: disable=unused-argument
    return None


def parse_object_value(
    object_value_node: "ObjectValueNode", schema: "GraphQLSchema"
) -> Optional[Dict[str, Any]]:
    """
    Returns the value of an AST object value node
    :param object_value_node: AST object value node to treat
    :param schema: the GraphQLSchema instance linked to the engine
    :type object_value_node: ObjectValueNode
    :type schema: GraphQLSchema
    :return: the object value
    :rtype: Optional[Dict[str, Any]]
    """
    if not object_value_node:
        return None
    return {
        parse_name(field_node.name, schema): parse_value(
            field_node.value, schema
        )
        for field_node in object_value_node.fields
    }


_VALUE_PARSER_MAPPING = {
    "BooleanValueNode": parse_boolean_value,
    "EnumValueNode": parse_enum_value,
    "FloatValueNode": parse_float_value,
    "IntValueNode": parse_int_value,
    "ListValueNode": parse_list_value,
    "NullValueNode": parse_null_value,
    "ObjectValueNode": parse_object_value,
    "StringValueNode": parse_string_value,
}


def parse_value(
    value_node: "ValueNode", schema: "GraphQLSchema"
) -> Optional[Any]:
    """
    Returns the value of an AST value node
    :param value_node: AST value node to treat
    :param schema: the GraphQLSchema instance linked to the engine
    :type value_node: ValueNode
    :type schema: GraphQLSchema
    :return: the value
    :rtype: Optional[Any]
    """
    if not value_node:
        return None
    return _VALUE_PARSER_MAPPING[value_node.__class__.__name__](
        value_node, schema
    )


def parse_input_value_definition(
    input_value_definition_node: "InputValueDefinitionNode",
    schema: "GraphQLSchema",
    as_argument_definition: bool = False,
) -> Optional[Union["GraphQLArgument", "GraphQLInputField"]]:
    """
    Computes an AST input value definition node into a GraphQLArgument or
    GraphQLInputField instance.
    :param input_value_definition_node: AST input value definition node to
    treat
    :param schema: the GraphQLSchema instance linked to the engine
    :param as_argument_definition: determines whether or not the return type
    should be a GraphQLArgument or a GraphQLInputField
    :type input_value_definition_node: InputValueDefinitionNode
    :type schema: GraphQLSchema
    :type as_argument_definition: bool
    :return: the computed GraphQLArgument or GraphQLInputField instance
    :rtype: Optional[Union[GraphQLArgument, GraphQLInputField]]
    """
    if not input_value_definition_node:
        return None

    init_kwargs = {
        "name": parse_name(input_value_definition_node.name, schema),
        "description": parse_name(
            input_value_definition_node.description, schema
        ),
        "gql_type": parse_type(input_value_definition_node.type, schema),
        "default_value": input_value_definition_node.default_value,
        "directives": input_value_definition_node.directives,
    }

    if not as_argument_definition:
        return GraphQLInputField(**init_kwargs)
    return GraphQLArgument(
        **init_kwargs, definition=input_value_definition_node
    )


def parse_arguments_definition(
    argument_definitions_node: List["InputValueDefinitionNode"],
    schema: "GraphQLSchema",
) -> Optional[Dict[str, "GraphQLArgument"]]:
    """
    Returns a dictionary of computed GraphQLArgument.
    :param argument_definitions_node: list of AST input value definition
    node to treat
    :param schema: the GraphQLSchema instance linked to the engine
    :type argument_definitions_node: List[InputValueDefinitionNode]
    :type schema: GraphQLSchema
    :return: dictionary of computed GraphQLArgument
    :rtype: Optional[Dict[str, GraphQLArgument]]
    """
    if not argument_definitions_node:
        return None

    computed_arguments = {}
    for input_value_definition_node in argument_definitions_node:
        computed_argument = parse_input_value_definition(
            input_value_definition_node, schema, as_argument_definition=True
        )
        computed_arguments[computed_argument.name] = computed_argument
    return computed_arguments


def parse_operation_type_definition(
    operation_type_definition_node: "OperationTypeDefinitionNode",
    schema: "GraphQLSchema",
) -> None:
    """
    Computes the new operation type definition name and update it in the
    schema.
    :param operation_type_definition_node: AST operation type definition node
    to treat
    :param schema: the GraphQLSchema instance linked to the engine
    :type operation_type_definition_node: OperationTypeDefinitionNode
    :type schema: GraphQLSchema
    """
    if not operation_type_definition_node:
        return
    setattr(
        schema,
        f"{operation_type_definition_node.operation_type}_operation_name",
        parse_named_type(operation_type_definition_node.type, schema),
    )


def parse_operation_type_definitions(
    operation_type_definitions_node: List["OperationTypeDefinitionNode"],
    schema: "GraphQLSchema",
) -> None:
    """
    Parses all AST operation type definition node in order to update the
    schema.
    :param operation_type_definitions_node: list of AST operation type
    definition node to treat
    :param schema: the GraphQLSchema instance linked to the engine
    :type operation_type_definitions_node: List[OperationTypeDefinitionNode]
    :type schema: GraphQLSchema
    """
    if not operation_type_definitions_node:
        return

    for operation_type_definition_node in operation_type_definitions_node:
        parse_operation_type_definition(operation_type_definition_node, schema)


def parse_schema_definition(
    schema_definition_node: "SchemaDefinitionNode", schema: "GraphQLSchema"
) -> None:
    """
    Parses the AST operation type definition nodes from the AST schema
    definition node.
    :param schema_definition_node: AST schema definition node to treat
    :param schema: the GraphQLSchema instance linked to the engine
    :type schema_definition_node: SchemaDefinitionNode
    :type schema: GraphQLSchema
    """
    if not schema_definition_node:
        return
    parse_operation_type_definitions(
        schema_definition_node.operation_type_definitions, schema
    )


def parse_scalar_type_definition(
    scalar_type_definition_node: "ScalarTypeDefinitionNode",
    schema: "GraphQLSchema",
) -> Optional["GraphQLScalarType"]:
    """
    Computes an AST scalar type definition node into a GraphQLScalarType
    instance.
    :param scalar_type_definition_node: AST scalar type definition node to
    treat
    :param schema: the GraphQLSchema instance linked to the engine
    :type scalar_type_definition_node: ScalarTypeDefinitionNode
    :type schema: GraphQLSchema
    :return: the computed GraphQLScalarType instance
    :rtype: Optional[GraphQLScalarType]
    """
    if not scalar_type_definition_node:
        return None

    scalar_type = GraphQLScalarType(
        name=parse_name(scalar_type_definition_node.name, schema),
        description=parse_name(
            scalar_type_definition_node.description, schema
        ),
        directives=scalar_type_definition_node.directives,
    )
    schema.add_scalar_definition(scalar_type)
    return scalar_type


def parse_implements_interfaces(
    interfaces_node: List["NamedTypeNode"], schema: "GraphQLSchema"
) -> Optional[List[str]]:
    """
    Returns the list of implemented interface names.
    :param interfaces_node: list of AST named type node to treat
    :param schema: the GraphQLSchema instance linked to the engine
    :type interfaces_node: List[NamedTypeNode]
    :type schema: GraphQLSchema
    :return: the list of implemented interface names
    :rtype: Optional[List[str]]
    """
    if not interfaces_node:
        return []

    return [
        parse_named_type(interface_node, schema)
        for interface_node in interfaces_node
    ]


def parse_object_type_definition(
    object_type_definition_node: "ObjectTypeDefinitionNode",
    schema: "GraphQLSchema",
) -> Optional["GraphQLObjectType"]:
    """
    Computes an AST object type definition node into a GraphQLObjectType
    instance.
    :param object_type_definition_node: AST object type definition node to
    treat
    :param schema: the GraphQLSchema instance linked to the engine
    :type object_type_definition_node: ObjectTypeDefinitionNode
    :type schema: GraphQLSchema
    :return: the GraphQLObjectType instance
    :rtype: Optional[GraphQLObjectType]
    """
    if not object_type_definition_node:
        return None
    name = parse_name(object_type_definition_node.name, schema)
    if schema.has_type(name):
        return parse_object_type_extension(object_type_definition_node, schema)
    object_type = GraphQLObjectType(
        name=name,
        description=parse_name(
            object_type_definition_node.description, schema
        ),
        interfaces=parse_implements_interfaces(
            object_type_definition_node.interfaces, schema
        ) or [],
        fields=parse_fields_definition(
            object_type_definition_node.fields, schema
        ),
        directives=object_type_definition_node.directives,
    )
    schema.add_type_definition(object_type)
    return object_type


def parse_object_type_extension(
    object_type_extension: ObjectTypeExtensionNode,
    schema: "GraphQLSchema",
) -> Optional[GraphQLObjectType]:
    if not object_type_extension:
        return None
    name = parse_name(object_type_extension.name, schema)
    if not schema.has_type(name):
        return parse_object_type_definition(object_type_extension, schema)
    original_object_type: ObjectTypeExtensionNode = schema.type_definitions[name]
    object_type = GraphQLObjectType(
        name=name,
        description=original_object_type.description or parse_name(
            object_type_extension.description, schema
        ),
        interfaces=(original_object_type.interfaces or []) + (parse_implements_interfaces(
            object_type_extension.interfaces, schema
        ) or []),
        fields={
            **original_object_type.implemented_fields,
            **parse_fields_definition(object_type_extension.fields, schema)
        },
        directives=original_object_type.directives + object_type_extension.directives,
    )
    del schema.type_definitions[name]
    schema.add_type_definition(object_type)
    return object_type


def parse_field_definition(
    field_definition_node: "FieldDefinitionNode", schema: "GraphQLSchema"
) -> Optional["GraphQLField"]:
    """
    Computes an AST field definition node into a GraphQLField instance.
    :param field_definition_node: AST field definition node to treat
    :param schema: the GraphQLSchema instance linked to the engine
    :type field_definition_node: FieldDefinitionNode
    :type schema: GraphQLSchema
    :return: the GraphQLField instance
    :rtype: Optional[GraphQLField]
    """
    if not field_definition_node:
        return None

    return GraphQLField(
        name=parse_name(field_definition_node.name, schema),
        description=parse_name(field_definition_node.description, schema),
        gql_type=parse_type(field_definition_node.type, schema),
        arguments=parse_arguments_definition(
            field_definition_node.arguments, schema
        ),
        directives=field_definition_node.directives,
    )


def parse_fields_definition(
    fields_definition_node: List["FieldDefinitionNode"],
    schema: "GraphQLSchema",
) -> Optional[Dict[str, "GraphQLField"]]:
    """
    Returns a dictionary of computed GraphQLField.
    :param fields_definition_node: list of AST field definition node to treat
    :param schema: the GraphQLSchema instance linked to the engine
    :type fields_definition_node: List[FieldDefinitionNode]
    :type schema: GraphQLSchema
    :return: dictionary of computed GraphQLField
    :rtype: Optional[Dict[str, GraphQLField]]
    """
    if not fields_definition_node:
        return None

    computed_fields = {}
    for field_definition_node in fields_definition_node:
        computed_field = parse_field_definition(field_definition_node, schema)
        computed_fields[computed_field.name] = computed_field
    return computed_fields


def parse_interface_type_definition(
    interface_type_definition_node: "InterfaceTypeDefinitionNode",
    schema: "GraphQLSchema",
) -> Optional["GraphQLInterfaceType"]:
    """
    Computes an AST interface type definition node into a GraphQLInterfaceType
    instance.
    :param interface_type_definition_node: AST interface type definition node
    to treat
    :param schema: the GraphQLSchema instance linked to the engine
    :type interface_type_definition_node: InterfaceTypeDefinitionNode
    :type schema: GraphQLSchema
    :return: the GraphQLInterfaceType instance
    :rtype: Optional[GraphQLInterfaceType]
    """
    if not interface_type_definition_node:
        return None

    interface_type = GraphQLInterfaceType(
        name=parse_name(interface_type_definition_node.name, schema),
        description=parse_name(
            interface_type_definition_node.description, schema
        ),
        fields=parse_fields_definition(
            interface_type_definition_node.fields, schema
        ),
        directives=interface_type_definition_node.directives,
    )
    schema.add_type_definition(interface_type)
    return interface_type


def parse_union_member_types(
    types_node: List["NamedTypeNode"], schema: "GraphQLSchema"
) -> Optional[List[str]]:
    """
    Returns the list of union member type name.
    :param types_node: list of AST named type node to treat
    :param schema: the GraphQLSchema instance linked to the engine
    :type types_node: List[NamedTypeNode]
    :type schema: GraphQLSchema
    :return: the list of union member type name
    :rtype: Optional[List[str]]
    """
    if not types_node:
        return None

    return [
        parse_named_type(union_member_type_node, schema)
        for union_member_type_node in types_node
    ]


def parse_union_type_definition(
    union_type_definition_node: "UnionTypeDefinitionNode",
    schema: "GraphQLSchema",
) -> Optional["GraphQLUnionType"]:
    """
    Computes an AST union type definition node into a GraphQLUnionType
    instance.
    :param union_type_definition_node: AST union type definition node to treat
    :param schema: the GraphQLSchema instance linked to the engine
    :type union_type_definition_node: UnionTypeDefinitionNode
    :type schema: GraphQLSchema
    :return: the GraphQLUnionType instance
    :rtype: Optional[GraphQLUnionType]
    """
    if not union_type_definition_node:
        return None

    union_type = GraphQLUnionType(
        name=parse_name(union_type_definition_node.name, schema),
        description=parse_name(union_type_definition_node.description, schema),
        types=parse_union_member_types(
            union_type_definition_node.types, schema
        ),
        directives=union_type_definition_node.directives,
    )
    schema.add_type_definition(union_type)
    return union_type


def parse_enum_value_definition(
    enum_value_definition_node: "EnumValueDefinitionNode",
    schema: "GraphQLSchema",
) -> Optional["GraphQLEnumValue"]:
    """
    Computes an AST enum value definition node into a GraphQLEnumValue
    instance.
    :param enum_value_definition_node: AST enum value definition node to treat
    :param schema: the GraphQLSchema instance linked to the engine
    :type enum_value_definition_node: EnumValueDefinitionNode
    :type schema: GraphQLSchema
    :return: the GraphQLEnumValue instance
    :rtype: Optional[GraphQLEnumValue]
    """
    if not enum_value_definition_node:
        return None
    return GraphQLEnumValue(
        value=parse_name(enum_value_definition_node.name, schema),
        description=parse_name(enum_value_definition_node.description, schema),
        directives=enum_value_definition_node.directives,
    )


def parse_enum_values_definition(
    enum_values_definition_node: List["EnumValueDefinitionNode"],
    schema: "GraphQLSchema",
) -> Optional[List["GraphQLEnumValue"]]:
    """
    Returns a list of computed GraphQLEnumValue.
    :param enum_values_definition_node: list of AST enum value definition node
    to treat
    :param schema: the GraphQLSchema instance linked to the engine
    :type enum_values_definition_node: List[EnumValueDefinitionNode]
    :type schema: GraphQLSchema
    :return: list of computed GraphQLEnumValue
    :rtype: Optional[List[GraphQLEnumValue]]
    """
    if not enum_values_definition_node:
        return None

    return [
        parse_enum_value_definition(enum_value_definition_node, schema)
        for enum_value_definition_node in enum_values_definition_node
    ]


def parse_enum_type_definition(
    enum_type_definition_node: "EnumTypeDefinitionNode",
    schema: "GraphQLSchema",
) -> Optional["GraphQLEnumType"]:
    """
    Computes an AST enum type definition node into a GraphQLEnumType instance.
    :param enum_type_definition_node: AST enum type definition node to treat
    :param schema: the GraphQLSchema instance linked to the engine
    :type enum_type_definition_node: EnumTypeDefinitionNode
    :type schema: GraphQLSchema
    :return: the GraphQLEnumType instance
    :rtype: Optional[GraphQLEnumType]
    """
    if not enum_type_definition_node:
        return None

    enum_type = GraphQLEnumType(
        name=parse_name(enum_type_definition_node.name, schema),
        description=parse_name(enum_type_definition_node.description, schema),
        values=parse_enum_values_definition(
            enum_type_definition_node.values, schema
        ),
        directives=enum_type_definition_node.directives,
    )
    schema.add_enum_definition(enum_type)
    return enum_type


def parse_input_fields_definition(
    input_fields_definition_node: List["InputValueDefinitionNode"],
    schema: "GraphQLSchema",
) -> Optional[Dict[str, "GraphQLInputField"]]:
    """
    Returns a dictionary of computed GraphQLInputField.
    :param input_fields_definition_node: list of AST input value definition
    node to treat
    :param schema: the GraphQLSchema instance linked to the engine
    :type input_fields_definition_node: List[InputValueDefinitionNode]
    :type schema: GraphQLSchema
    :return: dictionary of computed GraphQLInputField
    :rtype: Optional[Dict[str, GraphQLInputField]]
    """
    if not input_fields_definition_node:
        return None

    computed_input_fields = {}
    for input_field_definition_node in input_fields_definition_node:
        input_value_definition = parse_input_value_definition(
            input_field_definition_node, schema
        )
        computed_input_fields[
            input_value_definition.name
        ] = input_value_definition
    return computed_input_fields


def parse_input_object_type_definition(
    input_object_type_definition_node: "InputObjectTypeDefinitionNode",
    schema: "GraphQLSchema",
) -> Optional["GraphQLInputObjectType"]:
    """
    Computes an AST input object type definition node into a
    GraphQLInputObjectType instance.
    :param input_object_type_definition_node: AST input object type
    definition node to treat
    :param schema: the GraphQLSchema instance linked to the engine
    :type input_object_type_definition_node: InputObjectTypeDefinitionNode
    :type schema: GraphQLSchema
    :return: the GraphQLInputObjectType instance
    :rtype: Optional[GraphQLInputObjectType]
    """
    if not input_object_type_definition_node:
        return None

    input_object_type = GraphQLInputObjectType(
        name=parse_name(input_object_type_definition_node.name, schema),
        description=parse_name(
            input_object_type_definition_node.description, schema
        ),
        fields=parse_input_fields_definition(
            input_object_type_definition_node.fields, schema
        ),
        directives=input_object_type_definition_node.directives,
    )
    schema.add_type_definition(input_object_type)
    return input_object_type


def parse_type(
    type_node: "TypeNode", schema: "GraphQLSchema"
) -> Union["GraphQLList", "GraphQLNonNull", str]:
    """
    Computes an AST type node into its GraphQL representation.
    :param type_node: AST type node to treat
    :param schema: the GraphQLSchema instance linked to the engine
    :type type_node: TypeNode
    :type schema: GraphQLSchema
    :return: the GraphQL representation of the type node
    :rtype: Union[GraphQLList, GraphQLNonNull, str]
    """
    inner_type_node = type_node
    type_wrappers = []
    while isinstance(inner_type_node, (NonNullTypeNode, ListTypeNode)):
        if isinstance(inner_type_node, ListTypeNode):
            type_wrappers.append(partial(GraphQLList, schema=schema))
        elif isinstance(inner_type_node, NonNullTypeNode):
            type_wrappers.append(
                partial(partial(GraphQLNonNull, schema=schema))
            )
        inner_type_node = inner_type_node.type

    graphql_type = parse_named_type(inner_type_node, schema)
    for type_wrapper in reversed(type_wrappers):
        graphql_type = type_wrapper(gql_type=graphql_type)
    return graphql_type


def parse_directive_definition(
    directive_definition_node: "DirectiveDefinitionNode",
    schema: "GraphQLSchema",
) -> Optional["GraphQLDirective"]:
    """
    Computes an AST directive definition node into a GraphQLDirective instance.
    :param directive_definition_node: AST directive definition node to treat
    :param schema: the GraphQLSchema instance linked to the engine
    :type directive_definition_node: DirectiveDefinitionNode
    :type schema: GraphQLSchema
    :return: the GraphQLDirective instance
    :rtype: Optional[GraphQLDirective]
    """
    if not directive_definition_node:
        return None
    directive = GraphQLDirective(
        name=parse_name(directive_definition_node.name, schema),
        description=parse_name(directive_definition_node.description, schema),
        locations=[
            location.value for location in directive_definition_node.locations
        ],
        arguments=parse_arguments_definition(
            directive_definition_node.arguments, schema
        ),
    )
    schema.add_directive_definition(directive)
    return directive


_DEFINITION_PARSER_MAPPING = {
    "SchemaDefinitionNode": parse_schema_definition,
    "ScalarTypeDefinitionNode": parse_scalar_type_definition,
    "ObjectTypeDefinitionNode": parse_object_type_definition,
    "InterfaceTypeDefinitionNode": parse_interface_type_definition,
    "UnionTypeDefinitionNode": parse_union_type_definition,
    "EnumTypeDefinitionNode": parse_enum_type_definition,
    "InputObjectTypeDefinitionNode": parse_input_object_type_definition,
    "DirectiveDefinitionNode": parse_directive_definition,
    "ObjectTypeExtensionNode": parse_object_type_extension
    # TODO high priority InputObjectExtensionNode, EnumTypeExtensionNode, UnionTypeExtensionNode, 
    # TODO InterfaceTypeExtensionNode, , SchemaExtensionNode, 
}


def parse_definition(
    definition_node: "DefinitionNode", schema: "GraphQLSchema"
) -> Any:
    """
    Attempts to parses and computes an AST definition node.
    :param definition_node: AST definition node to treat
    :param schema: the GraphQLSchema instance linked to the engine
    :type definition_node: DefinitionNode
    :type schema: GraphQLSchema
    :return: the computed result
    :rtype: Any
    """
    definition_parser = _DEFINITION_PARSER_MAPPING.get(
        definition_node.__class__.__name__
    )
    if definition_parser is None:
        return None
    return definition_parser(definition_node, schema)


def schema_from_document(
    document_node: "DocumentNode", schema_name: str
) -> "GraphQLSchema":
    """
    Parses all AST definition node from the AST document node in order to build
    the GraphQLSchema.
    :param document_node: AST document node to treat
    :param schema_name: name of the schema to build
    :type document_node: DocumentNode
    :type schema_name: str
    :return: build GraphQLSchema
    :rtype: GraphQLSchema
    """
    schema = GraphQLSchema(name=schema_name)
    for definition_node in document_node.definitions:
        parse_definition(definition_node, schema)
    return schema


def schema_from_sdl(
    sdl: Union[str, bytes], schema_name: str
) -> "GraphQLSchema":
    """
    Parse the SDL into an AST document node before validating it and building a
    GraphQL Schema instance upon it.
    :param sdl: sdl to parse
    :param schema_name: name of the schema to build
    :type sdl: Union[str, bytes]
    :type schema_name: str
    :return: build GraphQLSchema
    :rtype: GraphQLSchema
    """
    document_node = parse_to_document(sdl)
    # TODO: implements the `validate_document` function
    # errors = validate_document(document)
    # if errors:
    #     raise Something(errors)
    return schema_from_document(document_node, schema_name=schema_name)
