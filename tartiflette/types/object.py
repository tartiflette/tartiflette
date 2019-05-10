from typing import Any, Dict, List, Optional, Union

from tartiflette.types.field import GraphQLField
from tartiflette.types.helpers import (
    get_directive_instances,
    wraps_with_directives,
)
from tartiflette.types.type import GraphQLType
from tartiflette.utils.coercer_way import CoercerWay


class GraphQLObjectType(GraphQLType):
    """
    Object Type Definition

    Almost all of the GraphQL types you define will be object types.
    Object types are composite types and have a name,
    but most importantly describe their fields.
    """

    def __init__(
        self,
        name: str,
        fields: Dict[str, GraphQLField],
        interfaces: Optional[List[str]] = None,
        description: Optional[str] = None,
        schema: Optional["GraphQLSchema"] = None,
        directives: Optional[Dict[str, Union[str, Dict[str, Any]]]] = None,
    ) -> None:
        super().__init__(name=name, description=description, schema=schema)
        self._fields = fields
        # TODO: specify what is in the List.
        self.interfaces_names = interfaces or []
        self._interfaces = None
        self._directives = directives
        self._directives_implementations = {}

    def __repr__(self) -> str:
        return (
            "{}(name={!r}, fields={!r}, "
            "interfaces={!r}, description={!r})".format(
                self.__class__.__name__,
                self.name,
                self._fields,
                self.interfaces_names,
                self.description,
            )
        )

    def __eq__(self, other: Any) -> bool:
        return (
            super().__eq__(other)
            and self._fields == other._fields
            and self.interfaces_names == other.interfaces_names
        )

    def add_field(self, value: GraphQLField) -> None:
        self._fields[value.name] = value

    def find_field(self, name: str) -> GraphQLField:
        return self._fields[name]

    # Introspection Attribute
    @property
    def kind(self) -> str:
        return "OBJECT"

    # Introspection Attribute
    @property
    def fields(self) -> List[GraphQLField]:
        try:
            return [
                self._fields[x] for x in self._fields if not x.startswith("__")
            ]
        except (AttributeError, TypeError):
            pass
        return []

    def bake(self, schema: "GraphQLSchema") -> None:
        super().bake(schema)
        self._interfaces = []
        for interface_name in self.interfaces_names:
            interface = self._schema.find_type(interface_name)
            self._interfaces.append(interface)
            interface.possibleTypes.append(self)

        directives_definition = get_directive_instances(
            self._directives, self._schema
        )

        self._directives_implementations = {
            CoercerWay.OUTPUT: wraps_with_directives(
                directives_definition=directives_definition,
                directive_hook="on_pre_output_coercion",
            )
        }

        self._introspection_directives = wraps_with_directives(
            directives_definition=directives_definition,
            directive_hook="on_introspection",
        )

    def bake_fields(self, custom_default_resolver):
        for field in self._fields.values():
            try:
                field.bake(self._schema, self, custom_default_resolver)
            except AttributeError:
                pass

    # Introspection Attribute
    @property
    def interfaces(self) -> List[GraphQLType]:
        return self._interfaces or []

    @property
    def directives(self):
        return self._directives_implementations
