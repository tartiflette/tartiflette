from typing import Any, Dict, List, Optional, Union

from tartiflette.types.helpers import (
    get_directive_instances,
    wraps_with_directives,
)
from tartiflette.types.type import GraphQLType
from tartiflette.utils.coercer_way import CoercerWay


class GraphQLEnumValue:
    """
    Enums are special leaf values.
    `GraphQLEnumValue`s is a way to represent them.
    """

    def __init__(
        self,
        value: Any = None,
        description: Optional[str] = None,
        directives: Optional[Dict[str, Union[str, Dict[str, Any]]]] = None,
    ) -> None:
        self.value = value
        self.description = description
        self._directives = directives
        self._schema = None
        self._directives_implementations = None
        self._introspection_directives = None

        # Introspection Attribute
        self.isDeprecated = False  # pylint: disable=invalid-name

    def __repr__(self) -> str:
        return "{}(value={!r}, description={!r})".format(
            self.__class__.__name__, self.value, self.description
        )

    def __str__(self) -> str:
        return str(self.value)

    def __eq__(self, other: Any) -> bool:
        return self is other or (
            type(self) is type(other) and self.value == other.value
        )

    # Introspection Attribute
    @property
    def name(self) -> str:
        return self.value

    @property
    def directives(self) -> List[Dict[str, Any]]:
        return self._directives_implementations

    @property
    def introspection_directives(self):
        return self._introspection_directives

    def bake(self, schema: "GraphQLSchema") -> None:
        self._schema = schema
        directives_definition = get_directive_instances(
            self._directives, self._schema
        )
        self._directives_implementations = {
            CoercerWay.OUTPUT: wraps_with_directives(
                directives_definition=directives_definition,
                directive_hook="on_pre_output_coercion",
            ),
            CoercerWay.INPUT: wraps_with_directives(
                directives_definition=directives_definition,
                directive_hook="on_post_input_coercion",
            ),
        }

        self._introspection_directives = wraps_with_directives(
            directives_definition=directives_definition,
            directive_hook="on_introspection",
        )


class GraphQLEnumType(GraphQLType):
    """
    Enum Type Definition

    Some leaf values of requests and input values are Enums.
    GraphQL serializes Enum values as strings, however internally
    Enums can be represented by any kind of type, often integers.

    Note: If a value is not provided in a definition,
    the name of the enum value will be used as its internal value.
    """

    def __init__(
        self,
        name: str,
        values: List[GraphQLEnumValue],
        description: Optional[str] = None,
        schema: Optional["GraphQLSchema"] = None,
        directives: Optional[List[str]] = None,
    ) -> None:
        super().__init__(
            name=name,
            description=description,
            is_enum_value=True,
            schema=schema,
        )
        self.values = values
        self._directives = directives
        self._directives_executors = {
            CoercerWay.OUTPUT: self._output_directives_executor,
            CoercerWay.INPUT: self._input_directives_executor,
        }
        self._directives_implementations = {}
        self._value_map = {}

    def __repr__(self) -> str:
        return "{}(name={!r}, values={!r}, description={!r})".format(
            self.__class__.__name__, self.name, self.values, self.description
        )

    def __eq__(self, other: Any) -> bool:
        return super().__eq__(other) and self.values == other.values

    # Introspection Attribute
    @property
    def kind(self) -> str:
        return "ENUM"

    # Introspection Attribute
    @property
    def enumValues(  # pylint: disable=invalid-name
        self
    ) -> List[GraphQLEnumValue]:
        return self.values

    def bake(self, schema: "GraphQLSchema") -> None:
        super().bake(schema)
        directives_definition = get_directive_instances(
            self._directives, self._schema
        )
        self._directives_implementations = {
            CoercerWay.OUTPUT: wraps_with_directives(
                directives_definition=directives_definition,
                directive_hook="on_pre_output_coercion",
            ),
            CoercerWay.INPUT: wraps_with_directives(
                directives_definition=directives_definition,
                directive_hook="on_post_input_coercion",
            ),
        }

        self._introspection_directives = wraps_with_directives(
            directives_definition=directives_definition,
            directive_hook="on_introspection",
        )

        for value in self.values:
            value.bake(schema)
            self._value_map[value.name] = value

    async def _output_directives_executor(self, val, *args, **kwargs):
        if isinstance(val, list):
            return [
                await self._output_directives_executor(x, *args, **kwargs)
                for x in val
            ]

        # Cause this is called PRE coercion, call directives if val is in value_map
        if val in self._value_map:
            # Call value directives
            val = await self._value_map[val].directives[CoercerWay.OUTPUT](
                val, *args, **kwargs
            )

        # Call Type directives
        return await self._directives_implementations[CoercerWay.OUTPUT](
            val, *args, **kwargs
        )

    async def _input_directives_executor(self, val, *args, **kwargs):
        # Call Type Directives
        rval = await self._directives_implementations[CoercerWay.INPUT](
            val, *args, **kwargs
        )

        # Manage the fact that, val can be inputed as None.
        if not val:
            return rval

        # Call Value Directives
        # This is done POST coercion, so VAL exists in map
        return await self._value_map[val].directives[CoercerWay.INPUT](
            rval, *args, **kwargs
        )

    @property
    def directives(self):
        return self._directives_executors
