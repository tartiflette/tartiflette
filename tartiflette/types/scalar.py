from typing import Optional

from tartiflette.types.type import GraphQLType


class GraphQLScalarType(GraphQLType):
    """
    Scalar Type Definition

    The leaf values of any request and input values to arguments are
    Scalars (or Enums which are special Scalars) and are defined with a name
    and a series of functions used to convert to and from the request or SDL.

    Example: see the default Int, String or Boolean scalars.
    """

    __slots__ = (
        'name',
        'description',
        'serialize',
        'deserialize',
    )

    def __init__(self, name: str,
                 serialize: Optional[callable]=None,
                 deserialize: Optional[callable]= None,
                 description: Optional[str] = None):
        super().__init__(name=name, description=description)
        # TODO: Better validation
        # if not callable(serialize) or not callable(deserialize):
        #     raise TartifletteGraphQLTypeException(
        #         "Error while defining Scalar `{}`. "
        #         "You must provide `serialize` and `deserialize` functions.".
        #             format(name)
        #         , gql_type=self)

        self.serialize = serialize
        self.deserialize = deserialize

    def __repr__(self) -> str:
        return "{}(name={!r}, description={!r})".format(
            self.__class__.__name__, self.name, self.description,
        )

    def __eq__(self, other) -> bool:
        # TODO: Need to check if [de]serialize functions need to be equal
        return super().__eq__(other) and self.serialize == other.serialize and \
               self.deserialize == other.deserialize
