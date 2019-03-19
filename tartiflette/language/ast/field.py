from typing import Any, List, Optional

from tartiflette.language.ast.base import SelectionNode


class FieldNode(SelectionNode):
    """
    AST node representing a GraphQL field.
    """

    __slots__ = (
        "alias",
        "name",
        "arguments",
        "directives",
        "selection_set",
        "location",
    )

    def __init__(
        self,
        name: "NameNode",
        alias: Optional["NameNode"] = None,
        arguments: Optional[List["ArgumentNode"]] = None,
        directives: Optional[List["DirectiveNode"]] = None,
        selection_set: Optional["SelectionSetNode"] = None,
        location: Optional["Location"] = None,
    ) -> None:
        """
        :param name: name of the field
        :param alias: alias of the field
        :param arguments: arguments of the field
        :param directives: directives of the field
        :param selection_set: selection set of the field
        :param location: location of the field in the query/SDL
        :type name: NameNode
        :type alias: Optional[NameNode]
        :type arguments: Optional[List[ArgumentNode]]
        :type directives: Optional[List[DirectiveNode]]
        :type selection_set: Optional[SelectionSetNode]
        :type location: Optional[Location]
        """
        self.name = name
        self.alias = alias
        self.arguments = arguments
        self.directives = directives
        self.selection_set = selection_set
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
            isinstance(other, FieldNode)
            and (
                self.alias == other.alias
                and self.name == other.name
                and self.arguments == other.arguments
                and self.directives == other.directives
                and self.selection_set == other.selection_set
                and self.location == other.location
            )
        )

    def __repr__(self) -> str:
        """
        Returns the representation of a FieldNode instance.
        :return: the representation of a FieldNode instance
        :rtype: str
        """
        return (
            "FieldNode(alias=%r, name=%r, arguments=%r, directives=%r, "
            "selection_set=%r, location=%r)"
            % (
                self.alias,
                self.name,
                self.arguments,
                self.directives,
                self.selection_set,
                self.location,
            )
        )
