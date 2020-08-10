from typing import Dict, List, Optional, Set, Union

from tartiflette.language.ast import (
    ListTypeNode,
    NamedTypeNode,
    NonNullTypeNode,
    ObjectTypeDefinitionNode,
    ObjectTypeExtensionNode,
)
from tartiflette.language.ast.base import TypeDefinitionNode
from tartiflette.language.visitor.constants import SKIP
from tartiflette.utils.errors import graphql_error_from_nodes
from tartiflette.validation.rules.base import ASTValidationRule

__all__ = ("ValidObjectImplementsRule",)


def _is_type_sub_type_of(
    known_types: Dict[str, "TypeDefinitionNode"],
    maybe_sub_type: "Node",
    super_type: "Node",
) -> bool:
    """
    Determine whether or not a type is a sub-type of another.
    :param known_types: all defined type definitions
    :param maybe_sub_type: type which should be a sub-type of the other
    :param super_type: super type that should be implemented
    :type known_types: Dict[str, TypeDefinitionNode]
    :type maybe_sub_type: Node
    :type super_type: Node
    :return: whether or not a type is a sub-type of another
    :rtype: bool
    """
    # pylint: disable=too-complex
    if isinstance(maybe_sub_type, NamedTypeNode):
        maybe_sub_type = known_types[maybe_sub_type.name.value]

    if isinstance(super_type, NamedTypeNode):
        super_type = known_types[super_type.name.value]

    if maybe_sub_type is super_type:
        return True

    if isinstance(super_type, NonNullTypeNode):
        if isinstance(maybe_sub_type, NonNullTypeNode):
            return _is_type_sub_type_of(
                known_types, maybe_sub_type.type, super_type.type
            )
        return False

    if isinstance(maybe_sub_type, NonNullTypeNode):
        return _is_type_sub_type_of(
            known_types, maybe_sub_type.type, super_type
        )

    if isinstance(super_type, ListTypeNode):
        if isinstance(maybe_sub_type, ListTypeNode):
            return _is_type_sub_type_of(
                known_types, maybe_sub_type.type, super_type.type
            )
        return False

    if isinstance(maybe_sub_type, ListTypeNode):
        return False

    if isinstance(maybe_sub_type, ObjectTypeDefinitionNode):
        for interface in maybe_sub_type.interfaces:
            if super_type is known_types[interface.name.value]:
                return True

    return False


def _is_equal_type(type_a: "Node", type_b: "Node") -> bool:
    """
    Determine whether or not two node types are equals.
    :param type_a: first type to check
    :param type_b: second type to check
    :type type_a: Node
    :type type_b: Node
    :return: whether or not two node types are equals
    :rtype: bool
    """
    if isinstance(type_a, NamedTypeNode) and isinstance(type_b, NamedTypeNode):
        return type_a.name.value == type_b.name.value

    if isinstance(type_a, NonNullTypeNode) and isinstance(
        type_b, NonNullTypeNode
    ):
        return _is_equal_type(type_a.type, type_b.type)

    if isinstance(type_a, ListTypeNode) and isinstance(type_b, ListTypeNode):
        return _is_equal_type(type_a.type, type_b.type)

    return False


# TODO: refactor since defined also through _is_required_argument_node()
def _is_required_argument(
    input_value_node: "InputValueDefinitionNode",
) -> bool:
    """
    Determine whether or not an InputValueDefinitionNode is required.
    :param input_value_node: the InputValueDefinitionNode instance to check
    :type input_value_node: InputValueDefinitionNode
    :return: whether or not an InputValueDefinitionNode is required
    :rtype: bool
    """
    return (
        isinstance(input_value_node.type, NonNullTypeNode)
        and input_value_node.default_value is None
    )


class ValidObjectImplementsRule(ASTValidationRule):
    """
    Validate that object properly implements their interfaces.
    """

    def __init__(self, context: "ASTValidationContext") -> None:
        """
        :param context: context forwarded to the validation rule
        :type context: ASTValidationContext
        """
        super().__init__(context)
        self._known_types: Dict[str, "TypeDefinitionNode"] = {
            definition_node.name.value: definition_node
            for definition_node in context.document_node.definitions
            if isinstance(definition_node, TypeDefinitionNode)
        }
        self._known_interfaces: Dict[
            str, Dict[str, "FieldDefinitionNode"]
        ] = {}
        self._known_objects: Dict[str, Dict[str, "FieldDefinitionNode"]] = {}
        self._object_with_interfaces: Dict[str, Set[str]] = {}
        self._interface_arguments: Dict[
            str, Dict[str, "InputValueDefinitionNode"]
        ] = {}
        self._object_arguments: Dict[
            str, Dict[str, "InputValueDefinitionNode"]
        ] = {}

    def _collect_fields(
        self,
        node: Union[
            "InterfaceTypeDefinitionNode",
            "InterfaceTypeExtensionNode",
            "ObjectTypeDefinitionNode",
            "ObjectTypeExtensionNode",
        ],
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> SKIP:
        """
        Collect fields and arguments of interface and object types.
        :param node: the current node being visiting
        :param key: the index/key to this node from the parent node/list
        :param parent: the parent immediately above this node
        :param path: the path to get to this node from the root node
        :param ancestors: nodes and list visited before reaching parent node
        :type node: Union[
            "InterfaceTypeDefinitionNode",
            "InterfaceTypeExtensionNode",
            "ObjectTypeDefinitionNode",
            "ObjectTypeExtensionNode",
        ]
        :type key: Optional[Union[int, str]]
        :type parent: Optional[Union[Node, List[Node]]]
        :type path: List[Union[int, str]]
        :type ancestors: List[Union[Node, List[Node]]]
        :return: the SKIP visitor constant
        :rtype: SKIP
        """
        # pylint: disable=unused-argument
        type_name = node.name.value
        is_object = isinstance(
            node, (ObjectTypeDefinitionNode, ObjectTypeExtensionNode)
        )

        if is_object and node.interfaces:
            self._object_with_interfaces.setdefault(type_name, set()).update(
                {
                    interface_node.name.value
                    for interface_node in node.interfaces
                }
            )

        if node.fields:
            known_fields = (
                self._known_objects if is_object else self._known_interfaces
            )
            known_fields.setdefault(type_name, {})
            for field_definition in node.fields:
                field_name = field_definition.name.value
                known_fields[type_name][field_name] = field_definition

                if field_definition.arguments:
                    known_arguments = (
                        self._object_arguments
                        if is_object
                        else self._interface_arguments
                    )
                    type_field_key = f"{type_name}.{field_name}"
                    known_arguments.setdefault(type_field_key, {})
                    for argument_definition in field_definition.arguments:
                        known_arguments[type_field_key][
                            argument_definition.name.value
                        ] = argument_definition
        return SKIP

    def leave_Document(  # pylint: disable=invalid-name
        self,
        node: "DocumentNode",
        key: Optional[Union[int, str]],
        parent: Optional[Union["Node", List["Node"]]],
        path: List[Union[int, str]],
        ancestors: List[Union["Node", List["Node"]]],
    ) -> None:
        """
        Validate that each object type implements their interfaces.
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
        # pylint: disable=unused-argument,too-complex,too-many-locals
        for (
            object_name,
            implemented_interfaces,
        ) in self._object_with_interfaces.items():
            object_fields = self._known_objects.get(object_name, {})
            for interface_name in implemented_interfaces:
                interface_fields = self._known_interfaces.get(interface_name)
                if not interface_fields:
                    continue

                for field_name, field_definition in interface_fields.items():
                    object_field = object_fields.get(field_name)
                    if object_field is None:
                        self.context.report_error(
                            graphql_error_from_nodes(
                                "Interface field "
                                f"< {interface_name}.{field_name} > expected "
                                f"but < {object_name} > does not provide it.",
                                nodes=[field_definition],
                            )
                        )
                        continue

                    if not _is_type_sub_type_of(
                        self._known_types,
                        object_field.type,
                        field_definition.type,
                    ):
                        self.context.report_error(
                            graphql_error_from_nodes(
                                "Interface field "
                                f"< {interface_name}.{field_name} > expects "
                                f"type < {field_definition.type} > but "
                                f"< {object_name}.{field_name} > is type "
                                f"< {object_field.type} >.",
                                nodes=[
                                    field_definition.type,
                                    object_field.type,
                                ],
                            )
                        )
                        continue

                    iface_field_args = self._interface_arguments.get(
                        f"{interface_name}.{field_name}", {}
                    )
                    obj_field_args = self._object_arguments.get(
                        f"{object_name}.{field_name}", {}
                    )
                    for (
                        iface_arg_name,
                        iface_arg_def,
                    ) in iface_field_args.items():
                        obj_arg_def = obj_field_args.get(iface_arg_name)
                        if obj_arg_def is None:
                            self.context.report_error(
                                graphql_error_from_nodes(
                                    "Interface field argument "
                                    f"< {interface_name}.{field_name}({iface_arg_name}:) > "
                                    "expected but "
                                    f"< {object_name}.{field_name} > does not "
                                    f"provide it.",
                                    nodes=[iface_arg_def, object_field],
                                )
                            )
                            continue

                        if not _is_equal_type(
                            iface_arg_def.type, obj_arg_def.type
                        ):
                            self.context.report_error(
                                graphql_error_from_nodes(
                                    "Interface field argument "
                                    f"< {interface_name}.{field_name}({iface_arg_name}:) > "
                                    f"expects type < {iface_arg_def.type} > "
                                    f"but < {object_name}.{field_name}({iface_arg_name}:) > "
                                    f"is type < {obj_arg_def.type} >.",
                                    nodes=[iface_arg_def, obj_arg_def],
                                )
                            )

                    for obj_arg_name, obj_arg_def in obj_field_args.items():
                        iface_arg_def = iface_field_args.get(obj_arg_name)
                        if iface_arg_def is None and _is_required_argument(
                            obj_arg_def
                        ):
                            self.context.report_error(
                                graphql_error_from_nodes(
                                    "Object field "
                                    f"< {object_name}.{field_name} > includes "
                                    f"required argument {obj_arg_name} that "
                                    "is missing from the Interface field "
                                    f"< {interface_name}.{field_name} >.",
                                    nodes=[obj_arg_def, field_definition],
                                )
                            )

    enter_InterfaceTypeDefinition = _collect_fields
    enter_InterfaceTypeExtension = _collect_fields
    enter_ObjectTypeDefinition = _collect_fields
    enter_ObjectTypeExtension = _collect_fields
