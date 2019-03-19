from typing import Any, List, Optional

from tartiflette.language.ast.base import TypeDefinitionNode


class EnumTypeDefinitionNode(TypeDefinitionNode):
    """
    AST node representing a GraphQL enum type definition.
    """

    __slots__ = ("description", "name", "directives", "values", "location")

    def __init__(
        self,
        name: "NameNode",
        description: Optional["DescriptionNode"] = None,
        directives: Optional[List["DirectiveNode"]] = None,
        values: Optional[List["EnumValueDefinitionNode"]] = None,
        location: Optional["Location"] = None,
    ) -> None:
        """
        :param name: name of the enum type definition
        :param description: description of the enum type definition
        :param directives: directives of the enum type definition
        :param values: possible values of the enum type definition
        :param location: location of the enum type definition in the query/SDL
        :type name: NameNode
        :type description: Optional[DescriptionNode]
        :type directives: Optional[List[DirectiveNode]]
        :type values: Optional[List[EnumValueDefinitionNode]]
        :type location: Optional[Location]
        """
        self.name = name
        self.description = description
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
            isinstance(other, EnumTypeDefinitionNode)
            and (
                self.description == other.description
                and self.name == other.name
                and self.directives == other.directives
                and self.values == other.values
                and self.location == other.location
            )
        )

    def __repr__(self) -> str:
        """
        Returns the representation of an EnumTypeDefinitionNode instance.
        :return: the representation of an EnumTypeDefinitionNode instance
        :rtype: str
        """
        return (
            "EnumTypeDefinitionNode(description=%r, name=%r, directives=%r, "
            "values=%r, location=%r)"
            % (
                self.description,
                self.name,
                self.directives,
                self.values,
                self.location,
            )
        )
