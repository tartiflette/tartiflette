from typing import Any, Callable, Dict, List, Optional, Union

from tartiflette.resolver.default import (
    default_type_resolver,
    gather_arguments_coercer,
)
from tartiflette.schema.introspection import (
    SCHEMA_ROOT_FIELD_DEFINITION,
    TYPENAME_ROOT_FIELD_DEFINITION,
    prepare_type_root_field,
)
from tartiflette.schema.registry import SchemaRegistry
from tartiflette.types.enum import GraphQLEnumType
from tartiflette.types.exceptions.tartiflette import (
    GraphQLSchemaError,
    ImproperlyConfigured,
    RedefinedImplementation,
    UnknownSchemaFieldResolver,
)
from tartiflette.types.helpers.get_directive_instances import (
    compute_directive_nodes,
)
from tartiflette.types.input_object import GraphQLInputObjectType
from tartiflette.types.interface import GraphQLInterfaceType
from tartiflette.types.non_null import GraphQLNonNull
from tartiflette.types.object import GraphQLObjectType
from tartiflette.types.scalar import GraphQLScalarType
from tartiflette.types.union import GraphQLUnionType
from tartiflette.utils.callables import (
    is_valid_async_generator,
    is_valid_coroutine,
)
from tartiflette.utils.directives import wraps_with_directives
from tartiflette.utils.errors import graphql_error_from_nodes
from tartiflette.validation.validate import validate_sdl

__all__ = ("GraphQLSchema",)


_DEFAULT_QUERY_OPERATION_NAME = "Query"
_DEFAULT_MUTATION_OPERATION_NAME = "Mutation"
_DEFAULT_SUBSCRIPTION_OPERATION_NAME = "Subscription"


_IMPLEMENTABLE_DIRECTIVE_FUNCTION_HOOKS = (
    "on_post_bake",
    "on_pre_interface_output_coercion",
    "on_pre_object_output_coercion",
    "on_pre_union_output_coercion",
    "on_pre_enum_type_output_coercion",
    "on_pre_enum_value_output_coercion",
    "on_pre_scalar_output_coercion",
    "on_pre_output_coercion",
    "on_introspection",
    "on_post_input_object_coercion",
    "on_post_input_field_coercion",
    "on_post_enum_type_input_coercion",
    "on_post_enum_value_input_coercion",
    "on_post_scalar_input_coercion",
    "on_post_input_coercion",
    "on_post_argument_coercion",
    "on_field_execution",
    "on_field_collection",
    "on_fragment_spread_collection",
    "on_inline_fragment_collection",
    "on_schema_execution",
)

_IMPLEMENTABLE_DIRECTIVE_GENERATOR_HOOKS = ("on_schema_subscription",)


def _format_schema_error_message(errors: List["TartifletteError"]) -> str:
    result = "\n"
    for index, err in enumerate(errors):
        result = "{result}\n{index}: {err}".format(
            result=result, index=index, err=str(err),
        )
    return result


class GraphQLSchema:
    """
    GraphQL Schema

    Contains the complete GraphQL Schema: types, entrypoints and directives.
    """

    # pylint: disable=too-many-instance-attributes

    # Introspection attributes
    description = (
        "A GraphQL Schema defines the capabilities of a GraphQL server. It"
        "exposes all available types and directives on the server, as well as"
        "the entry points for query, mutation, and subscription operations."
    )

    def __init__(self, name: str = "default") -> None:
        """
        :param name: name of the schema
        :type name: str
        """
        self.name = name
        self.default_type_resolver: Optional[Callable] = None
        self.default_arguments_coercer: Optional[Callable] = None
        self.coerce_list_concurrently: Optional[bool] = None

        # Operation type names
        self.query_operation_name: str = _DEFAULT_QUERY_OPERATION_NAME
        self.mutation_operation_name: str = _DEFAULT_MUTATION_OPERATION_NAME
        self.subscription_operation_name: str = (
            _DEFAULT_SUBSCRIPTION_OPERATION_NAME
        )

        # Type, directive, enum, scalar & input type definitions
        self.type_definitions: Dict[str, "GraphQLType"] = {}
        self.directive_definitions: Dict[str, "GraphQLDirective"] = {}
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
        self.directives: List[
            "GraphQLDirective"
        ] = []  # pylint: disable=invalid-name

        self.extensions: List["GraphQLExtension"] = []
        self._schema_directives: List["DirectiveNode"] = []
        self.document_node: Optional["DocumentNode"] = None

    def add_schema_directives(
        self, directives_instances: List["DirectiveNode"]
    ) -> None:
        self._schema_directives.extend(directives_instances)

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
        if directive_definition.name in self.directive_definitions:
            raise RedefinedImplementation(
                "new GraphQL directive definition `{}` "
                "overrides existing directive definition `{}`.".format(
                    directive_definition.name,
                    repr(
                        self.directive_definitions.get(
                            directive_definition.name
                        )
                    ),
                )
            )
        self.directive_definitions[
            directive_definition.name
        ] = directive_definition

    def has_directive(self, name: str) -> bool:
        """
        Determines whether or not the name corresponds to a defined directive.
        :param name: name of the directive to find
        :type name: str
        :return: whether or not the name corresponds to a defined directive
        :rtype: bool
        """
        return name in self.directive_definitions

    def find_directive(self, name: str) -> "GraphQLDirective":
        """
        Returns the defined directive corresponding to the name.
        :param name: name of the directive to return
        :type name: str
        :return: the defined directive
        :rtype: GraphQLDirective
        """
        return self.directive_definitions[name]

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
        Adds a GraphQLEnumType to the defined enum definitions list.
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

    def add_extension(self, extension: "GraphQLExtension") -> None:
        """
        Adds a GraphQLExtension to the defined extensions list.
        :param extension: GraphQLExtension to add
        :type extension: GraphQLExtension
        """
        self.extensions.append(extension)

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

    def _validate_all_scalars_have_implementations(self) -> List[str]:
        """
        Validates that defined scalar types provide a proper implementation.
        :return: a list of errors
        :rtype: List[str]
        """
        errors = []
        for type_name, gql_type in self.type_definitions.items():
            if isinstance(gql_type, GraphQLScalarType) and (
                gql_type.coerce_output is None
                or gql_type.coerce_input is None
                or gql_type.parse_literal is None
            ):
                errors.append(
                    f"Scalar < {type_name} > " f"is missing an implementation"
                )
        return errors

    def _validate_directive_implementation(self) -> List[str]:
        """
        Validates that defined directives provide a proper implementation.
        :return: a list of errors
        :rtype: List[str]
        """
        errors = []
        for directive in self.directive_definitions.values():
            for expected in _IMPLEMENTABLE_DIRECTIVE_FUNCTION_HOOKS:
                attr = getattr(directive.implementation, expected, None)
                if attr and not is_valid_coroutine(attr):
                    errors.append(
                        f"Directive {directive.name} Method "
                        f"{expected} is not awaitable."
                    )

            for expected in _IMPLEMENTABLE_DIRECTIVE_GENERATOR_HOOKS:
                attr = getattr(directive.implementation, expected, None)
                if attr and not is_valid_async_generator(attr):
                    errors.append(
                        f"Directive {directive.name} Method "
                        f"{expected} is not an Async Generator."
                    )

        return errors

    def _validate_implementations(self) -> bool:
        """
        Check that the given scalars and directives have implementations.
        :return: a boolean which determines whether or not the schema is valid
        :rtype: bool
        """
        validators = [
            self._validate_all_scalars_have_implementations,
            self._validate_directive_implementation,
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

        for directive_definition in self.directive_definitions.values():
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
            elif isinstance(type_definition, GraphQLInputObjectType):
                await type_definition.bake_input_fields(self)

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

    def _bake_extensions(self):
        for extension in self.extensions:
            extension.bake(self)

    def bake_executor(self, executor):
        return wraps_with_directives(
            directives_definition=compute_directive_nodes(
                self, self._schema_directives
            ),
            directive_hooks=["on_schema_execution"],
            func=executor,
            is_resolver=True,
        )

    def bake_subscriptor(self, subscriptor):
        return wraps_with_directives(
            directives_definition=compute_directive_nodes(
                self, self._schema_directives
            ),
            directive_hooks=["on_schema_subscription"],
            func=subscriptor,
            is_async_generator=True,
        )

    async def bake(
        self,
        custom_default_resolver: Optional[Callable] = None,
        custom_default_type_resolver: Optional[Callable] = None,
        custom_default_arguments_coercer: Optional[Callable] = None,
        coerce_list_concurrently: Optional[bool] = None,
    ) -> None:
        """
        Bake the final schema (it should not change after this) used for
        execution.
        :param custom_default_resolver: callable that will replace the builtin
        default_resolver
        :param custom_default_type_resolver: callable that will replace the
        tartiflette `default_type_resolver` (will be called on abstract types
        to deduct the type of a result)
        :param custom_default_arguments_coercer: callable that will replace the
        tartiflette `default_arguments_coercer`
        :param coerce_list_concurrently: whether or not list will be coerced
        concurrently
        :type custom_default_resolver: Optional[Callable]
        :type custom_default_type_resolver: Optional[Callable]
        :type custom_default_arguments_coercer: Optional[Callable]
        :type coerce_list_concurrently: Optional[bool]
        """
        self.default_type_resolver = (
            custom_default_type_resolver or default_type_resolver
        )
        self.default_arguments_coercer = (
            custom_default_arguments_coercer or gather_arguments_coercer
        )
        self.coerce_list_concurrently = (
            coerce_list_concurrently
            if coerce_list_concurrently is not None
            else True
        )
        self._inject_introspection_fields()

        errors = validate_sdl(self.document_node)
        if errors:
            raise GraphQLSchemaError(
                message=_format_schema_error_message(errors)
            )

        try:
            self._bake_extensions()
        except Exception:  # pylint: disable=broad-except
            # Exceptions should be collected at validation time
            pass

        SchemaRegistry.bake_registered_objects(self)

        try:
            await self._bake_types(custom_default_resolver)
        except Exception:  # pylint: disable=broad-except
            # Exceptions should be collected at validation time
            pass

        self._validate_implementations()

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
        self.directives = list(self.directive_definitions.values())

        for type_name, type_definition in self.type_definitions.items():
            if not type_name.startswith("__"):
                self.types.append(type_definition)
