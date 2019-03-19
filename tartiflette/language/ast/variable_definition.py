from typing import Any, Optional

from tartiflette.language.ast.base import Node


class VariableDefinitionNode(Node):
    """
    AST node representing a GraphQL variable definition.
    """

    __slots__ = ("variable", "type", "default_value", "location")

    def __init__(
        self,
        variable: "VariableNode",
        type: "TypeNode",
        default_value: Optional["ValueNode"] = None,
        location: Optional["Location"] = None,
    ) -> None:
        """
        :param variable: variable of the variable definition
        :param type: type of the variable definition
        :param default_value: default value of the variable definition
        :param location: location of the variable definition in the query/SDL
        :type variable: VariableNode
        :type type: TypeNode
        :type default_value: Optional[ValueNode]
        :type location: Optional[Location]
        """
        # pylint: disable=redefined-builtin
        self.variable = variable
        self.type = type
        self.default_value = default_value
        self.location = location

    def __eq__(self, other: Any) -> bool:
        """
        Returns True if `other` instance is identical to `self`.
        :param other: object instance to compare to `self`
        :type other: Any
        :return: whether or not `other` is identical to `self`
        :rtype: bool
        """
        return self is other or (
            isinstance(other, VariableDefinitionNode)
            and (
                self.variable == other.variable
                and self.type == other.type
                and self.default_value == other.default_value
                and self.location == other.location
            )
        )

    def __repr__(self) -> str:
        """
        Returns the representation of a VariableDefinitionNode instance.
        :return: the representation of a VariableDefinitionNode instance
        :rtype: str
        """
        return (
            "VariableDefinitionNode(variable=%r, type=%r, default_value=%r, "
            "location=%r)"
            % (self.variable, self.type, self.default_value, self.location)
        )
