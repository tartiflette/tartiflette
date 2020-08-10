from typing import Dict, List, Optional, Set, Tuple, Union

from tartiflette.language.ast import (
    EnumTypeDefinitionNode,
    InputObjectTypeDefinitionNode,
    ListTypeNode,
    NonNullTypeNode,
    ScalarTypeDefinitionNode,
)
from tartiflette.language.ast.base import TypeDefinitionNode
from tartiflette.utils.errors import graphql_error_from_nodes
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("InputObjectNoCircularRefRule",)

_INPUT_TYPES = (
    ScalarTypeDefinitionNode,
    EnumTypeDefinitionNode,
    InputObjectTypeDefinitionNode,
)


class InputObjectNoCircularRefValidator:
    """
    Validate that input object doesn't produce circular references.
    """

    def __init__(
        self,
        context: "ASTValidationContext",
        known_types: Dict[str, "TypeDefinitionNode"],
        known_input_objects: Dict[str, Dict[str, "InputValueDefinitionNode"]],
    ) -> None:
        """
        :param context: context forwarded to the validation rule
        :param known_types: all defined type definitions
        :param known_input_objects: all defined input object definitions
        :type context: ASTValidationContext
        :type known_types: Dict[str, TypeDefinitionNode]
        :type known_input_objects: Dict[str, Dict[str, InputValueDefinitionNode]]
        """
        self._context = context
        self._known_types = known_types
        self._known_input_objects = known_input_objects
        self._visited_types: Set[str] = set()
        self._field_path: List[Tuple[str, "InputValueDefinitionNode"]] = []
        self._field_path_index_by_type_name: Dict[str, int] = {}

    def __call__(
        self,
        input_obj_name: str,
        input_obj_fields: Dict[str, "InputValueDefinitionNode"],
    ) -> None:
        """
        Check for circular reference on the input object.
        :param input_obj_name: the name of the input object
        :param input_obj_fields: list of input fields of the input obejct
        :type input_obj_name: str
        :type input_obj_fields: Dict[str, InputValueDefinitionNode]
        """
        if input_obj_name in self._visited_types:
            return

        self._visited_types.add(input_obj_name)
        self._field_path_index_by_type_name[input_obj_name] = len(
            self._field_path
        )

        for field_def in input_obj_fields.values():
            if not isinstance(field_def.type, NonNullTypeNode) or isinstance(
                field_def.type.type, ListTypeNode
            ):
                continue

            field_def_type = self._known_types.get(
                field_def.type.type.name.value
            )

            if isinstance(field_def_type, InputObjectTypeDefinitionNode):
                field_type = field_def.type.type
                cycle_index = self._field_path_index_by_type_name.get(
                    field_type.name.value
                )

                self._field_path.append(field_def)
                if cycle_index is None:
                    self(
                        field_type.name.value,
                        self._known_input_objects.get(
                            field_type.name.value, {}
                        ),
                    )
                else:
                    cycle_path = self._field_path[cycle_index:]
                    path_str = ".".join(
                        [field_def.name.value for field_def in cycle_path]
                    )
                    self._context.report_error(
                        graphql_error_from_nodes(
                            "Cannot reference Input Object "
                            f"< {field_type.name.value} > within itself "
                            "through a series of non-null fields "
                            f"< {path_str} >.",
                            nodes=cycle_path,
                        )
                    )
                self._field_path.pop()
        del self._field_path_index_by_type_name[input_obj_name]


class InputObjectNoCircularRefRule(ASTValidationRule):
    """
    Validate that input object doesn't produce circular references.
    """

    def __init__(self, context: "ASTValidationContext") -> None:
        """
        :param context: context forwarded to the validation rule
        :type context: ASTValidationContext
        """
        super().__init__(context)
        self._known_input_objects: Dict[
            str, Dict[str, "InputValueDefinitionNode"]
        ] = {}
        self._known_types: Dict[str, "TypeDefinitionNode"] = {
            definition_node.name.value: definition_node
            for definition_node in context.document_node.definitions
            if isinstance(definition_node, TypeDefinitionNode)
        }

    def enter_InputValueDefinition(  # pylint: disable=invalid-name
        self,
        node: "InputValueDefinitionNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> None:
        """
        Collect input value definition per input object type.
        :param node: the current node being visiting
        :param key: the index/key to this node from the parent node/list
        :param parent: the parent immediately above this node
        :param path: the path to get to this node from the root node
        :param ancestors: nodes and list visited before reaching parent node
        :type node: InputValueDefinitionNode
        :type key: Optional[Union[int, str]]
        :type parent: Optional[Union[Node, List[Node]]]
        :type path: List[Union[int, str]]
        :type ancestors: List[Union[Node, List[Node]]]
        """
        # pylint: disable=unused-argument
        self._known_input_objects.setdefault(
            ancestors[-1].name.value, {}
        ).update({node.name.value: node})

    def leave_Document(  # pylint: disable=invalid-name
        self,
        node: "DocumentNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> None:
        """
        Check that collected input type doesn't have circular reference.
        :param node: the current node being visiting
        :param key: the index/key to this node from the parent node/list
        :param parent: the parent immediately above this node
        :param path: the path to get to this node from the root node
        :param ancestors: nodes and list visited before reaching parent node
        :type node: DocumentNode
        :type key: Optional[Union[int, str]]
        :type parent: Optional[Union[Node, List[Node]]]
        :type path: List[Union[int, str]]
        :type ancestors: List[Union[Node, List[Node]]]
        """
        # pylint: disable=unused-argument
        validator = InputObjectNoCircularRefValidator(
            self.context, self._known_types, self._known_input_objects
        )
        for (
            input_obj_name,
            input_obj_fields,
        ) in self._known_input_objects.items():
            validator(input_obj_name, input_obj_fields)
