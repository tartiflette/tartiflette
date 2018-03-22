from collections import OrderedDict
from typing import Dict, Optional, List

from tartiflette.types.exceptions.tartiflette import \
    TartifletteGraphQLTypeException
from tartiflette.types.field import GraphQLField
from tartiflette.types.type import GraphQLType


class GraphQLObjectType(GraphQLType):
    """
    Object Type Definition

    Almost all of the GraphQL types you define will be object types.
    Object types are composite types and have a name,
    but most importantly describe their fields.
    """

    __slots__ = (
        'name',
        'description',
        '_fields',
        '_interfaces',
    )

    def __init__(self, name: str, fields: Dict[str, GraphQLField],
                 interfaces: Optional[List[str]]=None,
                 description: Optional[str]=None):
        # In the function signature above, it should be `OrderedDict` but the
        # python 3.6 interpreter fails to interpret the signature correctly.
        super().__init__(name=name, description=description)
        self._fields: Dict[str, GraphQLField] = fields
        # TODO: specify what is in the List.
        self._interfaces: Optional[List] = interfaces

    def __repr__(self) -> str:
        return "{}(name={!r}, fields={!r}, " \
               "interfaces={!r}, description={!r})".format(
            self.__class__.__name__,
            self.name, self._fields, self._interfaces, self.description,
        )

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.fields == other.fields and \
               self.interfaces == other.interfaces

    @property
    def fields(self) -> Dict[str, GraphQLField]:
        return self._fields

    @fields.setter
    def fields(self, value) -> None:
        self._fields = OrderedDict(value)

    @property
    def interfaces(self) -> List:
        return self._interfaces

    @interfaces.setter
    def interfaces(self, value) -> None:
        if not isinstance(value, list):
            raise TartifletteGraphQLTypeException(
                "Error while defining Object `{}`."
                "The provided `interfaces` should be a list.".format(self.name),
                gql_type=self)
        self._interfaces = value
