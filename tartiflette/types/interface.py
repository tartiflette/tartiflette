from typing import Dict, Optional

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
        schema=None,
    ):
        super().__init__(name=name, description=description, schema=schema)
        self._fields: Dict[str, GraphQLField] = fields

    def __repr__(self) -> str:
        return "{}(name={!r}, fields={!r}, description={!r})".format(
            self.__class__.__name__, self.name, self._fields, self.description
        )

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self._fields == other._fields

    @property
    def kind(self):
        return "INTERFACE"

    @property
    def fields_dict(self):
        return self._fields

    def get_field(self, name: str) -> GraphQLField:
        return self._fields[name]

    @property
    def fields(self):
        try:
            return [x for _, x in self._fields.items()]
        except AttributeError:
            return []
