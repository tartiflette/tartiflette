from typing import Optional, Dict, List, Callable


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
    ]

    def __init__(
        self,
        name: str,
        on: List[str],
        arguments: Optional[Dict] = None,
        description: Optional[str] = None,
        implementation: Optional[Callable] = None,
    ):
        self.name = name
        self.where = on
        self.arguments = arguments if arguments else {}
        self.description = description
        self.implementation = implementation or None

    def __repr__(self):
        return "{}(name={!r}, on={!r}, arguments={!r}, description={!r})".format(
            self.__class__.__name__,
            self.name,
            self.where,
            self.arguments,
            self.description,
        )

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self is other or (
            type(self) is type(other)
            and self.name == other.name
            and self.where == other.where
            and self.arguments == other.arguments
        )

    # Introspection property
    @property
    def args(self):
        return [x for _, x in self.arguments.items()]

    # Introspection Attribute
    @property
    def locations(self):
        return self.where
