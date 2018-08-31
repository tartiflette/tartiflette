from typing import Dict, List, Optional

from tartiflette.types.field import GraphQLField
from tartiflette.types.type import GraphQLType


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
    ):
        # In the function signature above, it should be `OrderedDict` but the
        # python 3.6 interpreter fails to interpret the signature correctly.
        super().__init__(name=name, description=description)
        self.fields: Dict[str, GraphQLField] = fields
        # TODO: specify what is in the List.
        self.interfaces: Optional[List[str]] = interfaces

    def __repr__(self) -> str:
        return (
            "{}(name={!r}, fields={!r}, "
            "interfaces={!r}, description={!r})".format(
                self.__class__.__name__,
                self.name,
                self.fields,
                self.interfaces,
                self.description,
            )
        )

    def __eq__(self, other) -> bool:
        return (
            super().__eq__(other)
            and self.fields == other.fields
            and self.interfaces == other.interfaces
        )

    def add_field(self, value: GraphQLField):
        self.fields[value.name] = value
