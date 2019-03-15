from typing import List, Optional

from tartiflette.language.ast.base import SelectionNode


class InlineFragmentNode(SelectionNode):
    """
    TODO:
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
        TODO:
        :param selection_set: TODO:
        :param type_condition: TODO:
        :param directives: TODO:
        :param location: TODO:
        :type selection_set: TODO:
        :type type_condition: TODO:
        :type directives: TODO:
        :type location: TODO:
        """
        self.selection_set = selection_set
        self.type_condition = type_condition
        self.directives = directives
        self.location = location

    def __eq__(self, other):
        """
        TODO:
        :param other: TODO:
        :type other: TODO:
        :return: TODO:
        :rtype: TODO:
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
        TODO:
        :return: TODO:
        :rtype: TODO:
        """
        return (
            "InlineFragmentNode(type_condition=%r, directives=%r, selection_set=%r, location=%r)"
            % (
                self.type_condition,
                self.directives,
                self.selection_set,
                self.location,
            )
        )
