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


def _format_schema_error_message(errors: List[str]) -> str:
    result = "\n"
    for index, err in enumerate(errors):
        result = "{result}\n{index}: {err}".format(
            result=result, index=index, err=err
        )
    return result


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
        try:
            self.bake_types(custom_default_resolver)  # Bake types
            self.call_onbuild_directives()  # Call on_build directive that can modify the schema
        except Exception:  # Failure here should be collected at validation time. pylint: disable=broad-except
            pass
            # TODO Change this when we'll have a better idea on what to do with the on_build kind of directive.

        self.validate()  # Revalidate.

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
        errors = []
        for validator in validators:
            errors.extend(validator())

        if errors:
            raise GraphQLSchemaError(
                message=_format_schema_error_message(errors)
            )
        return True

    def _validate_schema_named_types(self) -> List[str]:
        errors = []
        for type_name, gql_type in self._gql_types.items():
            try:
                for field in gql_type.fields:
                    reduced_type = reduce_type(field.gql_type)
                    if str(reduced_type) not in self._gql_types:
                        errors.append(
                            f"Field < {type_name}.{field.name} > is Invalid: "
                            f"the given Type < {reduced_type} > does not exist!"
                        )
            except AttributeError:
                pass
        return errors

    def _validate_object_follow_interfaces(self) -> List[str]:
        errors = []
        for gql_type in self._gql_types.values():
            try:
                ifaces_names = gql_type.interfaces_names
            except AttributeError:
                continue

            for iface_name in ifaces_names:
                try:
                    iface_type = self._gql_types[iface_name]
                    if not isinstance(iface_type, GraphQLInterfaceType):
                        errors.append(
                            f"Type < {gql_type.name} > "
                            f"implements < {iface_name} > "
                            f"which is not an interface!"
                        )
                        continue
                except KeyError:
                    errors.append(
                        f"Type < {gql_type.name} > "
                        f"implements < {iface_name} > "
                        f"which does not exist!"
                    )
                    continue

                for iface_field in iface_type.fields:
                    try:
                        gql_type_field = gql_type.find_field(iface_field.name)
                    except KeyError:
                        errors.append(
                            f"Field < {gql_type.name}.{iface_field.name} > is missing "
                            f"as defined in the < {iface_name} > Interface."
                        )
                    else:
                        if gql_type_field.gql_type != iface_field.gql_type:
                            errors.append(
                                f"Field < {gql_type.name}.{iface_field.name} > "
                                f"should be of Type < {iface_field.gql_type} > "
                                f"as defined in the < {iface_name} > Interface."
                            )
        return errors

    def _validate_schema_root_types_exist(self) -> List[str]:
        # Check "query" which is the only mandatory root type
        errors = []
        if self.query_type not in self._gql_types:
            errors.append(f"Missing Query Type < {self.query_type} >.")
        if (
            self.mutation_type != "Mutation"
            and self.mutation_type not in self._gql_types
        ):
            errors.append(f"Missing Mutation Type < {self.mutation_type} >.")
        if (
            self.subscription_type != "Subscription"
            and self.subscription_type not in self._gql_types
        ):
            errors.append(
                f"Missing Subscription Type < {self.subscription_type} >."
            )
        return errors

    def _validate_non_empty_object(self) -> List[str]:
        errors = []
        for type_name, gql_type in self._gql_types.items():
            if isinstance(gql_type, GraphQLObjectType) and not gql_type.fields:
                errors.append(f"Type < {type_name} > has no fields.")
        return errors

    def _validate_union_is_acceptable(self) -> List[str]:
        errors = []
        for type_name, gql_type in self._gql_types.items():
            if isinstance(gql_type, GraphQLUnionType):
                for contained_type_name in gql_type.gql_types:
                    if contained_type_name == type_name:
                        errors.append(
                            f"Union Type < {type_name} > contains itself."
                        )
                        # TODO: Are there other restrictions for `Union`s ?
                        # can they contain interfaces ?
                        # can they mix types: interface | object | scalar
        return errors

    def _validate_all_scalars_have_implementations(self) -> List[str]:
        errors = []
        for type_name, gql_type in self._gql_types.items():
            if isinstance(gql_type, GraphQLScalarType):
                if (
                    gql_type.coerce_output is None
                    or gql_type.coerce_input is None
                ):
                    errors.append(
                        f"Scalar < {type_name} > "
                        f"is missing an implementation"
                    )
        return errors

    def _validate_enum_values_are_unique(self) -> List[str]:
        errors = []
        for type_name, gql_type in self._gql_types.items():
            if isinstance(gql_type, GraphQLEnumType):
                for value in gql_type.values:
                    if str(value.value) in self._gql_types:
                        errors.append(
                            f"Enum < {type_name} > has a "
                            f"value of < {str(value.value)} > which "
                            f"is a Type"
                        )
        return errors

    def _validate_type_is_an_input_types(
        self, obj, message_prefix
    ) -> List[str]:
        errors = []
        rtype = reduce_type(obj.gql_type)
        if not rtype in self._input_types:
            errors.append(
                f"{message_prefix} is of type "
                f"< {rtype} > which is not a Scalar, "
                f"an Enum or an InputObject"
            )
        return errors

    def _validate_arguments_have_valid_type(self) -> List[str]:
        errors = []
        for gqltype in self._gql_types.values():
            try:
                for field in gqltype.fields:
                    for arg in field.args:
                        errors.extend(
                            self._validate_type_is_an_input_types(
                                arg,
                                f"Argument < {arg.name} > of Field < {gqltype}.{field.name} >",
                            )
                        )
            except AttributeError:
                pass

        for directive in self._directives.values():
            for arg in directive.args:
                errors.extend(
                    self._validate_type_is_an_input_types(
                        arg,
                        f"Argument < {arg.name} > of Directive < {directive.name} >",
                    )
                )

        return errors

    def _validate_input_type_composed_of_input_type(self) -> List[str]:
        errors = []
        for typename in self._input_types:
            gqltype = self._gql_types[typename]
            if isinstance(gqltype, GraphQLInputObjectType):
                for field in gqltype.inputFields:
                    errors.extend(
                        self._validate_type_is_an_input_types(
                            field, f"Field < {typename}.{field.name} >"
                        )
                    )
        return errors

    def inject_introspection(self) -> None:
        if self.query_type not in self._gql_types:
            return

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
        for gql_type in self._custom_scalars.values():
            gql_type.bake(self)

        for gql_type in self._gql_types.values():
            if not isinstance(gql_type, GraphQLScalarType):  # Are baked first
                gql_type.bake(self)

        for directive in self._directives.values():
            directive.bake(self)

        for gql_type in self._gql_types.values():
            if isinstance(gql_type, (GraphQLObjectType, GraphQLInterfaceType)):
                gql_type.bake_fields(custom_default_resolver)

    def call_onbuild_directives(self) -> None:
        for name, directive in self._directives.items():
            try:
                directive.implementation.on_build(self)
            except AttributeError:
                raise MissingImplementation(
                    "directive `{}` is missing an implementation".format(name)
                )
