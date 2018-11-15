from collections import namedtuple

from lark import Tree, v_args
from lark.visitors import Transformer_InPlace

from tartiflette.types.argument import GraphQLArgument
from tartiflette.types.directive import GraphQLDirective
from tartiflette.types.enum import GraphQLEnumType, GraphQLEnumValue
from tartiflette.types.exceptions.tartiflette import UnexpectedASTNode
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

    def __init__(self, sdl: str, schema):
        self.sdl = sdl
        self._schema = schema

    def document(self, tree: Tree):
        return tree.children

    def schema_definition(self, tree: Tree):
        # TODO: Save schema directives if there are some.
        return tree

    def type_system_definition(self, tree: Tree):
        # Nothing to do here
        return tree.children[0]

    def _operation_type_definition(self, tree: Tree, operation_name: str):
        for child in tree.children:
            if child.type == "named_type":
                setattr(self._schema, operation_name + "_type", child.value)
            elif child.type == operation_name.upper():
                pass
            else:
                raise ValueError(
                    "Invalid GraphQL named type for `{}` "
                    "operation definition, got `{}`".format(
                        operation_name, child.__class__.__name__
                    )
                )
        return tree

    def query_operation_type_definition(self, tree: Tree):
        return self._operation_type_definition(tree, "query")

    def mutation_operation_type_definition(self, tree: Tree):
        return self._operation_type_definition(tree, "mutation")

    def subscription_operation_type_definition(self, tree: Tree):
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

    def type_definition(self, tree: Tree):
        self._schema.add_definition(tree.children[0])
        return tree

    def scalar_type_definition(self, tree: Tree) -> GraphQLScalarType:
        # TODO: Add directives
        description = None
        name = None
        for child in tree.children:
            if child.type == "description":
                description = child.value
            elif child.type == "IDENT":
                name = child.value
            elif child.type == "discard" or child.type == "SCALAR":
                pass
            else:
                raise UnexpectedASTNode(
                    "Unexpected AST node `{}`, type `{}`".format(
                        child, child.__class__.__name__
                    )
                )
        scalar = GraphQLScalarType(
            name=name, description=description, schema=self._schema
        )
        self._schema.add_custom_scalar_definition(scalar)
        return scalar

    def union_type_definition(self, tree: Tree) -> GraphQLUnionType:
        # TODO: Add directives
        description = None
        name = None
        members = None
        for child in tree.children:
            if child.type == "description":
                description = child.value
            elif child.type == "IDENT":
                name = child.value
            elif child.type == "union_members":
                members = child.value
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
        )

    def union_member_types(self, tree: Tree) -> SchemaNode:
        members = []
        for child in tree.children:
            members.append(child.value)
        return SchemaNode("union_members", members)

    def enum_type_definition(self, tree: Tree):
        # TODO: Add directives
        description = None
        name = None
        values = None
        for child in tree.children:
            if child.type == "description":
                description = child.value
            elif child.type == "IDENT":
                name = child.value
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
        )
        self._schema.add_enum_definition(enum_type)
        return enum_type

    def enum_values_definition(self, tree: Tree) -> SchemaNode:
        values = []
        for child in tree.children:
            values.append(child)
        return SchemaNode("enum_values", values)

    def enum_value_definition(self, tree: Tree) -> GraphQLEnumValue:
        # TODO: Add directives
        description = None
        value: GraphQLEnumValue = None
        for child in tree.children:
            if child.type == "description":
                description = child.value
            elif child.type == "enum_value":
                value = child.value
            elif child.type == "discard":
                pass
            else:
                raise UnexpectedASTNode(
                    "Unexpected AST node `{}`, type `{}`".format(
                        child, child.__class__.__name__
                    )
                )
        if description:
            value.description = description
        return value

    def interface_type_definition(self, tree: Tree) -> GraphQLInterfaceType:
        # TODO: Add directives
        description = None
        name = None
        fields = None
        for child in tree.children:
            if child.type == "description":
                description = child.value
            elif child.type == "IDENT":
                name = child.value
            elif child.type == "fields":
                fields = child.value
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
        )

    def object_type_definition(self, tree: Tree) -> GraphQLObjectType:
        # TODO: Add directives
        description = None
        name = None
        interfaces = None
        fields = None
        for child in tree.children:
            if child.type == "description":
                description = child.value
            elif child.type == "IDENT":
                name = child.value
            elif child.type == "interfaces":
                interfaces = child.value
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
        )

    def implements_interfaces(self, tree: Tree) -> SchemaNode:
        interfaces = []
        for child in tree.children:
            if child.type != "IMPLEMENTS":
                interfaces.append(child.value)
        return SchemaNode("interfaces", interfaces)

    def input_object_type_definition(
        self, tree: Tree
    ) -> GraphQLInputObjectType:
        # TODO: Add directives
        description = None
        name = None
        fields = None
        for child in tree.children:
            if child.type == "description":
                description = child.value
            elif child.type == "IDENT":
                name = child.value
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
        )

    def input_fields_definition(self, tree: Tree) -> SchemaNode:
        fields = {}
        for child in tree.children:
            fields[child.name] = child
        return SchemaNode("input_fields", fields)

    def fields_definition(self, tree: Tree) -> SchemaNode:
        fields = {}
        for child in tree.children:
            fields[child.name] = child
        return SchemaNode("fields", fields)

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
        arguments = {}
        for child in tree.children:
            arguments[child.name] = child
        return SchemaNode("arguments", arguments)

    def input_value_definition(self, tree: Tree):
        # TODO: Add directives
        description = None
        name = None
        gql_type = None
        default_value = None
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
        )

    def directive_definition(self, tree: Tree):
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

    def directive_locations(self, tree: Tree):
        locations = []
        for child in tree.children:
            if child.value in GraphQLDirective.POSSIBLE_LOCATIONS:
                locations.append(child.value)
            else:
                raise ValueError(
                    "Invalid directive location `{}`".format(child.value)
                )
        return SchemaNode("directive_locations", locations)

    def description(self, tree: Tree) -> SchemaNode:
        return SchemaNode("description", tree.children[0].value)

    def default_value(self, tree: Tree) -> SchemaNode:
        # Ignore this node and return the value contained
        return tree.children[0]

    def enum_value(self, tree: Tree) -> SchemaNode:
        return SchemaNode(
            "enum_value", GraphQLEnumValue(value=str(tree.children[0].value))
        )

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
                name, value = child.value
                obj[name] = value
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
        arguments = {}
        for child in tree.children:
            arguments[child.value[0]] = child.value[1]
        return SchemaNode("arguments", arguments)

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
        directives = {}
        for child in tree.children:
            if child.type == "directive":
                directives[child.value[0]] = child.value[1]
        return SchemaNode("directives", directives)

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

    def __getattr__(self, attr):
        ignored = []

        def fn(tree: Tree):
            if tree.data not in ignored:
                print("{} => {}\n".format(attr, tree))
            return tree

        return fn
