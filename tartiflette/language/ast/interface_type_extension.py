from typing import Any, List, Optional

from tartiflette.language.ast.base import TypeExtensionNode


class InterfaceTypeExtensionNode(TypeExtensionNode):
    """
    AST node representing a GraphQL interface type extension.
    """

    __slots__ = ("name", "directives", "fields", "location")

    def __init__(
        self,
        name: "NameNode",
        directives: Optional[List["DirectiveNode"]] = None,
        fields: Optional[List["FieldDefinitionNode"]] = None,
        location: Optional["Location"] = None,
    ) -> None:
        """
        :param name: name of the interface type extension
        :param directives: directives of the interface type extension
        :param fields: fields of the interface type extension
        :param location: location of the interface type extension in the
        query/SDL
        :type name: NameNode
        :type directives: Optional[List[DirectiveNode]]
        :type fields: Optional[List[FieldDefinitionNode]]
        :type location: Optional[Location]
        """
        self.name = name
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
            isinstance(other, InterfaceTypeExtensionNode)
            and (
                self.name == other.name
                and self.directives == other.directives
                and self.fields == other.fields
                and self.location == other.location
            )
        )

    def __repr__(self) -> str:
        """
        Returns the representation of an InterfaceTypeExtensionNode instance.
        :return: the representation of an InterfaceTypeExtensionNode instance
        :rtype: str
        """
        return (
            "InterfaceTypeExtensionNode(name=%r, directives=%r, fields=%r, "
            "location=%r)"
            % (self.name, self.directives, self.fields, self.location)
        )
