from collections import OrderedDict

from lark.lexer import Token
from lark.tree import Transformer_NoRecurse, Tree

from tartiflette.sdl.schema import DefaultGraphQLSchema
from tartiflette.sdl.transformers.helpers import find_token_in_ast
from tartiflette.sdl.transformers.schema import GraphQLType, GraphQLValue, \
    GraphQLNamedType, GraphQLUnionTypeDefinition, GraphQLNamedTypeDefinition, \
    GraphQLScalarTypeDefinition, GraphQLInterfaceTypeDefinition, \
    GraphQLFieldDefinition, GraphQLListType, GraphQLNonNullType, \
    GraphQLArgumentDefinition, GraphQLObjectTypeDefinition, \
    GraphQLInputObjectTypeDefinition, GraphQLEnumTypeDefinition, Description, \
    Name, GraphQLScalarValue, GraphQLEnumValue, GraphQLListValue, \
    GraphQLObjectValue, GraphQLObjectFieldValue, GraphQLEnumValueDefinition
"""
import_sdl -> create AST -> convert to schema -> validate schema

import_sdl -> build_schema -> validate_schema -> link it with external definitions (custom Scalar, directives, resolvers <- auto imports) -> runnable ! :D

@QueryResolver(schema_endpoint)
def func(...)
"""


class SchemaTransformer(Transformer_NoRecurse):
    """
    SchemaTransformer converts a cleaned lark AST tree (that has been passed
    through the CleaningTransformer) into a GraphQLSchema full definition.

    Each function is called on a `Tree` node corresponding to the
    grammar rule name.
    """

    def __init__(self, input_sdl: str, schema=None):
        self.input_sdl = input_sdl
        self._schema = schema if schema else DefaultGraphQLSchema

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
            if isinstance(child, GraphQLNamedType):
                setattr(self._schema, operation_name + "_type", child)
            elif isinstance(child, Token) and \
                    child.type == operation_name.upper():
                pass
            else:
                raise ValueError(
                    'Invalid GraphQLNamedType for `{}` '
                    'operation definition, got `{}`'.format(
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

    def named_type(self, tree: Tree):
        token = find_token_in_ast(tree.children, ['IDENT'])
        return GraphQLNamedType(str(token.value), ast_node=token)

    def type(self, tree: Tree):
        subtype = tree.children[0]
        if not isinstance(subtype, GraphQLType):
            raise ValueError(
                'Invalid GraphQLType, got `{}`'.format(
                    subtype.__class__.__name__
                )
            )
        else:
            return subtype

    def type_definition(self, tree: Tree):
        for child in tree.children:
            if isinstance(child, GraphQLNamedTypeDefinition):
                self._schema.add_definition(child)
            else:
                raise ValueError(
                    'All GraphQL type definitions must be '
                    'sub-classes of type '
                    '`GraphQLNamedTypeDefinition`, '
                    'got `{}`'.format(child.__class__.__name__)
                )
        return tree

    def scalar_type_definition(self, tree: Tree):
        description = None
        ast_node = None
        name = None
        directives = []  # TODO: To do !
        for child in tree.children:
            if isinstance(child, Description):
                description = child
            elif isinstance(child, Token) and child.type == 'SCALAR':
                ast_node = child
            elif isinstance(child, Token) and child.type == 'IDENT':
                name = Name(name=child.value, ast_node=child)
            else:
                raise ValueError(
                    '`scalar_type_definition` unknown AST Node, '
                    'got `{}`'.format(child.__class__.__name__)
                )
        return GraphQLScalarTypeDefinition(
            name=name, description=description, ast_node=ast_node
        )

    def union_type_definition(self, tree: Tree):
        description = None
        ast_node = None
        name = None
        directives = []  # TODO: To do !
        union_members = []
        for child in tree.children:
            if isinstance(child, Description):
                description = child
            elif isinstance(
                child, Tree
            ) and child.data == 'union_member_types':
                union_members = child.children
            elif isinstance(child, Token) and child.type == 'UNION':
                ast_node = child
            elif isinstance(child, Token) and child.type == 'IDENT':
                name = Name(name=child.value, ast_node=child)
            else:
                raise ValueError(
                    '`union_type_definition` unknown AST Node, '
                    'got `{}`'.format(child.__class__.__name__)
                )
        return GraphQLUnionTypeDefinition(
            name=name,
            types=union_members,
            description=description,
            ast_node=ast_node
        )

    def union_member_types(self, tree: Tree):
        # TODO: Is this check useful ? We may be able to remove it !
        for child in tree.children:
            if not isinstance(child, GraphQLNamedType):
                raise ValueError(
                    '`union_member_type`s must be '
                    '`GraphQLNamedType`s, '
                    'got {}'.format(child.__class__.__name__)
                )
        return tree

    def enum_type_definition(self, tree: Tree):
        description = None
        name = None
        directives = []  # TODO: To do !
        values = []
        for child in tree.children:
            if isinstance(child, Description):
                description = child
            elif isinstance(child, Token) and child.type == 'ENUM':
                ast_node = child
            elif isinstance(child, Token) and child.type == 'IDENT':
                name = Name(name=child.value, ast_node=child)
            elif isinstance(child, dict) and child.get("values"):
                values = child.get("values")
            else:
                raise ValueError(
                    '`enum_type_definition` unknown AST Node, '
                    'got `{}`'.format(child.__class__.__name__)
                )
        return GraphQLEnumTypeDefinition(
            name=name,
            values=values,
            description=description,
            ast_node=ast_node
        )

    def enum_values_definition(self, tree: Tree):
        values = []
        for child in tree.children:
            if isinstance(child, GraphQLEnumValueDefinition):
                values.append(child)
            else:
                raise ValueError(
                    '`enum_values_definition` unknown AST Node, '
                    'got `{}`'.format(child.__class__.__name__)
                )
        return {"values": values}

    def enum_value_definition(self, tree: Tree):
        description = None
        enum_value = None
        directives = []  # TODO: To do !
        for child in tree.children:
            if isinstance(child, Description):
                description = child
            elif isinstance(child, GraphQLEnumValue):
                enum_value = child
            # elif isinstance(child, GraphQLDirective):
            #     ...
            else:
                raise ValueError(
                    '`enum_value_definition` unknown AST Node, '
                    'got `{}`'.format(child.__class__.__name__)
                )
        return GraphQLEnumValueDefinition(
            key=enum_value.value,
            description=description,
            ast_node=enum_value.ast_node
        )

    def interface_type_definition(self, tree: Tree):
        description = None
        ast_node = None
        name = None
        directives = []  # TODO: To do !
        fields = {}
        for child in tree.children:
            if isinstance(child, Description):
                description = child
            elif isinstance(child, Token) and child.type == 'INTERFACE':
                ast_node = child
            elif isinstance(child, Token) and child.type == 'IDENT':
                name = Name(name=child.value, ast_node=child)
            elif isinstance(child, dict) and child.get("fields"):
                fields = child.get("fields")
            else:
                raise ValueError(
                    '`interface_type_definition` unknown AST Node, '
                    'got `{}`'.format(child.__class__.__name__)
                )
        return GraphQLInterfaceTypeDefinition(
            name=name,
            fields=fields,
            description=description,
            ast_node=ast_node
        )

    def object_type_definition(self, tree: Tree):
        description = None
        ast_node = None
        name = None
        interfaces = []
        directives = []  # TODO: To do !
        fields = OrderedDict()
        for child in tree.children:
            if isinstance(child, Description):
                description = child
            elif isinstance(child, Token) and child.type == 'TYPE':
                ast_node = child
            elif isinstance(child, Token) and child.type == 'IDENT':
                name = Name(name=child.value, ast_node=child)
            elif isinstance(child, dict) and child.get("interfaces"):
                interfaces = child.get("interfaces")
            elif isinstance(child, dict) and child.get("fields"):
                fields = child.get("fields")
            elif isinstance(child, GraphQLFieldDefinition):
                fields[child.name] = child
            elif child is None:
                pass  # TODO: directives to do.
            else:
                raise ValueError(
                    '`object_type_definition` unknown AST Node, '
                    'got `{}`'.format(child.__class__.__name__)
                )
        return GraphQLObjectTypeDefinition(
            name=name,
            fields=fields,
            interfaces=interfaces,
            description=description,
            ast_node=ast_node
        )

    def implements_interfaces(self, tree: Tree):
        interfaces = []
        for child in tree.children:
            if isinstance(child, GraphQLNamedType):
                interfaces.append(child)
            elif isinstance(child, Token) and child.type == 'IMPLEMENTS':
                pass
            else:
                raise ValueError(
                    '`implements_interfaces` unknown AST Node, '
                    'got `{}`'.format(child.__class__.__name__)
                )
        return {"interfaces": interfaces}

    def input_object_type_definition(self, tree: Tree):
        description = None
        ast_node = None
        name = None
        directives = []  # TODO: To do !
        fields = OrderedDict()
        for child in tree.children:
            if isinstance(child, Description):
                description = child
            elif isinstance(child, Token) and child.type == 'INPUT':
                ast_node = child
            elif isinstance(child, Token) and child.type == 'IDENT':
                name = Name(name=child.value, ast_node=child)
            elif isinstance(child, dict) and child.get("fields"):
                fields = child.get("fields")
            elif isinstance(child, GraphQLFieldDefinition):
                fields[child.name] = child
            else:
                raise ValueError(
                    '`input_object_type_definition` unknown AST Node, '
                    'got `{}`'.format(child.__class__.__name__)
                )
        return GraphQLInputObjectTypeDefinition(
            name=name,
            fields=fields,
            description=description,
            ast_node=ast_node
        )

    def input_fields_definition(self, tree: Tree):
        fields = OrderedDict()
        for child in tree.children:
            if isinstance(child, GraphQLArgumentDefinition):
                fields[child.name] = child
            else:
                raise ValueError(
                    '`input_fields_definition` unknown AST Node, '
                    'got `{}`'.format(child.__class__.__name__)
                )
        return {"fields": fields}

    def fields_definition(self, tree: Tree):
        fields = OrderedDict()
        for child in tree.children:
            if isinstance(child, GraphQLFieldDefinition):
                fields[child.name] = child
            else:
                raise ValueError(
                    '`fields_definition` unknown AST Node, '
                    'got `{}`'.format(child.__class__.__name__)
                )
        return {"fields": fields}

    def field_definition(self, tree: Tree):
        description = None
        name = find_token_in_ast(tree, ['IDENT'])
        arguments = OrderedDict()
        gql_type = None
        directives = []  # TODO: To do !
        for child in tree.children:
            if isinstance(child, Description):
                description = child
            elif isinstance(child, Token) and child.type == 'IDENT':
                name = Name(name=child.value, ast_node=child)
            elif isinstance(child, GraphQLType):
                gql_type = child
            elif isinstance(child, dict) and child.get("arguments"):
                arguments = child.get("arguments")
            elif child is None:
                pass  # TODO: directives to do.
            # elif isinstance(child, GraphQLDirective):
            #     directives.append(child)
            else:
                raise ValueError(
                    '`field_definition` unknown AST Node, '
                    'got `{}`'.format(child.__class__.__name__)
                )
        return GraphQLFieldDefinition(
            name=name,
            gql_type=gql_type,
            arguments=arguments,
            description=description
        )

    def arguments_definition(self, tree: Tree):
        arguments = OrderedDict()
        for child in tree.children:
            if isinstance(child, GraphQLArgumentDefinition):
                arguments[child.name] = child
            else:
                raise ValueError(
                    '`arguments_definition` unknown AST Node, '
                    'got `{}`'.format(child.__class__.__name__)
                )
        return {"arguments": arguments}

    def input_value_definition(self, tree: Tree):
        description = None
        name = None
        gql_type = None
        default_value = None
        for child in tree.children:
            if isinstance(child, Description):
                description = child
            elif isinstance(child, Token) and child.type == 'IDENT':
                name = Name(name=child.value, ast_node=child)
            elif isinstance(child, GraphQLType):
                gql_type = child
            elif isinstance(child, GraphQLValue):
                default_value = child
            else:
                raise ValueError(
                    '`input_value_definition` unknown AST Node, '
                    'got `{}`'.format(child.__class__.__name__)
                )
        return GraphQLArgumentDefinition(
            name=name,
            gql_type=gql_type,
            default_value=default_value,
            description=description
        )

    def list_type(self, tree: Tree):
        child = tree.children[0]
        if isinstance(child, GraphQLType):
            return GraphQLListType(gql_type=child)
        else:
            raise ValueError(
                '`list_type` unknown AST Node, '
                'got `{}`'.format(child.__class__.__name__)
            )

    def non_null_type(self, tree: Tree):
        child = tree.children[0]
        if isinstance(child, GraphQLType):
            return GraphQLNonNullType(gql_type=child)
        else:
            raise ValueError(
                '`non_null_type` unknown AST Node, '
                'got `{}`'.format(child.__class__.__name__)
            )

    def description(self, tree: Tree):
        token = find_token_in_ast(tree.children, ['DESCRIPTION'])
        return Description(description=token.value, ast_node=token)

    def default_value(self, tree: Tree):
        return tree.children[0]

    def enum_value(self, tree: Tree):
        token = tree.children[0]
        return GraphQLEnumValue(token.value, ast_node=token)

    def value(self, tree: Tree):
        value_type_to_gql_type = {
            "int_value": GraphQLScalarValue,
            "float_value": GraphQLScalarValue,
            "string_value": GraphQLScalarValue,
            "true_value": GraphQLScalarValue,
            "false_value": GraphQLScalarValue,
            "null_value": GraphQLScalarValue,
        }
        subtree = tree.children[0]
        if isinstance(subtree, GraphQLEnumValue):
            return subtree
        value_type = getattr(subtree, "data")
        if value_type in value_type_to_gql_type.keys():
            token = subtree.children[0]
            return value_type_to_gql_type[value_type](
                token.value, ast_node=token
            )
        elif value_type == "list_value":
            return GraphQLListValue(subtree.children)
        elif value_type == "object_value":
            return GraphQLObjectValue(subtree.children)
        # TODO: This should never happen. Leave an alert here ?
        raise ValueError(
            '`value` unknown AST Node, '
            'got `{}`'.format(value_type.__class__.__name__)
        )

    def object_field(self, tree: Tree):
        name = None
        value = None
        for child in tree.children:
            if isinstance(child, Token):
                name = Name(name=child.value, ast_node=child)
            else:
                value = child
        return GraphQLObjectFieldValue(name, value)

    def argument(self, tree: Tree):
        name = None
        value = None
        for child in tree.children:
            if isinstance(child, Token):
                name = Name(name=child.value, ast_node=child)
            else:
                value = child
        return {name.name: value}

    def arguments(self, tree: Tree):
        kwargs = {}
        for child in tree.children:
            if isinstance(child, dict):
                kwargs.update(child)
            else:
                raise ValueError(
                    '`arguments` unknown AST Node, '
                    'got `{}`'.format(child.__class__.__name__)
                )
        return kwargs

    def directives(self, tree: Tree):
        # TODO !!!!
        return None

    def directive(self, tree: Tree):
        # TODO !!!
        return None

    def __getattr__(self, attr):
        ignored = [
            'int_value',
            'float_value',
            'string_value',
            'list_value',
            'object_value',
            'enum_value',
            'true_value',
            'false_value',
            'null_value',
        ]

        def fn(tree: Tree):
            if tree.data not in ignored:
                print('{}({})\n'.format(attr, tree))
            return tree

        return fn
