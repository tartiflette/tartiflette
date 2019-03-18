from copy import deepcopy
from typing import Dict, List, Optional


def _create_node_name(gql_type: str, name: Optional[str] = None):
    node_name = gql_type
    if name:
        node_name = node_name + "(%s)" % name
    return node_name


class InternalVisitorContext:
    #  pylint: disable=too-many-locals,too-many-instance-attributes
    def __init__(
        self,
        operation: Optional["NodeOperationDefinition"] = None,
        node: Optional["NodeField"] = None,
        argument: Optional["NodeArgument"] = None,
        directive: Optional["NodeDirective"] = None,
        type_condition: Optional[str] = None,
        fragment_definition: Optional["NodeFragmentDefinition"] = None,
        inline_fragment_info: Optional["FragmentData"] = None,
        depth: int = 0,
        path: Optional[str] = None,
        field_path: Optional[List[str]] = None,
        fields: Optional[Dict[str, "GraphQLField"]] = None,
    ) -> None:
        # pylint: disable=too-many-arguments
        self._operation = operation
        self._node = node
        self._argument = argument
        self._directive = directive
        self._type_condition = type_condition
        self._fragment_definition = fragment_definition
        self._inline_fragment_info = inline_fragment_info
        self._depth = depth
        self._path = path or ""
        self._field_path = field_path or []
        self._fields = fields or {}
        self._current_object_value = None
        self._fragment_spread = None

    def clone(self) -> "InternalVisitorContext":
        return InternalVisitorContext(
            self._operation,
            self._node,
            self._argument,
            self._directive,
            self._type_condition,
            self._fragment_definition,
            self._inline_fragment_info,
            self._depth,
            self._path,
            deepcopy(self._field_path),
            dict(self._fields),
        )

    @property
    def fragment_spread(self) -> "FragmentData":
        return self._fragment_spread

    @fragment_spread.setter
    def fragment_spread(self, val: "FragmentData") -> None:
        self._fragment_spread = val

    @property
    def current_object_value(self) -> "ObjectValue":
        return self._current_object_value

    @current_object_value.setter
    def current_object_value(self, cov) -> None:
        self._current_object_value = cov

    @property
    def operation(self) -> Optional["NodeOperationDefinition"]:
        return self._operation

    @operation.setter
    def operation(self, val: "NodeOperationDefinition") -> None:
        self._operation = val

    @property
    def node(self) -> Optional["NodeField"]:
        return self._node

    @node.setter
    def node(self, val: "NodeField") -> None:
        self._node = val

    @property
    def argument(self) -> Optional[str]:
        return self._argument

    @argument.setter
    def argument(self, argument: "NodeArgument") -> None:
        self._argument = argument

    @property
    def directive(self) -> Optional["NodeDirective"]:
        return self._directive

    @directive.setter
    def directive(self, directive: "NodeDirective") -> None:
        self._directive = directive

    @property
    def type_condition(self) -> Optional[str]:
        return self._type_condition

    @type_condition.setter
    def type_condition(self, val: str) -> None:
        self._type_condition = val

    @property
    def fragment_definition(self) -> Optional["NodeFragmentDefinition"]:
        return self._fragment_definition

    @fragment_definition.setter
    def fragment_definition(self, val: "NodeFragmentDefinition") -> None:
        self._fragment_definition = val

    @property
    def inline_fragment_info(self) -> Optional["FragmentData"]:
        return self._inline_fragment_info

    @inline_fragment_info.setter
    def inline_fragment_info(self, val: "FragmentData") -> None:
        self._inline_fragment_info = val

    @property
    def depth(self) -> int:
        return len(self.field_path)

    @property
    def path(self) -> str:
        return self._path

    @path.setter
    def path(self, val: str) -> None:
        self._path = val

    @property
    def field_path(self) -> List[str]:
        return self._field_path

    @field_path.setter
    def field_path(self, val: List[str]) -> None:
        self._field_path = val

    @property
    def _hashed_field_path(self) -> str:
        return "/".join(self._field_path)

    @property
    def current_field(self) -> Optional["GraphQLField"]:
        try:
            return self._fields[self._hashed_field_path]
        except KeyError:
            pass
        return None

    def move_in(self, element: "_VisitorElement") -> None:
        self._path = self._path + "/%s" % _create_node_name(
            element.libgraphql_type, element.name
        )

    def move_out(self) -> None:
        self._path = "/".join(self._path.split("/")[:-1])

    def move_in_field(
        self, element: "_VisitorElement", field: "GraphQLField"
    ) -> None:
        self._field_path.append(element.name)
        self._fields[self._hashed_field_path] = field

    def move_out_field(self) -> None:
        self._fields.pop(self._hashed_field_path, None)
        if self.depth > 0:
            self._field_path.pop()
            self.node = self.node.parent

    def compute_type_cond(self, type_cond_depth: int) -> Optional[str]:
        if self.depth == type_cond_depth or (
            self.inline_fragment_info
            and self.depth == self.inline_fragment_info.depth
        ):
            return self.type_condition
        return None
