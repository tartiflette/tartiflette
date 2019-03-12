from typing import Any, Callable, Dict, List, Optional

from tartiflette.types.field import GraphQLField
from tartiflette.types.type import GraphQLType


class GraphQLInterfaceType(GraphQLType):
    """
    Interface Type Definition

    It's an abstract type meaning that its purpose is to define a contract
    and enforce it on one or many fields of an Object type.
    The Interface type is used to describe what types are possible,
    what fields are in common across all types, as well as a
    function to determine which type is actually used
    when the field is resolved.
    """

    def __init__(
        self,
        name: str,
        fields: Dict[str, GraphQLField],
        description: Optional[str] = None,
        schema: Optional["GraphQLSchema"] = None,
    ) -> None:
        super().__init__(name=name, description=description, schema=schema)
        self._fields = fields
        self._possible_types = []

    def __repr__(self) -> str:
        return "{}(name={!r}, fields={!r}, description={!r})".format(
            self.__class__.__name__, self.name, self._fields, self.description
        )

    def __eq__(self, other: Any) -> bool:
        return super().__eq__(other) and self._fields == other._fields

    # Introspection Attribute
    @property
    def kind(self) -> str:
        return "INTERFACE"

    def find_field(self, name: str) -> GraphQLField:
        return self._fields[name]

    @property
    def fields(self) -> List[GraphQLField]:
        try:
            return [
                self._fields[x] for x in self._fields if not x.startswith("__")
            ]
        except (AttributeError, TypeError):
            pass
        return []

    def bake(
        self,
        schema: "GraphQLSchema",
        custom_default_resolver: Optional[Callable],
    ) -> None:
        super().bake(schema, custom_default_resolver)

        for field in list(self._fields.values()):
            field.bake(schema, self, custom_default_resolver)

    # introspection attribute
    @property
    def possibleTypes(self) -> list:  # pylint: disable=invalid-name
        return self._possible_types
