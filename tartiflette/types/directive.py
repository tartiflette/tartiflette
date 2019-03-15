from typing import Any, Callable, Dict, List, Optional


class GraphQLDirective:
    """
    Directive Definition

    A directive definition defines where a directive can be used and
    its arguments
    """

    SCHEMA = "SCHEMA"
    SCALAR = "SCALAR"
    OBJECT = "OBJECT"
    FIELD_DEFINITION = "FIELD_DEFINITION"
    ARGUMENT_DEFINITION = "ARGUMENT_DEFINITION"
    INTERFACE = "INTERFACE"
    UNION = "UNION"
    ENUM = "ENUM"
    ENUM_VALUE = "ENUM_VALUE"
    INPUT_OBJECT = "INPUT_OBJECT"
    INPUT_FIELD_DEFINITION = "INPUT_FIELD_DEFINITION"
    FIELD = "FIELD"
    FRAGMENT_SPREAD = "FRAGMENT_SPREAD"
    INLINE_FRAGMENT = "INLINE_FRAGMENT"

    POSSIBLE_LOCATIONS = [
        SCHEMA,
        SCALAR,
        OBJECT,
        FIELD_DEFINITION,
        ARGUMENT_DEFINITION,
        INTERFACE,
        UNION,
        ENUM,
        ENUM_VALUE,
        INPUT_OBJECT,
        INPUT_FIELD_DEFINITION,
        FIELD,
        FRAGMENT_SPREAD,
        INLINE_FRAGMENT,
    ]

    def __init__(
        self,
        name: str,
        on: List[str],
        arguments: Optional[Dict[str, "GraphQLArgument"]] = None,
        description: Optional[str] = None,
        implementation: Optional[Callable] = None,
        schema=None,
    ) -> None:
        self.name = name
        self.where = on
        self.arguments = arguments or {}
        self.description = description
        self.implementation = implementation or None
        self.schema = schema

    def __repr__(self) -> str:
        return "{}(name={!r}, on={!r}, arguments={!r}, description={!r})".format(
            self.__class__.__name__,
            self.name,
            self.where,
            self.arguments,
            self.description,
        )

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other: Any) -> bool:
        return self is other or (
            type(self) is type(other)
            and self.name == other.name
            and self.where == other.where
            and self.arguments == other.arguments
        )

    # Introspection property
    @property
    def args(self) -> List["GraphQLArgument"]:
        return list(self.arguments.values())

    # Introspection Attribute
    @property
    def locations(self) -> List[str]:
        return self.where

    def bake(self, schema: "GraphQLSchema") -> None:
        for arg in self.arguments.values():
            arg.bake(schema)
