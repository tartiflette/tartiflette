from typing import Optional, Dict, List

from tartiflette.sdl.transformers.helpers import reduce_gql_type
from tartiflette.sdl.transformers.schema import Description, \
    GraphQLBaseObject, GraphQLNamedType, GraphQLDirectiveDefinition, \
    GraphQLNamedTypeDefinition, GraphQLFieldDefinition, \
    GraphQLObjectTypeDefinition, GraphQLInputObjectTypeDefinition, \
    GraphQLInterfaceTypeDefinition


class GraphQLSchema(GraphQLBaseObject):
    """
    GraphQL Schema

    Contains the complete GraphQL Schema: types, entrypoints and directives.
    """

    __slots__ = [
        '_query_type',
        '_mutation_type',
        '_subscription_type',
        '_directives',
        '_gql_types',
        '_implementations',
        '_possible_types',
    ]

    def __init__(self, *args, **kwargs):
        kwargs["description"] = Description(
            description="A GraphQL Schema contains the complete definition "
            "of the GraphQL structure: types, entrypoints (query, "
            "mutation, subscription)."
        )
        super(GraphQLSchema, self).__init__(**kwargs)
        # Schema entry points
        self._query_type: Optional[GraphQLNamedType] = \
            GraphQLNamedType(name="Query")
        self._mutation_type: Optional[GraphQLNamedType] = \
            GraphQLNamedType(name="Mutation")
        self._subscription_type: Optional[GraphQLNamedType] = \
            GraphQLNamedType(name="Subscription")
        # Directives
        self._directives: Dict[str, GraphQLDirectiveDefinition] = {}
        # Types, definitions and implementations
        self._gql_types: Dict[str, GraphQLNamedTypeDefinition] = {}
        # All `GraphQLObjectType`s implementing a given interface
        self._implementations: Dict[str, List[GraphQLNamedTypeDefinition]] = {}
        # All non-abstract types possible for a given abstract type
        self._possible_types: Dict[str, Dict[str, bool]] = {}

    def __repr__(self):
        return "GraphQLSchema(query: {}, " \
               "mutation: {}, " \
               "subscription: {}, " \
               "types: {}, " \
               "directives: {})".format(
                self._query_type,
                self._mutation_type,
                self.subscription_type,
                self._gql_types,
                self._directives,
                )

    def __eq__(self, other):
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
    def query_type(self) -> Optional[GraphQLNamedType]:
        return self._query_type

    @query_type.setter
    def query_type(self, value: GraphQLNamedType) -> None:
        if not isinstance(value, GraphQLNamedType):
            raise ValueError(
                'Schema `query` must be a '
                '`GraphQLNamedType`, got `{}`'.format(
                    value.__class__.__name__
                )
            )
        self._query_type = value

    @property
    def mutation_type(self) -> Optional[GraphQLNamedType]:
        return self._mutation_type

    @mutation_type.setter
    def mutation_type(self, value: GraphQLNamedType) -> None:
        if not isinstance(value, GraphQLNamedType):
            raise ValueError(
                'Schema `mutation` must be a '
                '`GraphQLNamedType`, got `{}`'.format(
                    value.__class__.__name__
                )
            )
        self._mutation_type = value

    @property
    def subscription_type(self) -> Optional[GraphQLNamedType]:
        return self._subscription_type

    @subscription_type.setter
    def subscription_type(self, value: GraphQLNamedType) -> None:
        if not isinstance(value, GraphQLNamedType):
            raise ValueError(
                'Schema `subscription` must be a '
                '`GraphQLNamedType`, got `{}`'.format(
                    value.__class__.__name__
                )
            )
        self._subscription_type = value

    def add_definition(self, value: GraphQLNamedTypeDefinition) -> None:
        # TODO: Check stuff, call update_schema after each new definition ?
        self._gql_types[value.name] = value

    def get_field_by_name(self, name: str) -> Optional[GraphQLFieldDefinition]:
        name_parts = name.split('.')
        if len(name_parts) == 1:
            object_name = self._query_type.name
            field_name = name_parts[0]
        elif len(name_parts) == 2:
            object_name, field_name = name_parts
        else:
            raise ValueError(
                'Field name must be of the format '
                '`ObjectName.fieldName` or `fieldName`, '
                'got `{}`'.format(name)
            )
        object_type_def = self._gql_types.get(object_name)
        if isinstance(
            object_type_def,
            (GraphQLObjectTypeDefinition, GraphQLInputObjectTypeDefinition)
        ):
            field = object_type_def.fields.get(field_name)
            if field:
                return field
        raise ValueError('Field `{}` not found in schema.'.format(name))

    def update_schema(self) -> None:
        """
        Updates the schema given all the defined types: compute interfaces and
        unions.

        :return: None
        """
        pass

    def validate_schema(self) -> bool:
        """
        Check that the given schema is valid. Maybe store this in a cached value
        like __validation_errors: List[Errors]

        :return: bool
        """
        validators = [
            self._validate_schema_named_types,
            self._validate_object_follow_interfaces,
            self._validate_schema_root_types_exist,
            self._validate_non_empty_object,
        ]
        for validator in validators:
            res = validator()
            if not res:
                return False
        return True

        # Validate custom Scalar has an implementation (do it here ?)
        # Validate Enum: a keys is not in the GraphQL default scalars or a
        #     custom scalar, it has to be "unique"
        # Validate Union: cannot contain itself and must be of concrete types (check if this is true)
        # Validate Field: default value must be of given type
        #
        pass

    def print_sdl(self):
        pass

    def _validate_schema_named_types(self):
        for obj_name, gtype in self._gql_types.items():
            # TODO: Make all types that have "fields" inherit from the same one
            if isinstance(gtype, (GraphQLObjectTypeDefinition,
                                  GraphQLInterfaceTypeDefinition,
                                  GraphQLInputObjectTypeDefinition)) and \
                    gtype.fields:
                for field_name, field in gtype.fields.items():
                    leaf_gqlt = reduce_gql_type(field.gql_type)
                    if leaf_gqlt.name not in self._gql_types\
                            and leaf_gqlt.name not in ['ID', 'Int', 'Float',
                                                       'Boolean', 'String']:
                        # TODO: Remove "native" types here and set them
                        # automatically at import time.
                        raise ValueError(
                            "Field `{}` in object `{}` is invalid. "
                            "The given type `{}` does not exist !".format(
                                field_name, obj_name, field.gql_type
                            )
                        )
        return True

    def _validate_object_follow_interfaces(self):
        for obj_name, gtype in self._gql_types.items():
            if isinstance(gtype, GraphQLObjectTypeDefinition):
                if gtype.interfaces:
                    for interface_namedtype in gtype.interfaces:
                        interface = self._gql_types.get(
                            interface_namedtype.name
                        )
                        if isinstance(
                            interface, GraphQLInterfaceTypeDefinition
                        ):
                            for ifa_field_name, ifa_field in interface.fields.items(
                            ):
                                if ifa_field_name in gtype.fields:
                                    # compare type declaration
                                    obj_field = gtype.fields.get(
                                        ifa_field_name
                                    )
                                    if obj_field.gql_type != ifa_field.gql_type:
                                        raise ValueError(
                                            "Field `{}` in object `{}` "
                                            "is invalid. The interface "
                                            "`{}` constraints the field to a "
                                            "`{}` type, got `{}`".format(
                                                ifa_field_name, obj_name,
                                                interface.name,
                                                ifa_field.gql_type,
                                                obj_field.gql_type
                                            )
                                        )
                                else:
                                    raise ValueError(
                                        "Field `{}` in object `{}` "
                                        "is missing. The interface `{}` "
                                        "expects a `{}` field of type "
                                        "`{}`".format(
                                            ifa_field_name, obj_name,
                                            interface.name, ifa_field.name,
                                            ifa_field.gql_type
                                        )
                                    )
        return True

    def _validate_schema_root_types_exist(self):
        # Check query, this is mandatory
        if self._query_type.name not in self._gql_types.keys():
            raise ValueError(
                "Schema could not find root query type "
                "`{}`".format(self._query_type.name)
            )
        elif self._mutation_type.name != "Mutation" and \
            self._mutation_type.name not in self._gql_types.keys():
            raise ValueError(
                "Schema could not find root mutation type "
                "`{}`".format(self._query_type.name)
            )
        elif self._subscription_type.name != "Subscription" and \
            self._subscription_type.name not in self._gql_types.keys():
            raise ValueError(
                "Schema could not find root subscription type "
                "`{}`".format(self._query_type.name)
            )
        return True

    def _validate_non_empty_object(self):
        for obj_name, gtype in self._gql_types.items():
            if isinstance(gtype, GraphQLObjectTypeDefinition):
                if len(gtype.fields) == 0:
                    raise ValueError(
                        "Object `{}` has no fields.".format(obj_name)
                    )
        return True


DefaultGraphQLSchema = GraphQLSchema()
