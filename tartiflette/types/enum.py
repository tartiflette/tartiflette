from functools import partial
from typing import Any, Callable, Dict, List, Optional

from tartiflette.coercers.inputs.directives_coercer import (
    input_directives_coercer,
)
from tartiflette.coercers.inputs.enum_coercer import (
    enum_coercer as input_enum_coercer,
)
from tartiflette.coercers.literals.directives_coercer import (
    literal_directives_coercer,
)
from tartiflette.coercers.literals.enum_coercer import (
    enum_coercer as literal_enum_coercer,
)
from tartiflette.coercers.outputs.directives_coercer import (
    output_directives_coercer,
)
from tartiflette.coercers.outputs.enum_coercer import enum_coercer
from tartiflette.types.helpers.get_directive_instances import (
    compute_directive_nodes,
)
from tartiflette.types.type import (
    GraphQLExtension,
    GraphQLInputType,
    GraphQLType,
)
from tartiflette.utils.directives import (
    default_post_input_coercion_directive,
    wraps_with_directives,
)

__all__ = ("GraphQLEnumValue", "GraphQLEnumType")


class GraphQLEnumValue:
    """
    Definition of a GraphQL enum value.
    """

    def __init__(
        self,
        value: str,
        definition: "EnumValueDefinitionNode",
        description: Optional[str] = None,
        directives: Optional[List["DirectiveNode"]] = None,
    ) -> None:
        """
        :param value: value of the enum value
        :param definition: the enum value definition AST node
        :param description: description of the enum value
        :param directives: list of directives linked to the enum value
        :type value: str
        :type definition: EnumValueDefinitionNode
        :type description: Optional[str]
        :type directives: Optional[List[DirectiveNode]]
        """
        self.value = value
        self.definition = definition
        self.description = description

        # Directives
        self.directives = directives
        self.on_post_bake: Optional[Callable] = None
        self.introspection_directives: Optional[Callable] = None

        # Coercers
        self.input_coercer: Optional[Callable] = None
        self.literal_coercer: Optional[Callable] = None
        self.output_coercer: Optional[Callable] = None

        # Introspection attributes
        self.isDeprecated: bool = False  # pylint: disable=invalid-name

    def __eq__(self, other: Any) -> bool:
        """
        Returns True if `other` instance is identical to `self`.
        :param other: object instance to compare to `self`
        :type other: Any
        :return: whether or not `other` is identical to `self`
        :rtype: bool
        """
        return self is other or (
            isinstance(other, GraphQLEnumValue)
            and self.value == other.value
            and self.description == other.description
            and self.directives == other.directives
        )

    def __repr__(self) -> str:
        """
        Returns the representation of a GraphQLEnumValue instance.
        :return: the representation of a GraphQLEnumValue instance
        :rtype: str
        """
        return (
            "GraphQLEnumValue(value={!r}, description={!r}, "
            "directives={!r})".format(
                self.value, self.description, self.directives
            )
        )

    def __str__(self) -> str:
        """
        Returns a human-readable representation of the enum value.
        :return: a human-readable representation of the enum value
        :rtype: str
        """
        return str(self.value)

    # Introspection attribute
    @property
    def name(self) -> str:
        """
        Returns the name of the enum value which is used by the introspection
        query.
        :return: the name of the enum value
        :rtype: str
        """
        return self.value

    def bake(self, schema: "GraphQLSchema") -> None:
        """
        Bakes the GraphQLEnumValue and computes all the necessary stuff for
        execution.
        :param schema: the GraphQLSchema instance linked to the SDL
        :type schema: GraphQLSchema
        """
        # Directives
        directives_definition = compute_directive_nodes(
            schema, self.directives
        )
        self.on_post_bake = partial(
            wraps_with_directives(
                directives_definition=directives_definition,
                directive_hooks=["on_post_bake"],
                with_default=True,
            ),
            self,
        )
        self.introspection_directives = wraps_with_directives(
            directives_definition=directives_definition,
            directive_hooks=["on_introspection"],
        )
        post_input_coercion_directives = wraps_with_directives(
            directives_definition=directives_definition,
            directive_hooks=[
                "on_post_enum_value_input_coercion",
                "on_post_input_coercion",
            ],
            func=default_post_input_coercion_directive,
        )

        # Coercers
        self.input_coercer = post_input_coercion_directives
        self.literal_coercer = post_input_coercion_directives
        self.output_coercer = wraps_with_directives(
            directives_definition=directives_definition,
            directive_hooks=["on_pre_output_coercion"],
            with_default=True,
        )


class GraphQLEnumType(GraphQLInputType, GraphQLType):
    """
    Definition of a GraphQL enum type.
    """

    # Introspection attributes
    kind = "ENUM"

    def __init__(
        self,
        name: str,
        values: List["GraphQLEnumValue"],
        definition: "EnumTypeDefinitionNode",
        description: Optional[str] = None,
        directives: Optional[List["DirectiveNode"]] = None,
    ) -> None:
        """
        :param name: name of the enum
        :param values: list of values linked to the enum
        :param definition: the enum type definition AST node
        :param description: description of the enum
        :param directives: list of directives linked to the enum
        :type name: str
        :type values: List[GraphQLEnumValue]
        :type definition: EnumTypeDefinitionNode
        :type description: Optional[str]
        :type directives: Optional[List[DirectiveNode]]
        """
        self.name = name
        self.values = values
        self.definition = definition
        self.description = description
        self._value_map: Dict[str, "GraphQLEnumValue"] = {}

        # Directives
        self.directives = directives
        self.introspection_directives: Optional[Callable] = None

        # Coercers
        self.input_coercer: Optional[Callable] = None
        self.literal_coercer: Optional[Callable] = None
        self.output_coercer: Optional[Callable] = None

    def __eq__(self, other: Any) -> bool:
        """
        Returns True if `other` instance is identical to `self`.
        :param other: object instance to compare to `self`
        :type other: Any
        :return: whether or not `other` is identical to `self`
        :rtype: bool
        """
        return self is other or (
            isinstance(other, GraphQLEnumType)
            and self.name == other.name
            and self.values == other.values
            and self.description == other.description
            and self.directives == other.directives
        )

    def __repr__(self) -> str:
        """
        Returns the representation of a GraphQLEnumType instance.
        :return: the representation of a GraphQLEnumType instance
        :rtype: str
        """
        return (
            "GraphQLEnumType(name={!r}, values={!r}, description={!r}, "
            "directives={!r})".format(
                self.name, self.values, self.description, self.directives
            )
        )

    def __str__(self) -> str:
        """
        Returns a human-readable representation of the enum type.
        :return: a human-readable representation of the enum type
        :rtype: str
        """
        return self.name

    # Introspection attribute
    @property
    def enumValues(  # pylint: disable=invalid-name
        self,
    ) -> List["GraphQLEnumValue"]:
        """
        Returns the list of enum values of the enum which is used by the
        introspection query.
        :return: the list of enum values of the enum
        :rtype: List[GraphQLEnumValue]
        """
        return self.values

    def has_value(self, name: str) -> bool:
        """
        Determines whether or not the name corresponds to an enum value.
        :param name: name of the enum value to find
        :type name: str
        :return: whether or not the name corresponds to a defined enum value
        :rtype: bool
        """
        return name in self._value_map

    def get_value(self, name: str) -> "GraphQLEnumValue":
        """
        Returns the GraphQLEnumValue instance of the enum value `name`.
        :param name: the name of the enum value to fetch
        :type name: str
        :return: the GraphQLEnumValue instance of the enum value `name`
        :rtype: GraphQLEnumValue
        """
        return self._value_map[name]

    def bake(self, schema: "GraphQLSchema") -> None:
        """
        Bakes the GraphQLEnumType and computes all the necessary stuff for
        execution.
        :param schema: the GraphQLSchema instance linked to the SDL
        :type schema: GraphQLSchema
        """
        # Directives
        directives_definition = compute_directive_nodes(
            schema, self.directives
        )
        self.introspection_directives = wraps_with_directives(
            directives_definition=directives_definition,
            directive_hooks=["on_introspection"],
        )
        post_input_coercion_directives = wraps_with_directives(
            directives_definition=directives_definition,
            directive_hooks=[
                "on_post_enum_type_input_coercion",
                "on_post_input_coercion",
            ],
            func=default_post_input_coercion_directive,
        )

        # Coercers
        self.input_coercer = partial(
            input_directives_coercer,
            coercer=partial(input_enum_coercer, enum_type=self),
            directives=post_input_coercion_directives,
            definition_node=self.definition,
        )
        self.literal_coercer = partial(
            literal_directives_coercer,
            coercer=partial(literal_enum_coercer, enum_type=self),
            directives=post_input_coercion_directives,
            definition_node=self.definition,
        )
        self.output_coercer = partial(
            output_directives_coercer,
            coercer=partial(enum_coercer, enum_type=self),
            directives=wraps_with_directives(
                directives_definition=directives_definition,
                directive_hooks=["on_pre_output_coercion"],
                with_default=True,
            ),
        )

    async def bake_enum_values(self, schema: "GraphQLSchema") -> None:
        """
        Bakes enum's values.
        :param schema: the GraphQLSchema instance linked to the SDL
        :type schema: GraphQLSchema
        """
        for enum_value in self.values:
            enum_value.bake(schema)
            enum_value = await enum_value.on_post_bake()
            self._value_map[enum_value.name] = enum_value


class GraphQLEnumTypeExtension(GraphQLType, GraphQLExtension):
    def __init__(self, name, directives, values):
        self.name = name
        self.directives = directives
        self.values = values or []

    def bake(self, schema):
        enum = schema.find_type(self.name)
        enum.directives.extend(self.directives)
        enum.values.extend(self.values)

    def __eq__(self, other: Any) -> bool:
        """
        Returns True if `other` instance is identical to `self`.
        :param other: object instance to compare to `self`
        :type other: Any
        :return: whether or not `other` is identical to `self`
        :rtype: bool
        """
        return self is other or (
            isinstance(other, GraphQLEnumTypeExtension)
            and other.directives == self.directives
            and other.values == self.values
            and other.name == self.name
        )

    def __repr__(self) -> str:
        """
        Returns the representation of a GraphQLType instance.
        :return: the representation of a GraphQLType instance
        :rtype: str
        """
        return f"GraphQLEnumTypeExtension(name={repr(self.name)}, directives={repr(self.directives)}, values={repr(self.values)})"
