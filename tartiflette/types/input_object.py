from functools import partial
from typing import Any, Callable, Dict, List, Optional

from tartiflette.coercers.inputs.directives_coercer import (
    input_directives_coercer,
)
from tartiflette.coercers.inputs.input_object_coercer import (
    input_object_coercer as input_input_object_coercer,
)
from tartiflette.coercers.literals.directives_coercer import (
    literal_directives_coercer,
)
from tartiflette.coercers.literals.input_object_coercer import (
    input_object_coercer as literal_input_object_coercer,
)
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

__all__ = ("GraphQLInputObjectType",)


class GraphQLInputObjectType(GraphQLInputType, GraphQLType):
    """
    Definition of a GraphQL input object.
    """

    # Introspection attributes
    kind = "INPUT_OBJECT"

    def __init__(
        self,
        name: str,
        fields: Dict[str, "GraphQLInputField"],
        definition: "InputObjectTypeDefinitionNode",
        description: Optional[str] = None,
        directives: Optional[List["DirectiveNode"]] = None,
    ) -> None:
        """
        :param name: name of the input object
        :param fields: map of fields linked to the input object
        :param definition: the input object definition AST node
        :param description: description of the input object
        :param directives: list of directives linked to the input object
        :type name: str
        :type fields: Dict[str, GraphQLInputField]
        :type definition: InputObjectTypeDefinitionNode
        :type description: Optional[str]
        :type directives: Optional[List[DirectiveNode]]
        """
        self.name = name
        self.input_fields = fields or {}
        self.definition = definition
        self.description = description

        # Directives
        self.directives = directives
        self.introspection_directives: Optional[Callable] = None

        # Coercers
        self.input_coercer: Optional[Callable] = None
        self.literal_coercer: Optional[Callable] = None

        # Introspection attributes
        self.inputFields: List[  # pylint: disable=invalid-name
            "GraphQLInputField"
        ] = []

    def __eq__(self, other: Any) -> bool:
        """
        Returns True if `other` instance is identical to `self`.
        :param other: object instance to compare to `self`
        :type other: Any
        :return: whether or not `other` is identical to `self`
        :rtype: bool
        """
        return self is other or (
            isinstance(other, GraphQLInputObjectType)
            and self.name == other.name
            and self.input_fields == other.input_fields
            and self.description == other.description
            and self.directives == other.directives
        )

    def __repr__(self) -> str:
        """
        Returns the representation of a GraphQLInputObjectType instance.
        :return: the representation of a GraphQLInputObjectType instance
        :rtype: str
        """
        return (
            "GraphQLInputObjectType(name={!r}, fields={!r}, description={!r}, "
            "directives={!r})".format(
                self.name, self.input_fields, self.description, self.directives
            )
        )

    def __str__(self) -> str:
        """
        Returns a human-readable representation of the input object.
        :return: a human-readable representation of the input object
        :rtype: str
        """
        return self.name

    def has_field(self, name: str) -> bool:
        """
        Determines whether or not the name corresponds to a defined field.
        :param name: name of the field to find
        :type name: str
        :return: whether or not the name corresponds to a defined field
        :rtype: bool
        """
        return name in self.input_fields

    def bake(self, schema: "GraphQLSchema") -> None:
        """
        Bakes the GraphQLInputObject and computes all the necessary stuff for execution.
        :param schema: the GraphQLSchema schema instance linked to the SDL
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
                "on_post_input_object_coercion",
                "on_post_input_coercion",
            ],
            func=default_post_input_coercion_directive,
        )

        # Coercers
        self.input_coercer = partial(
            input_directives_coercer,
            coercer=partial(
                input_input_object_coercer, input_object_type=self
            ),
            directives=post_input_coercion_directives,
            definition_node=self.definition,
        )
        self.literal_coercer = partial(
            literal_directives_coercer,
            coercer=partial(
                literal_input_object_coercer, input_object_type=self
            ),
            directives=post_input_coercion_directives,
            definition_node=self.definition,
        )

    async def bake_input_fields(self, schema: "GraphQLSchema") -> None:
        """
        Bakes input object's input fields.
        :param schema: the GraphQLSchema instance linked to the SDL
        :type schema: GraphQLSchema
        """
        if self.input_fields:
            for input_field in self.input_fields.values():
                input_field.bake(schema)
                self.inputFields.append(input_field)


class GraphQLInputObjectTypeExtension(GraphQLType, GraphQLExtension):
    def __init__(self, name, input_fields, directives):
        self.name = name
        self.input_fields = input_fields or {}
        self.directives = directives

    def bake(self, schema):
        extended = schema.find_type(self.name)
        extended.input_fields.update(self.input_fields)
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
            isinstance(other, GraphQLInputObjectTypeExtension)
            and other.directives == self.directives
            and other.input_fields == self.input_fields
            and other.name == self.name
        )

    def __repr__(self) -> str:
        """
        Returns the representation of a GraphQLType instance.
        :return: the representation of a GraphQLType instance
        :rtype: str
        """
        return (
            f"GraphQLInputObjectTypeExtension(name={repr(self.name)}, "
            f"directives={repr(self.directives)}, "
            f"input_fields={repr(self.input_fields)})"
        )
