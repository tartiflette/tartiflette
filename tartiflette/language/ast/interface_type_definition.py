from typing import Any, List, Optional

from tartiflette.language.ast.base import TypeDefinitionNode


class InterfaceTypeDefinitionNode(TypeDefinitionNode):
    """
    AST node representing a GraphQL interface type definition.
    """

    __slots__ = ("description", "name", "directives", "fields", "location")

    def __init__(
        self,
        name: "NameNode",
        description: Optional["DescriptionNode"] = None,
        directives: Optional[List["DirectiveNode"]] = None,
        fields: Optional[List["FieldDefinitionNode"]] = None,
        location: Optional["Location"] = None,
    ) -> None:
        """
        :param name: name of the interface type definition
        :param description: description of the interface type definition
        :param directives: directives of the interface type definition
        :param fields: fields of the interface type definition
        :param location: location of the interface type definition in the
        query/SDL
        :type name: NameNode
        :type description: Optional[DescriptionNode]
        :type directives: Optional[List[DirectiveNode]]
        :type fields: Optional[List[FieldDefinitionNode]]
        :type location: Optional[Location]
        """
        self.name = name
        self.description = description
        self.directives = directives
        self.fields = fields
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
            isinstance(other, InterfaceTypeDefinitionNode)
            and (
                self.description == other.description
                and self.name == other.name
                and self.directives == other.directives
                and self.fields == other.fields
                and self.location == other.location
            )
        )

    def __repr__(self) -> str:
        """
        Returns the representation of an InterfaceTypeDefinitionNode instance.
        :return: the representation of an InterfaceTypeDefinitionNode instance
        :rtype: str
        """
        return (
            "InterfaceTypeDefinitionNode(description=%r, name=%r, "
            "directives=%r, fields=%r, location=%r)"
            % (
                self.description,
                self.name,
                self.directives,
                self.fields,
                self.location,
            )
        )
