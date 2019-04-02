from typing import Any, List, Optional

from tartiflette.language.ast.base import SelectionNode


class InlineFragmentNode(SelectionNode):
    """
    AST node representing a GraphQL inline fragment.
    """

    __slots__ = ("type_condition", "directives", "selection_set", "location")

    def __init__(
        self,
        selection_set: "SelectionSetNode",
        type_condition: Optional["NamedTypeNode"] = None,
        directives: Optional[List["DirectiveNode"]] = None,
        location: Optional["Location"] = None,
    ) -> None:
        """
        :param selection_set: selection set of the inline fragment
        :param type_condition: type condition of the inline fragment
        :param directives: directives of the inline fragment
        :param location: location of the inline fragment in the query/SDL
        :type selection_set: SelectionSetNode
        :type type_condition: Optional[NamedTypeNode]
        :type directives: Optional[List[DirectiveNode]]
        :type location: Optional[Location]
        """
        self.selection_set = selection_set
        self.type_condition = type_condition
        self.directives = directives
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
            isinstance(other, InlineFragmentNode)
            and (
                self.type_condition == other.type_condition
                and self.directives == other.directives
                and self.selection_set == other.selection_set
                and self.location == other.location
            )
        )

    def __repr__(self) -> str:
        """
        Returns the representation of an InlineFragmentNode instance.
        :return: the representation of an InlineFragmentNode instance
        :rtype: str
        """
        return (
            "InlineFragmentNode(type_condition=%r, directives=%r, "
            "selection_set=%r, location=%r)"
            % (
                self.type_condition,
                self.directives,
                self.selection_set,
                self.location,
            )
        )
