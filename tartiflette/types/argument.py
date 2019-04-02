from functools import partial
from typing import Any, Dict, List, Optional, Union

from tartiflette.types.helpers import get_directive_implem_list
from tartiflette.types.type import GraphQLType
from tartiflette.utils.arguments import (
    argument_coercer,
    surround_with_argument_execution_directives,
)
from tartiflette.utils.coercer import CoercerWay, get_coercer


class GraphQLArgument:
    """
    Argument Definition

    Arguments are used for:
      - GraphQLField resolvers
      - GraphQLInputObject fields
    """

    def __init__(
        self,
        name: str,
        gql_type: Union[str, GraphQLType],
        default_value: Optional[Any] = None,
        description: Optional[str] = None,
        directives: Optional[Dict[str, Optional[dict]]] = None,
        schema=None,
    ) -> None:
        # TODO: Narrow the default_value type ?
        self.name = name
        self.gql_type = gql_type
        self.default_value = default_value
        self.description = description
        self._type = {}
        self._schema = schema
        self._directives = directives
        self.coercer = None

        # Introspection Attribute
        self._directives_implementations = None

    def __repr__(self) -> str:
        return (
            "{}(name={!r}, gql_type={!r}, "
            "default_value={!r}, description={!r}, directives={!r})".format(
                self.__class__.__name__,
                self.name,
                self.gql_type,
                self.default_value,
                self.description,
                self.directives,
            )
        )

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other: Any) -> bool:
        return self is other or (
            type(self) is type(other)
            and self.name == other.name
            and self.gql_type == other.gql_type
            and self.default_value == other.default_value
            and self.directives == other.directives
        )

    @property
    def schema(self) -> "GraphQLSchema":
        return self._schema

    # Introspection Attribute
    @property
    def type(self) -> dict:
        return self._type

    @property
    def directives(self) -> List[Dict[str, Any]]:
        return self._directives_implementations

    @property
    def is_required(self) -> bool:
        if not isinstance(self.gql_type, GraphQLType):
            return False
        return self.gql_type.is_not_null and self.default_value is None

    @property
    def defaultValue(self) -> Any:  # pylint: disable=invalid-name
        return self.default_value

    def bake(self, schema: "GraphQLSchema") -> None:
        self._schema = schema
        self._directives_implementations = get_directive_implem_list(
            self._directives, self._schema
        )
        if isinstance(self.gql_type, GraphQLType):
            self._type = self.gql_type
        else:
            self._type["name"] = self.gql_type
            self._type["kind"] = self._schema.find_type(self.gql_type).kind

        self.coercer = partial(
            surround_with_argument_execution_directives(
                partial(
                    argument_coercer,
                    input_coercer=get_coercer(
                        self, schema=schema, way=CoercerWay.INPUT
                    ),
                ),
                self.directives,
            ),
            self,
        )
