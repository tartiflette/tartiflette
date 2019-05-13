from collections import namedtuple
from typing import List

from lark import Tree, v_args
from lark.visitors import Transformer_InPlace

from tartiflette.types.argument import GraphQLArgument
from tartiflette.types.directive import GraphQLDirective
from tartiflette.types.enum import GraphQLEnumType, GraphQLEnumValue
from tartiflette.types.exceptions.tartiflette import (
    InvalidSDL,
    UnexpectedASTNode,
)
from tartiflette.types.field import GraphQLField
from tartiflette.types.input_object import GraphQLInputObjectType
from tartiflette.types.interface import GraphQLInterfaceType
from tartiflette.types.list import GraphQLList
from tartiflette.types.non_null import GraphQLNonNull
from tartiflette.types.object import GraphQLObjectType
from tartiflette.types.scalar import GraphQLScalarType
from tartiflette.types.union import GraphQLUnionType

# pylint: disable=no-self-use
# pylint: disable=too-many-public-methods


SchemaNode = namedtuple("SchemaNode", ["type", "value"])
"""
SchemaNode is used as a container that mimics the lark.Token type.
That way, we can do child.type and child.value in any lark.Tree.children
"""


@v_args(tree=True)
class SchemaTransformer(Transformer_InPlace):
    """
    SchemaTransformer converts a cleaned lark AST tree (that has been passed
    through the CleaningTransformer) into a GraphQLSchema full definition.

    Each function is called on a `Tree` node corresponding to the
    grammar rule name.
    """

    # TODO: Add directives
    # TODO: Add type extensions
    # TODO: Cleanup errors & custom type (format, line number etc.).

    def __init__(self, sdl: str, schema: "GraphQLSchema") -> None:
        self.sdl = sdl
        self._schema = schema

    def document(self, tree: Tree) -> List[Tree]:
        return tree.children

    def schema_definition(self, tree: Tree) -> Tree:
        # TODO: Save schema directives if there are some.
        return tree

    def type_system_definition(self, tree: Tree) -> Tree:
        # Nothing to do here
        return tree.children[0]

    def _operation_type_definition(
        self, tree: Tree, operation_name: str
    ) -> Tree:
        for child in tree.children:
            if child.type == "named_type":
                setattr(self._schema, operation_name + "_type", child.value)
            elif child.type == operation_name.upper():
                pass
            else:
                raise InvalidSDL(
                    "Invalid GraphQL named type for `{}` "
                    "operation definition, got `{}`".format(
                        operation_name, child.__class__.__name__
                    )
                )
        return tree

    def query_operation_type_definition(self, tree: Tree) -> Tree:
        return self._operation_type_definition(tree, "query")

    def mutation_operation_type_definition(self, tree: Tree) -> Tree:
        return self._operation_type_definition(tree, "mutation")

    def subscription_operation_type_definition(self, tree: Tree) -> Tree:
        return self._operation_type_definition(tree, "subscription")

    def named_type(self, tree: Tree) -> SchemaNode:
        return SchemaNode("named_type", tree.children[0].value)

    def list_type(self, tree: Tree) -> SchemaNode:
        return SchemaNode(
            "list_type",
            GraphQLList(gql_type=tree.children[0].value, schema=self._schema),
        )

    def non_null_type(self, tree: Tree) -> SchemaNode:
        return SchemaNode(
            "non_null_type",
            GraphQLNonNull(
                gql_type=tree.children[0].value, schema=self._schema
            ),
        )

    def type(self, tree: Tree) -> SchemaNode:
        return SchemaNode("type", tree.children[0].value)

    def type_definition(self, tree: Tree) -> Tree:
        self._schema.add_definition(tree.children[0])
        return tree

    def scalar_type_definition(self, tree: Tree) -> GraphQLScalarType:
        description = None
        name = None
        directives = None
        for child in tree.children:
            if child.type == "description":
                description = child.value
            elif child.type == "IDENT":
                name = child.value
            elif child.type == "directives":
                directives = child.value
            elif child.type == "discard" or child.type == "SCALAR":
                pass
            else:
                raise UnexpectedASTNode(
                    "Unexpected AST node `{}`, type `{}`".format(
                        child, child.__class__.__name__
                    )
                )
        scalar = GraphQLScalarType(
            name=name,
            description=description,
            schema=self._schema,
            directives=directives,
        )
        self._schema.add_custom_scalar_definition(scalar)
        return scalar

    def union_type_definition(self, tree: Tree) -> GraphQLUnionType:
        description = None
        name = None
        members = None
        directives = None
        for child in tree.children:
            if child.type == "description":
                description = child.value
            elif child.type == "IDENT":
                name = child.value
            elif child.type == "union_members":
                members = child.value
            elif child.type == "directives":
                directives = child.value
            elif child.type == "discard" or child.type == "UNION":
                pass
            else:
                raise UnexpectedASTNode(
                    "Unexpected AST node `{}`, type `{}`".format(
                        child, child.__class__.__name__
                    )
                )
        return GraphQLUnionType(
            name=name,
            gql_types=members,
            description=description,
            schema=self._schema,
            directives=directives,
        )

    def union_member_types(self, tree: Tree) -> SchemaNode:
        return SchemaNode(
            "union_members", [child.value for child in tree.children]
        )

    def enum_type_definition(self, tree: Tree) -> GraphQLEnumType:
        description = None
        name = None
        values = None
        directives = None
        for child in tree.children:
            if child.type == "description":
                description = child.value
            elif child.type == "IDENT":
                name = child.value
            elif child.type == "directives":
                directives = child.value
            elif child.type == "enum_values":
                values = child.value
            elif child.type == "discard" or child.type == "ENUM":
                pass
            else:
                raise UnexpectedASTNode(
                    "Unexpected AST node `{}`, type `{}`".format(
                        child, child.__class__.__name__
                    )
                )

        enum_type = GraphQLEnumType(
            name=name,
            values=values,
            description=description,
            schema=self._schema,
            directives=directives,
        )
        self._schema.add_enum_definition(enum_type)
        return enum_type

    def enum_values_definition(self, tree: Tree) -> SchemaNode:
        return SchemaNode("enum_values", [child for child in tree.children])

    def enum_value_definition(self, tree: Tree) -> GraphQLEnumValue:
        description = None
        directives = None
        value = None
        for child in tree.children:
            if child.type == "description":
                description = child.value
            elif child.type == "enum_value":
                value = child.value
            elif child.type == "discard":
                pass
            elif child.type == "directives":
                directives = child.value
            else:
                raise UnexpectedASTNode(
                    "Unexpected AST node `{}`, type `{}`".format(
                        child, child.__class__.__name__
                    )
                )
        return GraphQLEnumValue(value, description, directives=directives)

    def interface_type_definition(self, tree: Tree) -> GraphQLInterfaceType:
        description = None
        name = None
        fields = None
        directives = None
        for child in tree.children:
            if child.type == "description":
                description = child.value
            elif child.type == "IDENT":
                name = child.value
            elif child.type == "fields":
                fields = child.value
            elif child.type == "directives":
                directives = child.value
            elif child.type == "discard" or child.type == "INTERFACE":
                pass
            else:
                raise UnexpectedASTNode(
                    "Unexpected AST node `{}`, type `{}`".format(
                        child, child.__class__.__name__
                    )
                )
        return GraphQLInterfaceType(
            name=name,
            fields=fields,
            description=description,
            schema=self._schema,
            directives=directives,
        )

    def object_type_definition(self, tree: Tree) -> GraphQLObjectType:
        description = None
        name = None
        interfaces = None
        fields = None
        directives = None
        for child in tree.children:
            if child.type == "description":
                description = child.value
            elif child.type == "IDENT":
                name = child.value
            elif child.type == "interfaces":
                interfaces = child.value
            elif child.type == "directives":
                directives = child.value
            elif child.type == "fields":
                fields = child.value
            elif child.type == "discard" or child.type == "TYPE":
                pass
            else:
                raise UnexpectedASTNode(
                    "Unexpected AST node `{}`, type `{}`".format(
                        child, child.__class__.__name__
                    )
                )
        return GraphQLObjectType(
            name=name,
            fields=fields,
            interfaces=interfaces,
            description=description,
            schema=self._schema,
            directives=directives,
        )

    def implements_interfaces(self, tree: Tree) -> SchemaNode:
        return SchemaNode(
            "interfaces",
            [
                child.value
                for child in tree.children
                if child.type != "IMPLEMENTS"
            ],
        )

    def input_object_type_definition(
        self, tree: Tree
    ) -> GraphQLInputObjectType:
        description = None
        name = None
        fields = None
        directives = None
        for child in tree.children:
            if child.type == "description":
                description = child.value
            elif child.type == "IDENT":
                name = child.value
            elif child.type == "directives":
                directives = child.value
            elif child.type == "input_fields":
                fields = child.value
            elif child.type == "discard" or child.type == "INPUT":
                pass
            else:
                raise UnexpectedASTNode(
                    "Unexpected AST node `{}`, type `{}`".format(
                        child, child.__class__.__name__
                    )
                )
        return GraphQLInputObjectType(
            name=name,
            fields=fields,
            description=description,
            schema=self._schema,
            directives=directives,
        )

    def input_fields_definition(self, tree: Tree) -> SchemaNode:
        return SchemaNode(
            "input_fields", {child.name: child for child in tree.children}
        )

    def fields_definition(self, tree: Tree) -> SchemaNode:
        return SchemaNode(
            "fields", {child.name: child for child in tree.children}
        )

    def field_definition(self, tree: Tree) -> GraphQLField:
        description = None
        name = None
        arguments = None
        gql_type = None
        directives = None
        for child in tree.children:
            if child.type == "description":
                description = child.value
            elif child.type == "IDENT":
                name = child.value
            elif child.type == "type":
                gql_type = child.value
            elif child.type == "arguments":
                arguments = child.value
            elif child.type == "directives":
                directives = child.value
            elif child.type == "discard":
                pass
            else:
                raise UnexpectedASTNode(
                    "Unexpected AST node `{}`, type `{}`".format(
                        child, child.__class__.__name__
                    )
                )
        return GraphQLField(
            name=name,
            gql_type=gql_type,
            arguments=arguments,
            description=description,
            directives=directives,
            schema=self._schema,
        )

    def arguments_definition(self, tree: Tree) -> SchemaNode:
        return SchemaNode(
            "arguments", {child.name: child for child in tree.children}
        )

    def input_value_definition(self, tree: Tree) -> GraphQLArgument:
        description = None
        name = None
        gql_type = None
        default_value = None
        directives = None
        for child in tree.children:
            if child.type == "description":
                description = child.value
            elif child.type == "IDENT":
                name = child.value
            elif child.type == "type":
                gql_type = child.value
            elif child.type == "value":
                default_value = child.value
            elif child.type == "discard":
                pass
            elif child.type == "directives":
                directives = child.value
            else:
                raise UnexpectedASTNode(
                    "Unexpected AST node `{}`, type `{}`".format(
                        child, child.__class__.__name__
                    )
                )
        return GraphQLArgument(
            name=name,
            gql_type=gql_type,
            default_value=default_value,
            description=description,
            directives=directives,
        )

    def directive_definition(self, tree: Tree) -> Tree:
        description = None
        name = None
        applies_on = None
        arguments = None
        for child in tree.children:
            if child.type == "description":
                description = child.value
            elif child.type == "IDENT":
                name = child.value
            elif child.type == "arguments":
                arguments = child.value
            elif child.type == "ON":
                pass
            elif child.type == "directive_locations":
                applies_on = child.value
            elif child.type == "discard" or child.type == "DIRECTIVE":
                pass
            else:
                raise UnexpectedASTNode(
                    "Unexpected AST node `{}`, type `{}`".format(
                        child, child.__class__.__name__
                    )
                )
        directive = GraphQLDirective(
            name=name,
            on=applies_on,
            arguments=arguments,
            description=description,
        )
        self._schema.add_directive(directive)
        return Tree("directive_definition", [directive])

    def directive_locations(self, tree: Tree) -> SchemaNode:
        locations = []
        for child in tree.children:
            if child.value in GraphQLDirective.POSSIBLE_LOCATIONS:
                locations.append(child.value)
            else:
                raise InvalidSDL(
                    "Invalid directive location `{}`".format(child.value)
                )
        return SchemaNode("directive_locations", locations)

    def description(self, tree: Tree) -> SchemaNode:
        return SchemaNode("description", tree.children[0].value)

    def default_value(self, tree: Tree) -> Tree:
        # Ignore this node and return the value contained
        return tree.children[0]

    def enum_value(self, tree: Tree) -> SchemaNode:
        return SchemaNode("enum_value", tree.children[0].value)

    def int_value(self, tree: Tree) -> SchemaNode:
        return SchemaNode("int_value", tree.children[0].value)

    def float_value(self, tree: Tree) -> SchemaNode:
        return SchemaNode("float_value", tree.children[0].value)

    def string_value(self, tree: Tree) -> SchemaNode:
        return SchemaNode("string_value", tree.children[0].value)

    def true_value(self, tree: Tree) -> SchemaNode:
        return SchemaNode("true_value", tree.children[0].value)

    def false_value(self, tree: Tree) -> SchemaNode:
        return SchemaNode("false_value", tree.children[0].value)

    def null_value(self, tree: Tree) -> SchemaNode:
        return SchemaNode("null_value", tree.children[0].value)

    def value(self, tree: Tree) -> SchemaNode:
        return SchemaNode("value", tree.children[0].value)

    def list_value(self, tree: Tree) -> SchemaNode:
        return SchemaNode(
            "list_value",
            [child.value for child in tree.children if child.type == "value"],
        )

    def object_value(self, tree: Tree) -> SchemaNode:
        obj = {}
        for child in tree.children:
            if child.type == "object_field":
                obj[child.value[0]] = child.value[
                    1
                ]  # name, value = child.value
            else:
                raise UnexpectedASTNode(
                    "Unexpected AST node `{}`, type `{}`".format(
                        child, child.__class__.__name__
                    )
                )
        return SchemaNode("object_value", obj)

    def object_field(self, tree: Tree) -> SchemaNode:
        name = None
        value = None
        for child in tree.children:
            if child.type == "IDENT":
                name = child.value
            elif child.type == "value":
                value = child.value
            else:
                raise UnexpectedASTNode(
                    "Unexpected AST node `{}`, type `{}`".format(
                        child, child.__class__.__name__
                    )
                )
        return SchemaNode("object_field", (name, value))

    def arguments(self, tree: Tree) -> SchemaNode:
        return SchemaNode(
            "arguments",
            {
                child.value[0]: child.value[1]  # name, value = child.value
                for child in tree.children
            },
        )

    def argument(self, tree: Tree) -> SchemaNode:
        name = None
        value = None
        for child in tree.children:
            if child.type == "IDENT":
                name = child.value
            elif child.type == "value":
                value = child.value
            else:
                raise UnexpectedASTNode(
                    "Unexpected AST node `{}`, type `{}`".format(
                        child, child.__class__.__name__
                    )
                )
        return SchemaNode("argument", (name, value))

    def directives(self, tree: Tree) -> SchemaNode:
        return SchemaNode(
            "directives",
            [
                {
                    "name": child.value[0],
                    "args": child.value[1],
                }  # name, value = child.value
                for child in tree.children
                if child.type == "directive"
            ],
        )

    def directive(self, tree: Tree) -> SchemaNode:
        name = None
        arguments = None
        for child in tree.children:
            if child.type == "IDENT":
                name = child.value
            elif child.type == "arguments":
                arguments = child.value
            else:
                raise UnexpectedASTNode(
                    "Unexpected AST node `{}`, type `{}`".format(
                        child, child.__class__.__name__
                    )
                )
        return SchemaNode("directive", (name, arguments))
