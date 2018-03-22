from typing import Optional, Any


class GraphQLArgument:
    """
    Argument Definition

    Arguments are used for:
      - GraphQLField resolvers
      - GraphQLInputObject fields
    """

    __slots__ = (
        'name',
        'description',
        'gql_type',
        'default_value',
    )

    def __init__(self, name: str, gql_type: str,
                 default_value: Optional[Any]=None,
                 description: Optional[str]=None):
        # TODO: Narrow the default_value type ?
        self.name = name
        self.gql_type = gql_type
        self.default_value = default_value
        self.description = description

    def __repr__(self):
        return "{}(name={!r}, gql_type={!r}, " \
               "default_value={!r}, description={!r})".format(
            self.__class__.__name__,
            self.name, self.gql_type,
            self.default_value, self.description
        )

    def __eq__(self, other):
        return self is other or (
                type(self) is type(other) and
                self.name == other.name and
                self.gql_type == other.gql_type and
                self.default_value == other.default_value
            )
