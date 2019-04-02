from typing import Any, List, Optional

from tartiflette.language.ast.base import TypeExtensionNode


class ObjectTypeExtensionNode(TypeExtensionNode):
    """
    AST node representing a GraphQL object type extension.
    """

    __slots__ = ("name", "interfaces", "directives", "fields", "location")

    def __init__(
        self,
        name: "NameNode",
        interfaces: Optional[List["NamedTypeNode"]] = None,
        directives: Optional[List["DirectiveNode"]] = None,
        fields: Optional[List["FieldDefinitionNode"]] = None,
        location: Optional["Location"] = None,
    ) -> None:
        """
        :param name: name of the object type extension
        :param interfaces: interfaces of the object type extension
        :param directives: directives of the object type extension
        :param fields: fields of the object type extension
        :param location: location of the object type extension in the query/SDL
        :type name: NameNode
        :type interfaces: Optional[List[NamedTypeNode]]
        :type directives: Optional[List[DirectiveNode]]
        :type fields: Optional[List[FieldDefinitionNode]]
        :type location: Optional[Location]
        """
        self.name = name
        self.interfaces = interfaces
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
            isinstance(other, ObjectTypeExtensionNode)
            and (
                self.name == other.name
                and self.interfaces == other.interfaces
                and self.directives == other.directives
                and self.fields == other.fields
                and self.location == other.location
            )
        )

    def __repr__(self) -> str:
        """
        Returns the representation of an ObjectTypeExtensionNode instance.
        :return: the representation of an ObjectTypeExtensionNode instance
        :rtype: str
        """
        return (
            "ObjectTypeExtensionNode(name=%r, interfaces=%r, directives=%r, "
            "fields=%r, location=%r)"
            % (
                self.name,
                self.interfaces,
                self.directives,
                self.fields,
                self.location,
            )
        )
