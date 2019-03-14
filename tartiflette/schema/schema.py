from typing import Any, Callable, Dict, List, Optional

from tartiflette.schema.introspection import (
    SCHEMA_ROOT_FIELD_DEFINITION,
    TYPENAME_ROOT_FIELD_DEFINITION,
    prepare_type_root_field,
)
from tartiflette.types.directive import GraphQLDirective
from tartiflette.types.enum import GraphQLEnumType
from tartiflette.types.exceptions.tartiflette import (
    GraphQLSchemaError,
    ImproperlyConfigured,
    MissingImplementation,
    RedefinedImplementation,
    UnknownSchemaFieldResolver,
)
from tartiflette.types.field import GraphQLField
from tartiflette.types.helpers import reduce_type
from tartiflette.types.input_object import GraphQLInputObjectType
from tartiflette.types.interface import GraphQLInterfaceType
from tartiflette.types.non_null import GraphQLNonNull
from tartiflette.types.object import GraphQLObjectType
from tartiflette.types.scalar import GraphQLScalarType
from tartiflette.types.type import GraphQLType
from tartiflette.types.union import GraphQLUnionType

_DEFAULT_QUERY_TYPE = "Query"
_DEFAULT_MUTATION_TYPE = "Mutation"
_DEFAULT_SUBSCRIPTION_TYPE = "Subscription"


class GraphQLSchema:
    """
    GraphQL Schema

    Contains the complete GraphQL Schema: types, entrypoints and directives.
    """

    def __init__(
        self, name: str = "default", description: Optional[str] = None
    ) -> None:
        self.description = (
            description
            or """A GraphQL Schema contains the complete definition of the GraphQL structure: types, entrypoints (query, mutation, subscription)."""
        )

        # Schema entry points
        self._query_type: Optional[str] = _DEFAULT_QUERY_TYPE
        self._mutation_type: Optional[str] = _DEFAULT_MUTATION_TYPE
        self._subscription_type: Optional[str] = _DEFAULT_SUBSCRIPTION_TYPE
        # Types, definitions and implementations
        self._gql_types: Dict[str, GraphQLType] = {}
        # Directives
        self._directives: Dict[str, GraphQLDirective] = {}
        # All `GraphQLObjectType`s implementing a given interface
        self._implementations: Dict[str, List[GraphQLType]] = {}
        # All non-abstract types possible for a given abstract type
        self._possible_types: Dict[str, Dict[str, bool]] = {}
        self._enums: Dict[str, GraphQLEnumType] = {}
        self._custom_scalars: Dict[str, GraphQLScalarType] = {}
        self._input_types: List[str] = []
        self.name = name

    def __repr__(self) -> str:
        return (
            "GraphQLSchema(name: {}, query: {}, "
            "mutation: {}, "
            "subscription: {}, "
            "types: {})".format(
                self.name,
                self._query_type,
                self._mutation_type,
                self.subscription_type,
                self._gql_types,
            )
        )

    def __eq__(self, other: Any) -> bool:
        if not type(self) is type(other):
            return False
        if (
            self._query_type != other.query_type
            or self._mutation_type != other.mutation_type
            or self._subscription_type != other.subscription_type
        ):
            return False
        if len(self._gql_types) != len(other.types):
            return False
        for key in self._gql_types:
            try:
                if self._gql_types[key] != other.gql_types[key]:
                    return False
            except KeyError:
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

    def get_operation_type(self, operation_name: str) -> Optional[str]:
        if operation_name == _DEFAULT_QUERY_TYPE:
            return self.query_type
        if operation_name == _DEFAULT_MUTATION_TYPE:
            return self.mutation_type
        if operation_name == _DEFAULT_SUBSCRIPTION_TYPE:
            return self.subscription_type
        return None

    #  Introspection Attribute
    @property
    def queryType(  # pylint: disable=invalid-name
        self
    ) -> Optional[GraphQLType]:
        try:
            return self._gql_types[self.query_type]
        except KeyError:
            pass
        return None

    #  Introspection Attribute
    @property
    def subscriptionType(  # pylint: disable=invalid-name
        self
    ) -> Optional[GraphQLType]:
        try:
            return self._gql_types[self.subscription_type]
        except KeyError:
            pass
        return None

    #  Introspection Attribute
    @property
    def mutationType(  # pylint: disable=invalid-name
        self
    ) -> Optional[GraphQLType]:
        try:
            return self._gql_types[self.mutation_type]
        except KeyError:
            pass
        return None

    #  Introspection Attribute
    @property
    def types(self) -> List[GraphQLType]:
        return [
            self._gql_types[x]
            for x in self._gql_types
            if not x.startswith("__")
        ]

    def find_type(self, name: str) -> GraphQLType:
        return self._gql_types[name]

    def has_type(self, name: str) -> bool:
        return name in self._gql_types

    @property
    def gql_types(self) -> Dict[str, GraphQLType]:
        return self._gql_types

    #  Introspection Attribute
    @property
    def directives(self) -> List[GraphQLDirective]:
        return list(self._directives.values())

    def find_directive(self, name: str) -> GraphQLDirective:
        return self._directives[name]

    @property
    def enums(self) -> Dict[str, GraphQLEnumType]:
        return self._enums

    def find_enum(self, name: str) -> GraphQLEnumType:
        return self._enums.get(name)

    def find_scalar(self, name: str) -> Optional[GraphQLScalarType]:
        return self._custom_scalars.get(name)

    def add_directive(self, value: GraphQLDirective) -> None:
        if self._directives.get(value.name):
            raise RedefinedImplementation(
                "new GraphQL directive definition `{}` "
                "overrides existing directive definition `{}`.".format(
                    value.name, repr(self._directives.get(value.name))
                )
            )
        self._directives[value.name] = value

    def add_definition(self, value: GraphQLType) -> None:
        if self._gql_types.get(value.name):
            raise RedefinedImplementation(
                "new GraphQL type definition `{}` "
                "overrides existing type definition `{}`.".format(
                    value.name, repr(self._gql_types.get(value.name))
                )
            )
        self._gql_types[value.name] = value
        if isinstance(value, GraphQLInputObjectType):
            self._input_types.append(value.name)

    def add_enum_definition(self, value: GraphQLEnumType) -> None:
        if self._enums.get(value.name):
            raise RedefinedImplementation(
                "new GraphQL enum definition `{}` "
                "overrides existing enum definition `{}`.".format(
                    value.name, repr(self._enums.get(value.name))
                )
            )
        self._enums[value.name] = value
        self._input_types.append(value.name)

    def add_custom_scalar_definition(self, value: GraphQLScalarType) -> None:
        if self._custom_scalars.get(value.name):
            raise RedefinedImplementation(
                "new GraphQL scalar definition `{}` "
                "overrides existing scalar definition `{}`.".format(
                    value.name, repr(self._custom_scalars.get(value.name))
                )
            )
        self._custom_scalars[value.name] = value
        self._input_types.append(value.name)

    def get_field_by_name(self, name: str) -> GraphQLField:
        try:
            object_name, field_name = name.split(".")
        except ValueError:
            raise ImproperlyConfigured(
                "field name must be of the format "
                "`TypeName.fieldName` got `{}`.".format(name)
            )

        try:
            return self._gql_types[object_name].find_field(field_name)
        except (AttributeError, KeyError):
            raise UnknownSchemaFieldResolver(
                "field `{}` was not found in GraphQL schema.".format(name)
            )

    def bake(self, custom_default_resolver: Optional[Callable] = None) -> None:
        """
        Bake the final schema (it should not change after this) used for
        execution.

        :return: None
        """
        self.inject_introspection()
        self.bake_types(custom_default_resolver)
        self.call_onbuild_directives()
        self.validate()

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
            self._validate_arguments_have_valid_type,
            self._validate_input_type_composed_of_input_type,
            # TODO: Validate Field: default value must be of given type
            # TODO: Check all objects have resolvers (at least in parent)
        ]
        for validator in validators:
            # TODO: Improve validation (messages & returns).
            res = validator()
            if not res:
                return False
        return True

    def _validate_schema_named_types(self) -> bool:
        for type_name, gql_type in self._gql_types.items():
            try:
                for field in gql_type.fields:
                    reduced_type = reduce_type(field.gql_type)
                    if str(reduced_type) not in self._gql_types:
                        raise GraphQLSchemaError(
                            "field `{}` in GraphQL type `{}` is invalid, "
                            "the given type `{}` does not exist!".format(
                                field.name, type_name, reduced_type
                            )
                        )
            except AttributeError:
                pass
        return True

    def _validate_object_follow_interfaces(self) -> bool:
        for gql_type in self._gql_types.values():
            try:
                ifaces_names = gql_type.interfaces_names
            except AttributeError:
                continue

            for iface_name in ifaces_names:
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

                for iface_field in iface_type.fields:
                    try:
                        gql_type_field = gql_type.find_field(iface_field.name)
                    except KeyError:
                        raise GraphQLSchemaError(
                            "field `{}` is missing in GraphQL type `{}` "
                            "that implements the `{}` interface.".format(
                                iface_field.name, gql_type.name, iface_name
                            )
                        )
                    if gql_type_field.gql_type != iface_field.gql_type:
                        raise GraphQLSchemaError(
                            "field `{}` in GraphQL type `{}` that "
                            "implements the `{}` interface does not follow "
                            "the interface field type `{}`.".format(
                                iface_field.name,
                                gql_type.name,
                                iface_name,
                                iface_field.gql_type,
                            )
                        )
        return True

    def _validate_schema_root_types_exist(self) -> bool:
        # Check "query" which is the only mandatory root type
        if self.query_type not in self._gql_types:
            raise GraphQLSchemaError(
                "schema could not find the root `query` type `{}`.".format(
                    self.query_type
                )
            )
        if (
            self.mutation_type != "Mutation"
            and self.mutation_type not in self._gql_types
        ):
            raise GraphQLSchemaError(
                "schema could not find the root `mutation` type `{}`.".format(
                    self.mutation_type
                )
            )
        if (
            self.subscription_type != "Subscription"
            and self.subscription_type not in self._gql_types
        ):
            raise GraphQLSchemaError(
                "schema could not find the root `subscription` type `{}`.".format(
                    self.subscription_type
                )
            )
        return True

    def _validate_non_empty_object(self) -> bool:
        for type_name, gql_type in self._gql_types.items():
            if isinstance(gql_type, GraphQLObjectType) and not gql_type.fields:
                raise GraphQLSchemaError(
                    "object type `{}` has no fields.".format(type_name)
                )
        return True

    def _validate_union_is_acceptable(self) -> bool:
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

    def _validate_all_scalars_have_implementations(self) -> bool:
        for type_name, gql_type in self._gql_types.items():
            if isinstance(gql_type, GraphQLScalarType):
                if (
                    gql_type.coerce_output is None
                    or gql_type.coerce_input is None
                ):
                    raise GraphQLSchemaError(
                        "scalar type `{}` must have a coercion "
                        "function for inputs and outputs.".format(type_name)
                    )
        return True

    def _validate_enum_values_are_unique(self) -> bool:
        for type_name, gql_type in self._gql_types.items():
            if isinstance(gql_type, GraphQLEnumType):
                for value in gql_type.values:
                    if str(value.value) in self._gql_types:
                        raise GraphQLSchemaError(
                            "enum type `{}` has a value of `{}` which "
                            "is not unique in the GraphQL schema.".format(
                                type_name, str(value.value)
                            )
                        )
        return True

    def _validate_type_is_an_input_types(self, obj, message_prefix) -> bool:
        rtype = reduce_type(obj.gql_type)
        if not rtype in self._input_types:
            raise GraphQLSchemaError(
                message=f"{message_prefix} is of type <{rtype}> which is not a Scalar, an Enum or an InputObject"
            )

    def _validate_arguments_have_valid_type(self) -> bool:
        for gqltype in self._gql_types.values():
            try:
                for field in gqltype.fields:
                    for arg in field.args:
                        self._validate_type_is_an_input_types(
                            arg,
                            f"Argument <{arg.name}> of Field <{gqltype}.{field.name}>",
                        )
            except AttributeError:
                pass

        for directive in self._directives.values():
            for arg in directive.args:
                self._validate_type_is_an_input_types(
                    arg,
                    f"Argument <{arg.name}> of Directive <{directive.name}>",
                )

        return True

    def _validate_input_type_composed_of_input_type(self) -> bool:
        for typename in self._input_types:
            gqltype = self._gql_types[typename]
            if isinstance(gqltype, GraphQLInputObjectType):
                for field in gqltype.inputFields:
                    self._validate_type_is_an_input_types(
                        field, f"Field <{typename}.{field.name}>"
                    )
        return True

    def inject_introspection(self) -> None:
        self._gql_types[self.query_type].add_field(
            SCHEMA_ROOT_FIELD_DEFINITION(
                gql_type=GraphQLNonNull("__Schema", schema=self)
            )
        )
        self._gql_types[self.query_type].add_field(
            prepare_type_root_field(self)
        )

        for gql_type in self._gql_types.values():
            try:
                __typename = TYPENAME_ROOT_FIELD_DEFINITION(
                    schema=self,
                    gql_type=GraphQLNonNull(gql_type="String", schema=self),
                )
                gql_type.add_field(__typename)
            except AttributeError:
                pass

    def bake_types(
        self, custom_default_resolver: Optional[Callable] = None
    ) -> None:
        for gql_type in self._gql_types.values():
            gql_type.bake(self, custom_default_resolver)

        for directive in self._directives.values():
            directive.bake(self)

    def call_onbuild_directives(self) -> None:
        for name, directive in self._directives.items():
            try:
                directive.implementation.on_build(self)
            except AttributeError:
                raise MissingImplementation(
                    "directive `{}` is missing an implementation".format(name)
                )
