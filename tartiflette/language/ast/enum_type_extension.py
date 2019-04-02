from typing import Any, List, Optional

from tartiflette.language.ast.base import TypeExtensionNode


class EnumTypeExtensionNode(TypeExtensionNode):
    """
    AST node representing a GraphQL enum type extension.
    """

    __slots__ = ("name", "directives", "values", "location")

    def __init__(
        self,
        name: "NameNode",
        directives: Optional[List["DirectiveNode"]] = None,
        values: Optional[List["EnumValueDefinitionNode"]] = None,
        location: Optional["Location"] = None,
    ) -> None:
        """
        :param name: name of the enum type extension node
        :param directives: directives of the enum type extension node
        :param values: possible values of the enum type extension node
        :param location: location of the enum type extension in the query/SDL
        :type name: NameNode
        :type directives: Optional[List[DirectiveNode]]
        :type values: Optional[List[EnumValueDefinitionNode]]
        :type location: Optional[Location]
        """
        self.name = name
        self.directives = directives
        self.values = values
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
            isinstance(other, EnumTypeExtensionNode)
            and (
                self.name == other.name
                and self.directives == other.directives
                and self.values == other.values
                and self.location == other.location
            )
        )

    def __repr__(self) -> str:
        """
        Returns the representation of an EnumTypeExtensionNode instance.
        :return: the representation of an EnumTypeExtensionNode instance
        :rtype: str
        """
        return (
            "EnumTypeExtensionNode(name=%r, directives=%r, values=%r, "
            "location=%r)"
            % (self.name, self.directives, self.values, self.location)
        )
