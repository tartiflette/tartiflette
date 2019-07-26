from inspect import iscoroutinefunction
from typing import Any, Callable, Dict, List, Optional, Union

from tartiflette.resolver.default import default_type_resolver
from tartiflette.schema.introspection import (
    SCHEMA_ROOT_FIELD_DEFINITION,
    TYPENAME_ROOT_FIELD_DEFINITION,
    prepare_type_root_field,
)
from tartiflette.types.enum import GraphQLEnumType
from tartiflette.types.exceptions.tartiflette import (
    GraphQLSchemaError,
    ImproperlyConfigured,
    RedefinedImplementation,
    UnknownSchemaFieldResolver,
)
from tartiflette.types.helpers.reduce_type import reduce_type
from tartiflette.types.input_object import GraphQLInputObjectType
from tartiflette.types.interface import GraphQLInterfaceType
from tartiflette.types.non_null import GraphQLNonNull
from tartiflette.types.object import GraphQLObjectType
from tartiflette.types.scalar import GraphQLScalarType
from tartiflette.types.union import GraphQLUnionType
from tartiflette.utils.errors import graphql_error_from_nodes

__all__ = ("GraphQLSchema",)

_DEFAULT_QUERY_OPERATION_NAME = "Query"
_DEFAULT_MUTATION_OPERATION_NAME = "Mutation"
_DEFAULT_SUBSCRIPTION_OPERATION_NAME = "Subscription"


_IMPLEMENTABLE_DIRECTIVE_HOOKS = (
    "on_post_bake",
    "on_pre_output_coercion",
    "on_introspection",
    "on_post_input_coercion",
    "on_argument_execution",
    "on_field_execution",
    "on_field_collection",
    "on_fragment_spread_collection",
    "on_inline_fragment_collection",
)


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

    # pylint: disable=too-many-instance-attributes

    # Introspection attributes
    description = "A GraphQL Schema defines the capabilities of a GraphQL server. It exposes all available types and directives on the server, as well as the entry points for query, mutation, and subscription operations."

    def __init__(self, name: str = "default") -> None:
        """
        :param name: name of the schema
        :type name: str
        """
        self.name = name
        self.default_type_resolver: Optional[Callable] = None

        # Operation type names
        self.query_operation_name: str = _DEFAULT_QUERY_OPERATION_NAME
        self.mutation_operation_name: str = _DEFAULT_MUTATION_OPERATION_NAME
        self.subscription_operation_name: str = _DEFAULT_SUBSCRIPTION_OPERATION_NAME

        # Type, directive, enum, scalar & input type definitions
        self.type_definitions: Dict[str, "GraphQLType"] = {}
        self._directive_definitions: Dict[str, "GraphQLDirective"] = {}
        self._scalar_definitions: Dict[str, "GraphQLScalarType"] = {}
        self._enum_definitions: Dict[str, "GraphQLEnumType"] = {}
        self._input_types: List[
            Union[
                "GraphQLScalarType",
                "GraphQLEnumType",
                "GraphQLInputObjectType",
            ]
        ] = []
        self._operation_types: Dict[str, "GraphQLObjectType"] = {}

        # Introspection attributes
        self.types: List["GraphQLType"] = []
        self.queryType: Optional[  # pylint: disable=invalid-name
            "GraphQLType"
        ] = None
        self.mutationType: Optional[  # pylint: disable=invalid-name
            "GraphQLType"
        ] = None
        self.subscriptionType: Optional[  # pylint: disable=invalid-name
            "GraphQLType"
        ] = None
        self.directives: List[  # pylint: disable=invalid-name
            "GraphQLDirective"
        ] = []

    def __eq__(self, other: Any) -> bool:
        """
        Returns True if `other` instance is identical to `self`.
        :param other: object instance to compare to `self`
        :type other: Any
        :return: whether or not `other` is identical to `self`
        :rtype: bool
        """
        return self is other or (
            isinstance(other, GraphQLSchema)
            and self.name == other.name
            and self.query_operation_name == other.query_operation_name
            and self.mutation_operation_name == other.mutation_operation_name
            and self.subscription_operation_name
            == other.subscription_operation_name
            and self.type_definitions == other.type_definitions
        )

    def __repr__(self) -> str:
        """
        Returns the representation of a GraphQLSchema instance.
        :return: the representation of a GraphQLSchema instance
        :rtype: str
        """
        return "GraphQLSchema(name={!r})".format(self.name)

    def __str__(self) -> str:
        """
        Returns a human-readable representation of the schema.
        :return: a human-readable representation of the schema
        :rtype: str
        """
        return self.name

    def __hash__(self) -> int:
        """
        Hash the name of the schema as a unique representation of a
        GraphQLSchema.
        :return: hash of the schema name
        :rtype: int
        """
        return hash(self.name)

    def add_type_definition(self, type_definition: "GraphQLType") -> None:
        """
        Adds a GraphQLType to the defined type list.
        :param type_definition: GraphQLType to add
        :type type_definition: GraphQLType
        """
        if type_definition.name in self.type_definitions:
            raise RedefinedImplementation(
                "new GraphQL type definition `{}` "
                "overrides existing type definition `{}`.".format(
                    type_definition.name,
                    repr(self.type_definitions.get(type_definition.name)),
                )
            )
        self.type_definitions[type_definition.name] = type_definition
        if isinstance(type_definition, GraphQLInputObjectType):
            self._input_types.append(type_definition.name)

    def has_type(self, name: str) -> bool:
        """
        Determines whether or not the name corresponds to a defined type.
        :param name: name of the type to find
        :type name: str
        :return: whether or not the name corresponds to a defined type
        :rtype: bool
        """
        return name in self.type_definitions

    def find_type(self, name: str) -> "GraphQLType":
        """
        Returns the defined type corresponding to the name.
        :param name: name of the type to return
        :type name: str
        :return: the defined type
        :rtype: GraphQLType
        """
        return self.type_definitions[name]

    def add_directive_definition(
        self, directive_definition: "GraphQLDirective"
    ) -> None:
        """
        Adds a GraphQLDirective to the defined directive list.
        :param directive_definition: GraphQLDirective to add
        :type directive_definition: GraphQLDirective
        """
        if directive_definition.name in self._directive_definitions:
            raise RedefinedImplementation(
                "new GraphQL directive definition `{}` "
                "overrides existing directive definition `{}`.".format(
                    directive_definition.name,
                    repr(
                        self._directive_definitions.get(
                            directive_definition.name
                        )
                    ),
                )
            )
        self._directive_definitions[
            directive_definition.name
        ] = directive_definition

    def find_directive(self, name: str) -> "GraphQLDirective":
        """
        Returns the defined directive corresponding to the name.
        :param name: name of the directive to return
        :type name: str
        :return: the defined directive
        :rtype: GraphQLDirective
        """
        return self._directive_definitions[name]

    def add_scalar_definition(
        self, scalar_definition: "GraphQLScalarType"
    ) -> None:
        """
        Adds a GraphQLScalarType to the defined scalar list.
        :param scalar_definition: GraphQLScalarType to add
        :type scalar_definition: GraphQLScalarType
        """
        if scalar_definition.name in self._scalar_definitions:
            raise RedefinedImplementation(
                "new GraphQL scalar definition `{}` "
                "overrides existing scalar definition `{}`.".format(
                    scalar_definition.name,
                    repr(self._scalar_definitions.get(scalar_definition.name)),
                )
            )
        self._scalar_definitions[scalar_definition.name] = scalar_definition
        self._input_types.append(scalar_definition.name)
        self.add_type_definition(scalar_definition)

    def find_scalar(self, name: str) -> Optional["GraphQLScalarType"]:
        """
        Returns the defined scalar corresponding to the name.
        :param name: name of the scalar to return
        :type name: str
        :return: the defined scalar
        :rtype: GraphQLScalarType
        """
        return self._scalar_definitions.get(name)

    def add_enum_definition(self, enum_definition: "GraphQLEnumType") -> None:
        """
        Adds a GraphQLScalarType to the defined scalar list.
        :param enum_definition: GraphQLEnumType to add
        :type enum_definition: GraphQLEnumType
        """
        if enum_definition.name in self._enum_definitions:
            raise RedefinedImplementation(
                "new GraphQL enum definition `{}` "
                "overrides existing enum definition `{}`.".format(
                    enum_definition.name,
                    repr(self._enum_definitions.get(enum_definition.name)),
                )
            )
        self._enum_definitions[enum_definition.name] = enum_definition
        self._input_types.append(enum_definition.name)
        self.add_type_definition(enum_definition)

    def get_field_by_name(self, name: str) -> "GraphQLField":
        """
        Returns the field corresponding to the filled in name.
        :param name: name of the field with the following format "Parent.field"
        :type name: str
        :return: the field corresponding to the filled in name
        :rtype: GraphQLField
        """
        try:
            parent_name, field_name = name.split(".")
        except ValueError:
            raise ImproperlyConfigured(
                "field name must be of the format `TypeName.fieldName` got "
                f"`{name}`."
            )

        try:
            return self.type_definitions[parent_name].find_field(field_name)
        except (AttributeError, KeyError):
            raise UnknownSchemaFieldResolver(
                f"field `{name}` was not found in GraphQL schema."
            )

    def _inject_introspection_fields(self) -> None:
        """
        Injects introspection fields to the query type and to defined object
        and union types.
        """
        query_type = self.type_definitions.get(self.query_operation_name)
        if not query_type:
            return

        query_type.add_field(
            SCHEMA_ROOT_FIELD_DEFINITION(
                gql_type=GraphQLNonNull("__Schema", schema=self)
            )
        )
        query_type.add_field(prepare_type_root_field(self))

        for type_definition in self.type_definitions.values():
            try:
                type_definition.add_field(
                    TYPENAME_ROOT_FIELD_DEFINITION(
                        gql_type=GraphQLNonNull(gql_type="String", schema=self)
                    )
                )
            except AttributeError:
                pass

    def _validate_schema_named_types(self) -> List[str]:
        """
        Validates that all type with fields refers to known GraphQL types.
        :return: a list of errors
        :rtype: List[str]
        """
        errors = []
        for type_name, gql_type in self.type_definitions.items():
            try:
                for field in gql_type.implemented_fields.values():
                    reduced_type = reduce_type(field.gql_type)
                    if str(reduced_type) not in self.type_definitions:
                        errors.append(
                            f"Field < {type_name}.{field.name} > is Invalid: "
                            f"the given Type < {reduced_type} > does not exist!"
                        )
            except AttributeError:
                pass
        return errors

    def _validate_object_follow_interfaces(self) -> List[str]:
        """
        Validates that object types which implements interfaces does follow
        their implementations.
        :return: a list of errors
        :rtype: List[str]
        """
        errors = []
        for gql_type in self.type_definitions.values():
            try:
                ifaces_names = gql_type.interfaces_names
            except AttributeError:
                continue

            for iface_name in ifaces_names:
                try:
                    iface_type = self.type_definitions[iface_name]
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

                for iface_field in iface_type.implemented_fields.values():
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
        """
        Validates that schema operation types are linked to defined types.
        :return: a list of errors
        :rtype: List[str]
        """
        errors = []
        # Check "query" which is the only mandatory root type
        if self.query_operation_name not in self.type_definitions:
            errors.append(
                f"Missing Query Type < {self.query_operation_name} >."
            )
        if (
            self.mutation_operation_name != "Mutation"
            and self.mutation_operation_name not in self.type_definitions
        ):
            errors.append(
                f"Missing Mutation Type < {self.mutation_operation_name} >."
            )
        if (
            self.subscription_operation_name != "Subscription"
            and self.subscription_operation_name not in self.type_definitions
        ):
            errors.append(
                f"Missing Subscription Type < {self.subscription_operation_name} >."
            )
        return errors

    def _validate_non_empty_object(self) -> List[str]:
        """
        Validates that object types implement at least one fields.
        :return: a list of errors
        :rtype: List[str]
        """
        errors = []
        for type_name, gql_type in self.type_definitions.items():
            if (
                isinstance(gql_type, GraphQLObjectType)
                and not gql_type.implemented_fields.values()
            ):
                errors.append(f"Type < {type_name} > has no fields.")
        return errors

    def _validate_union_is_acceptable(self) -> List[str]:
        """
        Validates that union types are valid.
        :return: a list of errors
        :rtype: List[str]
        """
        errors = []
        for type_name, gql_type in self.type_definitions.items():
            if isinstance(gql_type, GraphQLUnionType):
                for contained_type_name in gql_type.types:
                    if contained_type_name == type_name:
                        errors.append(
                            f"Union Type < {type_name} > contains itself."
                        )
                        # TODO: Are there other restrictions for `Union`s ?
                        # can they contain interfaces ?
                        # can they mix types: interface | object | scalar
        return errors

    def _validate_all_scalars_have_implementations(self) -> List[str]:
        """
        Validates that defined scalar types provide a proper implementation.
        :return: a list of errors
        :rtype: List[str]
        """
        errors = []
        for type_name, gql_type in self.type_definitions.items():
            if isinstance(gql_type, GraphQLScalarType):
                if (
                    gql_type.coerce_output is None
                    or gql_type.coerce_input is None
                    or gql_type.parse_literal is None
                ):
                    errors.append(
                        f"Scalar < {type_name} > "
                        f"is missing an implementation"
                    )
        return errors

    def _validate_enum_values_are_unique(self) -> List[str]:
        """
        Validates that enum values are unique for each enum types.
        :return: a list of errors
        :rtype: List[str]
        """
        errors = []
        for type_name, gql_type in self.type_definitions.items():
            if isinstance(gql_type, GraphQLEnumType):
                for value in gql_type.values:
                    if str(value.value) in self.type_definitions:
                        errors.append(
                            f"Enum < {type_name} > has a "
                            f"value of < {str(value.value)} > which "
                            f"is a Type"
                        )
        return errors

    def _validate_arguments_have_valid_type(self) -> List[str]:
        """
        Validates that argument definitions of fields and directives refer to
        an input type.
        :return: a list of errors
        :rtype: List[str]
        """
        errors = []
        for gqltype in self.type_definitions.values():
            try:
                for field in gqltype.implemented_fields.values():
                    for arg in field.arguments.values():
                        errors.extend(
                            self._validate_type_is_an_input_types(
                                arg,
                                f"Argument < {arg.name} > of Field < {gqltype}.{field.name} >",
                            )
                        )
            except AttributeError:
                pass

        for directive in self._directive_definitions.values():
            for arg in directive.arguments.values():
                errors.extend(
                    self._validate_type_is_an_input_types(
                        arg,
                        f"Argument < {arg.name} > of Directive < {directive.name} >",
                    )
                )

        return errors

    def _validate_type_is_an_input_types(
        self, obj: "GraphQLType", message_prefix: str
    ) -> List[str]:
        """
        Validates that the object is a defined input types.
        :param obj: object to check
        :param message_prefix: prefix to append to the error message
        :type obj: GraphQLType
        :type message_prefix: str
        :return: a list of errors
        :rtype: List[str]
        """
        rtype = reduce_type(obj.gql_type)
        if not rtype in self._input_types:
            return [
                f"{message_prefix} is of type "
                f"< {rtype} > which is not a Scalar, "
                "an Enum or an InputObject"
            ]
        return []

    def _validate_input_type_composed_of_input_type(self) -> List[str]:
        """
        Validates that each input fields of defined input object types refer to
        an input type.
        :return: a list of errors
        :rtype: List[str]
        """
        errors = []
        for typename in self._input_types:
            gqltype = self.type_definitions[typename]
            if isinstance(gqltype, GraphQLInputObjectType):
                for field in gqltype.input_fields.values():
                    errors.extend(
                        self._validate_type_is_an_input_types(
                            field, f"Field < {typename}.{field.name} >"
                        )
                    )
        return errors

    def _validate_directive_implementation(self) -> List[str]:
        """
        Validates that defined directives provide a proper implementation.
        :return: a list of errors
        :rtype: List[str]
        """
        errors = []
        for directive in self._directive_definitions.values():
            for expected in _IMPLEMENTABLE_DIRECTIVE_HOOKS:
                attr = getattr(directive.implementation, expected, None)
                if attr and not iscoroutinefunction(attr):
                    errors.append(
                        f"Directive {directive.name} Method {expected} is not awaitable"
                    )
        return errors

    def _validate(self) -> bool:
        """
        Check that the given schema is valid.
        :return: a boolean which determines whether or not the schema is valid
        :rtype: bool
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
            self._validate_directive_implementation
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

    async def _bake_types(
        self, custom_default_resolver: Optional[Callable] = None
    ) -> None:
        """
        Bakes types linked to the schema.
        :param custom_default_resolver: callable that will replace the builtin
        default_resolver (called as resolver for each UNDECORATED field)
        :type custom_default_resolver: Optional[Callable]
        """
        for scalar_definition in self._scalar_definitions.values():
            scalar_definition.bake(self)

        for type_definition in self.type_definitions.values():
            # Scalar types are already baked
            if not isinstance(type_definition, GraphQLScalarType):
                type_definition.bake(self)

        for directive_definition in self._directive_definitions.values():
            directive_definition.bake(self)

        for type_definition in self.type_definitions.values():
            if isinstance(
                type_definition,
                (GraphQLObjectType, GraphQLInterfaceType, GraphQLUnionType),
            ):
                await type_definition.bake_fields(
                    self, custom_default_resolver
                )
            elif isinstance(type_definition, GraphQLEnumType):
                await type_definition.bake_enum_values(self)

    def get_operation_root_type(
        self, operation: "OperationDefinitionNode"
    ) -> "GraphQLObjectType":
        """
        Extracts the root type of the operation from the schema.
        :param operation: AST operation definition node from which retrieve the
        root type
        :type operation: OperationDefinitionNode
        :return: the GraphQLObjectType instance related to the operation
        definition
        :rtype: GraphQLObjectType
        """
        try:
            return self._operation_types[operation.operation_type]
        except KeyError:
            raise graphql_error_from_nodes(
                "Schema is not configured for %ss." % operation.operation_type,
                nodes=operation,
            )

    async def bake(
        self,
        custom_default_resolver: Optional[Callable] = None,
        custom_default_type_resolver: Optional[Callable] = None,
    ) -> None:
        """
        Bake the final schema (it should not change after this) used for
        execution.
        :param custom_default_resolver: callable that will replace the builtin
        default_resolver
        :param custom_default_type_resolver: callable that will replace the
        tartiflette `default_type_resolver` (will be called on abstract types
        to deduct the type of a result)
        :type custom_default_resolver: Optional[Callable]
        :type custom_default_type_resolver: Optional[Callable]
        """
        self.default_type_resolver = (
            custom_default_type_resolver or default_type_resolver
        )
        self._inject_introspection_fields()
        try:
            await self._bake_types(custom_default_resolver)
        except Exception:  # pylint: disable=broad-except
            # Exceptions should be collected at validation time
            pass

        self._validate()

        # Bake introspection attributes
        self._operation_types = {
            "query": self.type_definitions.get(self.query_operation_name),
            "mutation": self.type_definitions.get(
                self.mutation_operation_name
            ),
            "subscription": self.type_definitions.get(
                self.subscription_operation_name
            ),
        }
        self.queryType = self._operation_types["query"]
        self.mutationType = self._operation_types["mutation"]
        self.subscriptionType = self._operation_types["subscription"]
        self.directives = list(self._directive_definitions.values())

        for type_name, type_definition in self.type_definitions.items():
            if not type_name.startswith("__"):
                self.types.append(type_definition)
