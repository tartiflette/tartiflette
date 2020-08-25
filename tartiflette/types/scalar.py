from functools import partial
from typing import Any, Callable, List, Optional

from tartiflette.coercers.inputs.directives_coercer import (
    input_directives_coercer,
)
from tartiflette.coercers.inputs.scalar_coercer import (
    scalar_coercer as input_scalar_coercer,
)
from tartiflette.coercers.literals.directives_coercer import (
    literal_directives_coercer,
)
from tartiflette.coercers.literals.scalar_coercer import (
    scalar_coercer as literal_scalar_coercer,
)
from tartiflette.coercers.outputs.directives_coercer import (
    output_directives_coercer,
)
from tartiflette.coercers.outputs.scalar_coercer import scalar_coercer
from tartiflette.types.helpers.get_directive_instances import (
    compute_directive_nodes,
)
from tartiflette.types.type import (
    GraphQLExtension,
    GraphQLInputType,
    GraphQLType,
)
from tartiflette.utils.directives import wraps_with_directives

__all__ = ("GraphQLScalarType",)


class GraphQLScalarType(GraphQLInputType, GraphQLType):
    """
    Definition of a GraphQL scalar.
    """

    # Introspection attributes
    kind = "SCALAR"

    def __init__(
        self,
        name: str,
        description: Optional[str] = None,
        directives: Optional[List["DirectiveNode"]] = None,
    ) -> None:
        """
        :param name: name of the scalar
        :param description: description of the scalar
        :param directives: list of directives linked to the scalar
        :type name: str
        :type description: Optional[str]
        :type directives: Optional[List[DirectiveNode]]
        """
        self.name = name
        self.description = description

        # Directives
        self.directives = directives
        self.introspection_directives: Optional[Callable] = None

        # Coercers
        self.coerce_output: Optional[Callable] = None
        self.coerce_input: Optional[Callable] = None
        self.parse_literal: Optional[Callable] = None
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
            isinstance(other, GraphQLScalarType)
            and self.name == other.name
            and self.description == other.description
            and self.directives == other.directives
            and self.coerce_output == other.coerce_output
            and self.coerce_input == other.coerce_input
            and self.parse_literal == other.parse_literal
        )

    def __repr__(self) -> str:
        """
        Returns the representation of a GraphQLScalarType instance.
        :return: the representation of a GraphQLScalarType instance
        :rtype: str
        """
        return "GraphQLScalarType(name={!r}, description={!r})".format(
            self.name, self.description
        )

    def __str__(self) -> str:
        """
        Returns a human-readable representation of the scalar.
        :return: a human-readable representation of the scalar
        :rtype: str
        """
        return self.name

    def bake(self, schema: "GraphQLSchema") -> None:
        """
        Bakes the GraphQLScalarType and computes all the necessary stuff for
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
            directive_hook="on_introspection",
        )
        post_input_coercion_directives = wraps_with_directives(
            directives_definition=directives_definition,
            directive_hook="on_post_input_coercion",
        )

        # Coercers
        self.input_coercer = partial(
            input_directives_coercer,
            coercer=partial(input_scalar_coercer, scalar_type=self),
            directives=post_input_coercion_directives,
        )
        self.literal_coercer = partial(
            literal_directives_coercer,
            coercer=partial(literal_scalar_coercer, scalar_type=self),
            directives=post_input_coercion_directives,
        )
        self.output_coercer = partial(
            output_directives_coercer,
            coercer=partial(scalar_coercer, scalar_type=self),
            directives=wraps_with_directives(
                directives_definition=directives_definition,
                directive_hook="on_pre_output_coercion",
                with_default=True,
            ),
        )


class GraphQLScalarTypeExtension(GraphQLType, GraphQLExtension):
    def __init__(self, name, directives):
        self.name = name
        self.directives = directives

    def bake(self, schema):
        extended = schema.find_type(self.name)
        extended.directives.extend(self.directives)

    def __eq__(self, other: Any) -> bool:
        """
        Returns True if `other` instance is identical to `self`.
        :param other: object instance to compare to `self`
        :type other: Any
        :return: whether or not `other` is identical to `self`
        :rtype: bool
        """
        return self is other or (
            isinstance(other, GraphQLScalarTypeExtension)
            and other.directives == self.directives
            and other.name == self.name
        )

    def __repr__(self) -> str:
        """
        Returns the representation of a GraphQLType instance.
        :return: the representation of a GraphQLType instance
        :rtype: str
        """
        return (
            f"GraphQLObjectTypeExtension("
            f"name={repr(self.name)}, "
            f"directives={repr(self.directives)})"
        )
