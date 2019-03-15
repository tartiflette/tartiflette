from typing import List, Optional

from tartiflette.language.ast.base import DefinitionNode


class FragmentDefinitionNode(DefinitionNode):
    """
    TODO:
    """

    __slots__ = (
        "name",
        "type_condition",
        "directives",
        "selection_set",
        "location",
    )

    def __init__(
        self,
        name: "NameNode",
        type_condition: "NamedTypeNode",
        selection_set: "SelectionSetNode",
        directives: Optional[List["DirectiveNode"]] = None,
        location: Optional["Location"] = None,
    ) -> None:
        """
        TODO:
        :param name: TODO:
        :param type_condition: TODO:
        :param selection_set: TODO:
        :param directives: TODO:
        :param location: TODO:
        :type name: TODO:
        :type type_condition: TODO:
        :type selection_set: TODO:
        :type directives: TODO:
        :type location: TODO:
        """
        self.name = name
        self.type_condition = type_condition
        self.selection_set = selection_set
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
            isinstance(other, FragmentDefinitionNode)
            and (
                self.name == other.name
                and self.type_condition == other.type_condition
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
            "FragmentDefinitionNode(name=%r, type_condition=%r, directives=%r, selection_set=%r, location=%r)"
            % (
                self.name,
                self.type_condition,
                self.directives,
                self.selection_set,
                self.location,
            )
        )
