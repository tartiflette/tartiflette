from typing import Any, List, Optional

from tartiflette.language.ast.base import Node


class InputValueDefinitionNode(Node):
    """
    TODO:
    """

    __slots__ = (
        "description",
        "name",
        "type",
        "default_value",
        "directives",
        "location",
    )

    def __init__(
        self,
        name: "NameNode",
        type: "TypeNode",
        description: Optional["DescriptionNode"] = None,
        default_value: Optional["ValueNode"] = None,
        directives: Optional[List["DirectiveNode"]] = None,
        location: Optional["Location"] = None,
    ) -> None:
        """
        TODO:
        :param name: TODO:
        :param type: TODO:
        :param description: TODO:
        :param default_value: TODO:
        :param directives: TODO:
        :param location: TODO:
        :type name: NameNode
        :type type: TypeNode
        :type description: Optional[DescriptionNode]
        :type default_value: Optional[ValueNode]
        :type directives: Optional[List[DirectiveNode]]
        :type location: Optional[Location]
        """
        # pylint: disable=redefined-builtin
        self.name = name
        self.type = type
        self.description = description
        self.default_value = default_value
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
            isinstance(other, InputValueDefinitionNode)
            and (
                self.description == other.description
                and self.name == other.name
                and self.type == other.type
                and self.default_value == other.default_value
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
            "InputValueDefinitionNode(description=%r, name=%r, type=%r, default_value=%r, directives=%r, location=%r)"
            % (
                self.description,
                self.name,
                self.type,
                self.default_value,
                self.directives,
                self.location,
            )
        )
