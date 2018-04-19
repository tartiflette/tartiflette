import traceback
from typing import Optional, Dict, List, Union

from tartiflette.executors.types import ExecutionData
from tartiflette.types.builtins import GraphQLBoolean, GraphQLFloat, GraphQLID, \
    GraphQLInt, GraphQLString
from tartiflette.types.exceptions.tartiflette import \
    GraphQLSchemaError, InvalidValue, GraphQLError
from tartiflette.types.field import GraphQLField
from tartiflette.types.helpers import reduce_type
from tartiflette.types.interface import GraphQLInterfaceType
from tartiflette.types.list import GraphQLList
from tartiflette.types.non_null import GraphQLNonNull
from tartiflette.types.object import GraphQLObjectType
from tartiflette.types.type import GraphQLType
from tartiflette.types.union import GraphQLUnionType


class GraphQLSchema:
    """
    GraphQL Schema

    Contains the complete GraphQL Schema: types, entrypoints and directives.
    """

    __slots__ = [
        'description',
        '_query_type',
        '_mutation_type',
        '_subscription_type',
        '_gql_types',
        '_implementations',
        '_possible_types',
    ]

    def __init__(self, description=None):
        self.description = description
        if not description:
            self.description = "A GraphQL Schema contains the complete definition "
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
        return "GraphQLSchema(query: {}, " \
               "mutation: {}, " \
               "subscription: {}, " \
               "types: {})".format(
                self._query_type,
                self._mutation_type,
                self.subscription_type,
                self._gql_types,
                )

    def __eq__(self, other):
        if not type(self) is type(other):
            return False
        if self._query_type != other._query_type or \
                self._mutation_type != other._mutation_type or \
                self._subscription_type != other._subscription_type:
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
        # TODO: Check stuff, call update_schema after each new definition ?
        if self._gql_types.get(value.name):
            raise ValueError('new GraphQL type definition `{}` '
                             'overrides existing type definition `{}`.'.format(
                                value.name,
                                repr(self._gql_types.get(value.name))
            ))
        self._gql_types[value.name] = value

    def to_real_type(self, gql_type: Union[str, GraphQLNonNull, GraphQLList]):
        # TODO: Execute this at schema build time, performance issue !
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

    def collect_field_value(self, field, resolved_value, execution_data: ExecutionData):
        # TODO: Execute the below conversion (to_real_type) at schema build time,
        # big performance issue !
        real_type = self.to_real_type(field.gql_type)
        try:
            result = real_type.collect_value(resolved_value)
        except NotImplementedError:
            result = resolved_value

        if isinstance(result, list):
            # TODO: Make this cleaner. Too many "useless" loops in
            # fields, executor & resolvers.
            # TODO: Also, we append the index in the path both here and in the
            # NodeField (we need it for errors but we can probably do better)
            new_result = []
            for index, res in enumerate(result):
                if isinstance(res, InvalidValue):
                    execution_data.path.append(index)
                    new_result.append(InvalidValue(res.value,
                                      gql_type=real_type,
                                      field=field, path=execution_data.path))
                else:
                    new_result.append(res)
            return new_result

        if isinstance(result, InvalidValue):
            return InvalidValue(result.value,
                                gql_type=real_type,
                                field=field, path=execution_data.path)
        return result

    def get_resolver(self, field_path: str) -> Optional[callable]:
        if not field_path:
            return None
        field_path_pieces = field_path.split('.')
        if not self._gql_types.get(field_path_pieces[0]):
            field_path_pieces.insert(0, self._query_type)
        field = self.get_field_by_name('.'.join(field_path_pieces[0:2]))
        while field_path_pieces[-1] != getattr(field, 'name', None):
            if not field:
                break
            field_path_pieces = [reduce_type(field.gql_type)] + field_path_pieces[2:]
            field = self.get_field_by_name(".".join(field_path_pieces[0:2]))
        if field:
            return field.resolver
        return None

    def get_field_by_name(self, name: str) -> Optional[GraphQLField]:
        try:
            object_name, field_name = name.split('.')
        except ValueError as err:
            raise ValueError(
                'field name must be of the format '
                '`TypeName.fieldName` got `{}`.'.format(name)
            ) from err

        try:
            return self._gql_types[object_name].fields[field_name]
        except (AttributeError, KeyError):
            pass
        return None

    def update_schema(self) -> None:
        """
        Updates the schema given all the defined types: compute interfaces and
        unions.

        :return: None
        """
        # TODO: To do :)
        pass

    def validate_schema(self) -> bool:
        """
        Check that the given schema is valid.

        :return: bool
        """
        # TODO: Maybe store this in a cached value
        # like __validation_errors: List[Errors]
        validators = [
            self._validate_schema_named_types,
            self._validate_object_follow_interfaces,
            self._validate_schema_root_types_exist,
            self._validate_non_empty_object,
            self._validate_union_is_acceptable,
            # TODO: Validate custom Scalar has an implementation
            # TODO: Validate Enum: a key should not use other NamedTypes or
            # reserved words, check Unions of Enums also !
            # TODO: Validate Field: default value must be of given type
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
                    if gql_type not in self._gql_types:
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
                                gql_type.name, iface_name,
                            )
                        )
                    for iface_field_name, iface_field in iface_type.fields.items():
                        try:
                            gql_type_field = gql_type.fields[iface_field_name]
                        except KeyError:
                            raise GraphQLSchemaError(
                                "field `{}` is missing in GraphQL type `{}` "
                                "that implements the `{}` interface.".format(
                                    iface_field_name, gql_type.name, iface_name,
                                )
                            )
                        if gql_type_field.gql_type != iface_field.gql_type:
                            raise GraphQLSchemaError(
                                "field `{}` in GraphQL type `{}` that "
                                "implements the `{}` interface does not follow "
                                "the interface field type `{}`.".format(
                                    iface_field_name, gql_type.name, iface_name,
                                    iface_field.gql_type
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
        elif self.mutation_type != "Mutation" and \
                self.mutation_type not in self._gql_types.keys():
            raise GraphQLSchemaError(
                "schema could not find the root `mutation` type `{}`.".format(
                    self.mutation_type
                )
            )
        elif self.subscription_type != "Subscription" and \
                self.subscription_type not in self._gql_types.keys():
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
                    "object type `{}` has no fields.".format(
                        type_name
                    )
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


DefaultGraphQLSchema = GraphQLSchema()
