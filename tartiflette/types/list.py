from typing import Any, Optional, Union

from tartiflette.executors.types import Info
from tartiflette.types.exceptions.tartiflette import NullError, InvalidValue
from tartiflette.types.type import GraphQLType


class GraphQLList(GraphQLType):
    """
    List Container
    A GraphQLList is a container, wrapping type that points at another type.
    The type contained will be returned as a list instead of a single item.
    """

    def __init__(
        self,
        gql_type: Union[str, GraphQLType],
        description: Optional[str] = None,
    ):
        super().__init__(name=None, description=description)
        self.gql_type = gql_type

    def __repr__(self) -> str:
        return "{}(gql_type={!r}, description={!r})".format(
            self.__class__.__name__, self.gql_type, self.description
        )

    def __str__(self):
        return "[{!s}]".format(self.gql_type)

    def __eq__(self, other):
        return super().__eq__(other) and self.gql_type == other.gql_type

    def coerce_value(self, value: Any, info: Info) -> Any:
        if value is None:
            return value
        try:
            results = []
            for index, item in enumerate(value):
                try:
                    results.append(self.gql_type.coerce_value(
                        item, info.clone_with_path(index)
                    ))
                except NullError as e:
                    info.execution_ctx.add_error(e)
                    return None
                except InvalidValue as e:
                    results.append(None)
                    info.execution_ctx.add_error(e)
            return results
        except TypeError:
            # GraphQLList accepts values of 1 element
            # see the GraphQL.js implementation
            pass
        return [self.gql_type.coerce_value(value, info)]
