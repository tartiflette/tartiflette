from typing import Any, Dict, List, Optional, Set, Union

from tartiflette.language.ast import (
    FieldNode,
    FragmentDefinitionNode,
    FragmentSpreadNode,
    InlineFragmentNode,
    OperationDefinitionNode,
)
from tartiflette.language.visitor.constants import SKIP
from tartiflette.language.visitor.type_info import (
    TypeInfo,
    WithTypeInfoVisitor,
)
from tartiflette.language.visitor.visit import visit
from tartiflette.language.visitor.visitor import Visitor

_NODE_WITH_SELECTION_SET = (
    OperationDefinitionNode,
    FragmentDefinitionNode,
    FieldNode,
    InlineFragmentNode,
)

__all__ = ("ASTValidationContext", "QueryValidationContext")


class ASTValidationContext:
    """
    Context for validation rules.
    """

    def __init__(
        self,
        document_node: "DocumentNode",
        schema: Optional["GraphQLSchema"] = None,
    ) -> None:
        """
        :param document_node: AST document node linked to the context
        :param schema: the GraphQLSchema instance linked to the context
        :type document_node: DocumentNode
        :type schema: Optional[GraphQLSchema]
        """
        self.document_node = document_node
        self.schema = schema
        self.errors: List["TartifletteError"] = []

    def report_error(self, error: "TartifletteError") -> None:
        """
        Add an error to the list of errors.
        :param error: the error to append
        :type error: TartifletteError
        """
        self.errors.append(error)


class VariableUsageVisitor(Visitor):
    """
    Visitor which fetch for variable usage.
    """

    def __init__(self, type_info: "TypeInfo") -> None:
        """
        :param type_info: TypeInfo instance to keep track of stacks
        :type type_info: TypeInfo
        """
        self._type_info = type_info
        self.usages = []

    def enter_VariableDefinition(  # pylint: disable=invalid-name
        self,
        node: "VariableDefinitionNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> SKIP:
        """
        Allow to by-pass the VariableDefinitionNode visit and children.
        :param node: the current node being visiting
        :param key: the index/key to this node from the parent node/list
        :param parent: the parent immediately above this node
        :param path: the path to get to this node from the root node
        :param ancestors: nodes and list visited before reaching parent node
        :type node: VariableDefinitionNode
        :type key: Optional[Union[int, str]]
        :type parent: Optional[Union[Node, List[Node]]]
        :type path: List[Union[int, str]]
        :type ancestors: List[Union[Node, List[Node]]]
        :return: the SKIP visitor constant
        :rtype: SKIP
        """
        # pylint: disable=no-self-use,unused-argument
        return SKIP

    def enter_Variable(  # pylint: disable=invalid-name
        self,
        node: "VariableNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> None:
        """
        Collect variable usages.
        :param node: the current node being visiting
        :param key: the index/key to this node from the parent node/list
        :param parent: the parent immediately above this node
        :param path: the path to get to this node from the root node
        :param ancestors: nodes and list visited before reaching parent node
        :type node: VariableNode
        :type key: Optional[Union[int, str]]
        :type parent: Optional[Union[Node, List[Node]]]
        :type path: List[Union[int, str]]
        :type ancestors: List[Union[Node, List[Node]]]
        """
        # pylint: disable=unused-argument
        self.usages.append(
            {
                "node": node,
                "type": self._type_info.get_input_type(),
                "default_value": self._type_info.get_default_value(),
            }
        )


class QueryValidationContext(ASTValidationContext):
    """
    Context for query validation rules.
    """

    def __init__(
        self,
        schema: "GraphQLSchema",
        document_node: "DocumentNode",
        type_info: "TypeInfo",
    ) -> None:
        """
        :param schema: the GraphQLSchema instance linked to the query
        :param document_node: query AST document node to validate
        :param type_info: TypeInfo instance to keep track of stacks
        :type schema: GraphQLSchema
        :type document_node: DocumentNode
        :type type_info: TypeInfo
        """
        super().__init__(document_node, schema=schema)
        self._type_info = type_info
        self._fragments: Optional[Dict[str, "FragmentDefinitionNode"]] = None
        self._fragment_spreads: Dict[
            "SelectionSetNode", List["FragmentSpreadNode"]
        ] = {}
        self._recursively_referenced_fragments: Dict[
            "OperationDefinitionNode", List["FragmentDefinitionNode"]
        ] = {}
        self._variable_usages: Dict[int, List[Dict[str, Any]]] = {}
        self._recursive_variable_usages: Dict[int, List[Dict[str, Any]]] = {}

    def get_fragment(self, name: str) -> Optional["FragmentDefinitionNode"]:
        """
        Fetch the FragmentDefinitionNode by its name.
        :param name: name of the fragment to fetch
        :type name: str
        :return: the FragmentDefinitionNode if found
        :rtype: Optional[FragmentDefinitionNode]
        """
        if self._fragments is None:
            self._fragments = {
                definition.name.value: definition
                for definition in self.document_node.definitions
                if isinstance(definition, FragmentDefinitionNode)
            }
        return self._fragments.get(name)

    def get_fragment_spreads(
        self, selection_set_node: "SelectionSetNode"
    ) -> List["FragmentSpreadNode"]:
        """
        Extract FragmentSpreadNode from a SelectionSetNode.
        :param selection_set_node: the SelectionSetNode to dig into
        :type selection_set_node: SelectionSetNode
        :return: list of FragmentSpreadNode found
        :rtype: List[FragmentSpreadNode]
        """
        node_id = id(selection_set_node)
        spreads = self._fragment_spreads.get(node_id)
        if spreads is None:
            spreads: List["FragmentSpreadNode"] = []
            sets_to_visit: List["SelectionSetNode"] = [selection_set_node]
            while sets_to_visit:
                set_to_visit = sets_to_visit.pop()
                for selection in set_to_visit.selections:
                    if isinstance(selection, FragmentSpreadNode):
                        spreads.append(selection)
                    elif (
                        isinstance(selection, _NODE_WITH_SELECTION_SET)
                        and selection.selection_set
                    ):
                        sets_to_visit.append(selection.selection_set)
            self._fragment_spreads[node_id] = spreads
        return spreads

    def get_recursively_referenced_fragments(
        self, operation_node: "OperationDefinitionNode"
    ) -> List["FragmentDefinitionNode"]:
        """
        Extract FragmentDefinitionNode for each spread fragment of an
        OperationDefinitionNode.
        :param operation_node: the OperationDefinitionNode to dig into
        :type operation_node: OperationDefinitionNode
        :return: list of spreaded FragmentDefinitionNode
        :rtype: List[FragmentDefinitionNode]
        """
        # pylint: disable=too-many-locals
        node_id = id(operation_node)
        fragments = self._recursively_referenced_fragments.get(node_id)
        if fragments is None:
            fragments: List["FragmentDefinitionNode"] = []
            collected_names: Set[str] = set()
            nodes_to_visit: List["SelectionSetNode"] = [
                operation_node.selection_set
            ]
            while nodes_to_visit:
                node = nodes_to_visit.pop()
                for spread in self.get_fragment_spreads(node):
                    fragment_name = spread.name.value
                    if fragment_name not in collected_names:
                        collected_names.add(fragment_name)
                        fragment = self.get_fragment(fragment_name)
                        if fragment:
                            fragments.append(fragment)
                            nodes_to_visit.append(fragment.selection_set)
            self._recursively_referenced_fragments[node_id] = fragments
        return fragments

    def get_variable_usages(
        self, node: Union["OperationDefinitionNode", "FragmentDefinitionNode"]
    ) -> List[Dict[str, Any]]:
        """
        Fetch and return variable usages for the provided node.
        :param node: the node to dig into
        :type node: Union[OperationDefinitionNode, FragmentDefinitionNode]
        :return: list of used variables on the node
        :rtype: List[Dict[str, Any]]
        """
        node_id = id(node)
        usages = self._variable_usages.get(node_id)
        if usages is not None:
            return usages

        type_info = TypeInfo(self.schema)
        variable_usage_visitor = VariableUsageVisitor(type_info)
        visit(node, WithTypeInfoVisitor(type_info, variable_usage_visitor))
        usages = variable_usage_visitor.usages
        self._variable_usages[node_id] = usages
        return usages

    def get_recursive_variable_usages(
        self, operation: "OperationDefinitionNode"
    ) -> List[Dict[str, Any]]:
        """
        Fetch and return variable usages for the OperationDefinitionNode.
        :param operation: the OperationDefinitionNode to dig into
        :type operation: OperationDefinitionNode
        :return: list of used variables on the OperationDefinitionNode
        :rtype: List[Dict[str, Any]]
        """
        operation_id = id(operation)
        usages = self._recursive_variable_usages.get(operation_id)
        if usages is None:
            usages = self.get_variable_usages(operation)
            for fragment in self.get_recursively_referenced_fragments(
                operation
            ):
                usages.extend(self.get_variable_usages(fragment))
            self._recursive_variable_usages[operation_id] = usages
        return usages

    def get_type(self) -> Optional["GraphQLOutputType"]:
        """
        Return the current GraphQLOutputType if one.
        :return: the current GraphQLOutputType if one
        :rtype: Optional[GraphQLOutputType]
        """
        return self._type_info.get_type()

    def get_field_def(self) -> Optional["GraphQLField"]:
        """
        Return the current GraphQLField if one.
        :return: the current GraphQLField if one
        :rtype: Optional[GraphQLField]
        """
        return self._type_info.get_field_def()

    def get_argument(self) -> Optional["GraphQLArgument"]:
        """
        Return the current GraphQLArgument if one.
        :return: the current GraphQLArgument if one
        :rtype: Optional[GraphQLArgument]
        """
        return self._type_info.get_argument()

    def get_parent_type(self) -> Optional["GraphQLCompositeType"]:
        """
        Return the GraphQLCompositeType parent type if one.
        :return: the GraphQLCompositeType parent type if one
        :rtype: Optional[GraphQLCompositeType]
        """
        return self._type_info.get_parent_type()

    def get_input_type(self) -> Optional["GraphQLInputType"]:
        """
        Return the current GraphQLInputType if one.
        :return: the current GraphQLInputType if one
        :rtype: Optional[GraphQLInputType]
        """
        return self._type_info.get_input_type()

    def get_parent_input_type(self) -> Optional["GraphQLInputType"]:
        """
        Return the parent GraphQLInputType if one.
        :return: the parent GraphQLInputType if one
        :rtype: Optional[GraphQLInputType]
        """
        return self._type_info.get_parent_input_type()
