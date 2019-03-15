from typing import Any, List, Optional

from tartiflette.language.ast.base import Node


class FieldDefinitionNode(Node):
    """
    TODO:
    """

    __slots__ = (
        "description",
        "name",
        "arguments",
        "type",
        "directives",
        "location",
    )

    def __init__(
        self,
        name: "NameNode",
        type: "TypeNode",
        description: Optional["DescriptionNode"] = None,
        arguments: Optional[List["InputValueDefinitionNode"]] = None,
        directives: Optional[List["DirectiveNode"]] = None,
        location: Optional["Location"] = None,
    ) -> None:
        """
        TODO:
        :param name: TODO:
        :param type: TODO:
        :param description: TODO:
        :param arguments: TODO:
        :param directives: TODO:
        :param location: TODO:
        :type name: NameNode
        :type type: TypeNode
        :type description: Optional[DescriptionNode]
        :type arguments: Optional[List[InputValueDefinitionNode]]
        :type directives: Optional[List[DirectiveNode]]
        :type location: Optional[Location]
        """
        # pylint: disable=redefined-builtin
        self.name = name
        self.type = type
        self.description = description
        self.arguments = arguments
        self.directives = directives
        self.location = location

    def __eq__(self, other: Any) -> bool:
        """
        TODO:
        :param other: TODO:
        :type other: Any
        :return: TODO:
        :rtype: bool
        """
        return self is other or (
            isinstance(other, FieldDefinitionNode)
            and (
                self.description == other.description
                and self.name == other.name
                and self.arguments == other.arguments
                and self.type == other.type
                and self.directives == other.directives
                and self.location == other.location
            )
        )

    def __repr__(self) -> str:
        """
        TODO:
        :return: TODO:
        :rtype: str
        """
        return (
            "FieldDefinitionNode(description=%r, name=%r, arguments=%r, type=%r, directives=%r, location=%r)"
            % (
                self.description,
                self.name,
                self.arguments,
                self.type,
                self.directives,
                self.location,
            )
        )
