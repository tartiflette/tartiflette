import functools
from typing import Dict, List, Optional, Union

from tartiflette.executors.types import Info
from tartiflette.introspection import (IntrospectionEnumValue,
                                       IntrospectionField,
                                       IntrospectionInputValue,
                                       IntrospectionSchema, IntrospectionType,
                                       IntrospectionTypeKind,
                                       SchemaRootFieldDefinition,
                                       TypeNameRootFieldDefinition,
                                       TypeRootFieldDefinition)
from tartiflette.types.builtins import (
    GraphQLBoolean,
    GraphQLFloat,
    GraphQLID,
    GraphQLInt,
    GraphQLString,
)
from tartiflette.types.enum import GraphQLEnumType
from tartiflette.types.exceptions.tartiflette import GraphQLSchemaError, \
    UnknownSchemaFieldResolver, GraphQLError
from tartiflette.types.field import GraphQLField
from tartiflette.types.helpers import reduce_type
from tartiflette.types.interface import GraphQLInterfaceType
from tartiflette.types.list import GraphQLList
from tartiflette.types.non_null import GraphQLNonNull
from tartiflette.types.object import GraphQLObjectType
from tartiflette.types.scalar import GraphQLScalarType
from tartiflette.types.type import GraphQLType
from tartiflette.types.union import GraphQLUnionType


class GraphQLSchema:
    """
    GraphQL Schema

    Contains the complete GraphQL Schema: types, entrypoints and directives.
    """

    def __init__(self, description=None):
        self.description = description
        if not description:
            self.description = (
                "A GraphQL Schema contains the complete definition "
            )
            "of the GraphQL structure: types, entrypoints (query, "
            "mutation, subscription)."
        # Schema entry points
        self._query_type: Optional[str] = "Query"
        self._mutation_type: Optional[str] = "Mutation"
        self._subscription_type: Optional[str] = "Subscription"
        # TODO: Directives
        # Types, definitions and implementations
        self._gql_types: Dict[str, GraphQLType] = {}
        # Add default objects
        self.add_definition(GraphQLBoolean)
        self.add_definition(GraphQLFloat)
        self.add_definition(GraphQLID)
        self.add_definition(GraphQLInt)
        self.add_definition(GraphQLString)
        # All `GraphQLObjectType`s implementing a given interface
        self._implementations: Dict[str, List[GraphQLType]] = {}
        # All non-abstract types possible for a given abstract type
        self._possible_types: Dict[str, Dict[str, bool]] = {}

    def __repr__(self):
        return (
            "GraphQLSchema(query: {}, "
            "mutation: {}, "
            "subscription: {}, "
            "types: {})".format(
                self._query_type,
                self._mutation_type,
                self.subscription_type,
                self._gql_types,
            )
        )

    def __eq__(self, other):
        if not type(self) is type(other):
            return False
        if (
            self._query_type != other._query_type
            or self._mutation_type != other._mutation_type
            or self._subscription_type != other._subscription_type
        ):
            return False
        if len(self._gql_types) != len(other._gql_types):
            return False
        for key in self._gql_types:
            if key not in other._gql_types:
                return False
            elif self._gql_types[key] != other._gql_types[key]:
                return False
        return True

    @property
    def query_type(self) -> Optional[str]:
        return self._query_type

    @query_type.setter
    def query_type(self, value: str) -> None:
        self._query_type = value

    @property
    def mutation_type(self) -> Optional[str]:
        return self._mutation_type

    @mutation_type.setter
    def mutation_type(self, value: str) -> None:
        self._mutation_type = value

    @property
    def subscription_type(self) -> Optional[str]:
        return self._subscription_type

    @subscription_type.setter
    def subscription_type(self, value: str) -> None:
        self._subscription_type = value

    @property
    def types(self):
        return self._gql_types

    def add_definition(self, value: GraphQLType) -> None:
        if self._gql_types.get(value.name):
            raise ValueError(
                "new GraphQL type definition `{}` "
                "overrides existing type definition `{}`.".format(
                    value.name, repr(self._gql_types.get(value.name))
                )
            )
        self._gql_types[value.name] = value

    def to_real_type(self, gql_type: Union[str, GraphQLNonNull, GraphQLList]):
        try:
            return self._gql_types[gql_type]
        except TypeError:  # Unhashable so must be GraphQL[NonNull|List]
            pass
        root = gql_type
        prev = None
        while isinstance(gql_type, (GraphQLList, GraphQLNonNull)):
            prev = gql_type
            gql_type = gql_type.gql_type
        # TODO: Improve this logic ! It's unpythonic
        if isinstance(gql_type, str):
            prev.gql_type = self._gql_types[gql_type]
        return root

    def get_resolver(self, field_path: str) -> Optional[callable]:
        if not field_path:
            return None
        field_path_pieces = field_path.split(".")
        if not self._gql_types.get(field_path_pieces[0]):
            field_path_pieces.insert(0, self._query_type)
        field = self.get_field_by_name(".".join(field_path_pieces[0:2]))
        while field_path_pieces[-1] != getattr(field, "name", None):
            if not field:
                break
            field_path_pieces = [
                reduce_type(field.gql_type)
            ] + field_path_pieces[2:]
            field = self.get_field_by_name(".".join(field_path_pieces[0:2]))
        if field:
            return field.resolver
        return None

    def get_field_by_name(self, name: str) -> Optional[GraphQLField]:
        try:
            object_name, field_name = name.split(".")
        except ValueError as err:
            raise ValueError(
                "field name must be of the format "
                "`TypeName.fieldName` got `{}`.".format(name)
            ) from err

        try:
            return self._gql_types[object_name].fields[field_name]
        except (AttributeError, KeyError):
            raise UnknownSchemaFieldResolver(
                "field `{}` was not found in GraphQL schema.".format(name)
            )

    def bake(self) -> None:
        """
        Bake the final schema (it should not change after this) used for
        execution.

        :return: None
        """
        self.validate()
        self.inject_introspection()
        self.field_gql_types_to_real_types()
        self.union_gql_types_to_real_types()
        self.wrap_all_resolvers()
        return None

    def validate(self) -> bool:
        """
        Check that the given schema is valid.

        :return: bool
        """
        # TODO: Optimization: most validation functions iterate over
        # the schema types: it could be done in one loop.
        validators = [
            self._validate_schema_named_types,
            self._validate_object_follow_interfaces,
            self._validate_schema_root_types_exist,
            self._validate_non_empty_object,
            self._validate_union_is_acceptable,
            self._validate_all_scalars_have_implementations,
            self._validate_enum_values_are_unique,
            # TODO: Validate Field: default value must be of given type
            # TODO: Check all objects have resolvers (at least in parent)
        ]
        for validator in validators:
            # TODO: Improve validation (messages & returns).
            res = validator()
            if not res:
                return False
        return True

    def print_sdl(self):
        pass

    def _validate_schema_named_types(self):
        for type_name, gql_type in self._gql_types.items():
            try:
                for field_name, field in gql_type.fields.items():
                    gql_type = reduce_type(field.gql_type)
                    if str(gql_type) not in self._gql_types:
                        raise GraphQLSchemaError(
                            "field `{}` in GraphQL type `{}` is invalid, "
                            "the given type `{}` does not exist!".format(
                                field_name, type_name, gql_type
                            )
                        )
            except AttributeError:
                pass
        return True

    def _validate_object_follow_interfaces(self):
        for type_name, gql_type in self._gql_types.items():
            try:
                for iface_name in gql_type.interfaces:
                    try:
                        iface_type = self._gql_types[iface_name]
                    except KeyError:
                        raise GraphQLSchemaError(
                            "GraphQL type `{}` implements the `{}` interface "
                            "which does not exist!".format(
                                gql_type.name, iface_name
                            )
                        )
                    if not isinstance(iface_type, GraphQLInterfaceType):
                        raise GraphQLSchemaError(
                            "GraphQL type `{}` implements the `{}` interface "
                            "which is not an interface!".format(
                                gql_type.name, iface_name
                            )
                        )
                    for (
                        iface_field_name,
                        iface_field,
                    ) in iface_type.fields.items():
                        try:
                            gql_type_field = gql_type.fields[iface_field_name]
                        except KeyError:
                            raise GraphQLSchemaError(
                                "field `{}` is missing in GraphQL type `{}` "
                                "that implements the `{}` interface.".format(
                                    iface_field_name, gql_type.name, iface_name
                                )
                            )
                        if gql_type_field.gql_type != iface_field.gql_type:
                            raise GraphQLSchemaError(
                                "field `{}` in GraphQL type `{}` that "
                                "implements the `{}` interface does not follow "
                                "the interface field type `{}`.".format(
                                    iface_field_name,
                                    gql_type.name,
                                    iface_name,
                                    iface_field.gql_type,
                                )
                            )
            except (AttributeError, TypeError):
                pass
        return True

    def _validate_schema_root_types_exist(self):
        # Check "query" which is the only mandatory root type
        if self.query_type not in self._gql_types.keys():
            raise GraphQLSchemaError(
                "schema could not find the root `query` type `{}`.".format(
                    self.query_type
                )
            )
        elif (
            self.mutation_type != "Mutation"
            and self.mutation_type not in self._gql_types.keys()
        ):
            raise GraphQLSchemaError(
                "schema could not find the root `mutation` type `{}`.".format(
                    self.mutation_type
                )
            )
        elif (
            self.subscription_type != "Subscription"
            and self.subscription_type not in self._gql_types.keys()
        ):
            raise GraphQLSchemaError(
                "schema could not find the root `subscription` type `{}`.".format(
                    self.subscription_type
                )
            )
        return True

    def _validate_non_empty_object(self):
        for type_name, gql_type in self._gql_types.items():
            if isinstance(gql_type, GraphQLObjectType) and not gql_type.fields:
                raise GraphQLSchemaError(
                    "object type `{}` has no fields.".format(type_name)
                )
        return True

    def _validate_union_is_acceptable(self):
        for type_name, gql_type in self._gql_types.items():
            if isinstance(gql_type, GraphQLUnionType):
                for contained_type_name in gql_type.gql_types:
                    if contained_type_name == type_name:
                        raise GraphQLSchemaError(
                            "union type `{}` contains itself.".format(
                                type_name
                            )
                        )
                        # TODO: Are there other restrictions for `Union`s ?
                        # can they contain interfaces ?
                        # can they mix types: interface | object | scalar
        return True

    def _validate_all_scalars_have_implementations(self):
        for type_name, gql_type in self._gql_types.items():
            if isinstance(gql_type, GraphQLScalarType):
                if gql_type.coerce_output is None or \
                        gql_type.coerce_input is None:
                    raise GraphQLSchemaError(
                        "scalar type `{}` must have a coercion "
                        "function for inputs and outputs.".format(
                            type_name
                        )
                    )
        return True

    def _validate_enum_values_are_unique(self):
        for type_name, gql_type in self._gql_types.items():
            if isinstance(gql_type, GraphQLEnumType):
                for value in gql_type.values:
                    if str(value.value) in self._gql_types:
                        raise GraphQLSchemaError(
                        "enum type `{}` has a value of `{}` which "
                        "is not unique in the GraphQL schema.".format(
                            type_name, str(value.value),
                        )
                    )
        return True

    @staticmethod
    def wrap_field_resolver(field: GraphQLField):
        if getattr(field.resolver, "__ttftt_wrapped__", False):
            return

        def _default_resolver(parent, arguments, request_ctx, info):
            try:
                return getattr(
                    parent, info.schema_field.name,
                )
            except AttributeError:
                pass

            try:
                return parent[info.schema_field.name]
            except (KeyError, TypeError):
                pass

            return None

        resolver = field.resolver

        @functools.wraps(resolver)
        async def wrapper(parent, arguments, request_ctx, info: Info):
            try:
                result = await resolver(parent, arguments, request_ctx, info)
            except TypeError:
                result = _default_resolver(parent, arguments, request_ctx, info)
            except Exception as e:
                # TODO: Capture this error !
                print(e)
                result = None
            coerced_value = field.gql_type.coerce_value(result, info)
            return result, coerced_value

        wrapper.__ttftt_wrapped__ = True

        field.resolver = wrapper
        return

    def wrap_all_resolvers(self):
        for type_name, gql_type in self._gql_types.items():
            try:
                for field_name, field in gql_type.fields.items():
                    self.wrap_field_resolver(field)
            except AttributeError:
                pass

    def field_gql_types_to_real_types(self) -> None:
        for type_name, gql_type in self._gql_types.items():
            try:
                for field_name, field in gql_type.fields.items():
                    field.gql_type = self.to_real_type(field.gql_type)
                    try:
                        for arg_name, arg in field.arguments.items():
                            arg.gql_type = self.to_real_type(arg.gql_type)
                    except AttributeError:
                        pass
            except AttributeError:
                pass

    def union_gql_types_to_real_types(self) -> None:
        for type_name, gql_type in self._gql_types.items():
            try:
                for idx, local_gql_type in enumerate(gql_type.gql_types):
                    gql_type.gql_types[idx] = self.to_real_type(local_gql_type)
            except AttributeError as e:
                pass

    def inject_introspection(self):
        # Add Introspection types
        self.add_definition(IntrospectionSchema)
        self.add_definition(IntrospectionType)
        self.add_definition(IntrospectionTypeKind)
        self.add_definition(IntrospectionField)
        self.add_definition(IntrospectionEnumValue)
        self.add_definition(IntrospectionInputValue)
        # Add introspection field into root objects
        self.types[self.query_type].add_field(SchemaRootFieldDefinition)
        self.types[self.query_type].add_field(TypeRootFieldDefinition)
        self.types[self.query_type].add_field(TypeNameRootFieldDefinition)


DefaultGraphQLSchema = GraphQLSchema()
