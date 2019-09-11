from typing import Any, Dict, List, Optional

__all__ = ("GraphQLDirective",)


class GraphQLDirective:
    """
    Definition of a GraphQL directive.
    """

    def __init__(
        self,
        name: str,
        locations: List[str],
        arguments: Optional[Dict[str, "GraphQLArgument"]] = None,
        description: Optional[str] = None,
    ) -> None:
        """
        :param name: name of the directive
        :param locations: list of allowed locations for the directive
        :param arguments: map of arguments linked to the directive
        :param description: description of the argument
        :type name: str
        :type locations: List[str]
        :type arguments: Optional[Dict[str, GraphQLArgument]]
        :type description: Optional[str]
        """
        self.name = name
        self.locations = locations
        self.arguments = arguments or {}
        self.description = description
        self.implementation = None

        # Introspection attributes
        self.args: List["GraphQLArgument"] = []

    def __eq__(self, other: Any) -> bool:
        """
        Returns True if `other` instance is identical to `self`.
        :param other: object instance to compare to `self`
        :type other: Any
        :return: whether or not `other` is identical to `self`
        :rtype: bool
        """
        return self is other or (
            isinstance(other, GraphQLDirective)
            and self.name == other.name
            and self.locations == other.locations
            and self.arguments == other.arguments
            and self.description == other.description
        )

    def __repr__(self) -> str:
        """
        Returns the representation of a GraphQLDirective instance.
        :return: the representation of a GraphQLDirective instance
        :rtype: str
        """
        return (
            "GraphQLDirective(name={!r}, locations={!r}, arguments={!r}, "
            "description={!r})".format(
                self.name, self.locations, self.arguments, self.description
            )
        )

    def __str__(self) -> str:
        """
        Returns a human-readable representation of the directive.
        :return: a human-readable representation of the directive
        :rtype: str
        """
        return self.name

    def bake(self, schema: "GraphQLSchema") -> None:
        """
        Bakes the GraphQLDirective and computes all the necessary stuff for
        execution.
        :param schema: the GraphQLSchema instance linked to the engine
        :type schema: GraphQLSchema
        """
        for argument in self.arguments.values():
            argument.bake(schema)
            self.args.append(argument)
