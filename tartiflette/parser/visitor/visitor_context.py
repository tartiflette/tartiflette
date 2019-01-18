from copy import deepcopy


def _create_node_name(gql_type, name=None):
    node_name = gql_type
    if name:
        node_name = node_name + "(%s)" % name
    return node_name


class InternalVisitorContext:
    def __init__(
        self,
        operation=None,
        node=None,
        argument_name=None,
        type_condition=None,
        fragment_definition=None,
        inline_fragment_info=None,
        depth=0,
        path=None,
        field_path=None,
    ):
        self._operation = operation
        self._node = node
        self._argument_name = argument_name
        self._type_condition = type_condition
        self._fragment_definition = fragment_definition
        self._inline_fragment_info = inline_fragment_info
        self._depth = depth
        self._path = path or ""
        self._field_path = field_path or []

    def clone(self):
        return InternalVisitorContext(
            self._operation,
            self._node,
            self._argument_name,
            self._type_condition,
            self._fragment_definition,
            self._inline_fragment_info,
            self._depth,
            self._path,
            deepcopy(self._field_path),
        )

    @property
    def operation(self):
        return self._operation

    @operation.setter
    def operation(self, val):
        self._operation = val

    @property
    def node(self):
        return self._node

    @node.setter
    def node(self, val):
        self._node = val

    @property
    def argument_name(self):
        return self._argument_name

    @argument_name.setter
    def argument_name(self, val):
        self._argument_name = val

    @property
    def type_condition(self):
        return self._type_condition

    @type_condition.setter
    def type_condition(self, val):
        self._type_condition = val

    @property
    def fragment_definition(self):
        return self._fragment_definition

    @fragment_definition.setter
    def fragment_definition(self, val):
        self._fragment_definition = val

    @property
    def inline_fragment_info(self):
        return self._inline_fragment_info

    @inline_fragment_info.setter
    def inline_fragment_info(self, val):
        self._inline_fragment_info = val

    @property
    def depth(self):
        return len(self.field_path)

    @property
    def path(self):
        return self._path

    @property
    def field_path(self):
        return self._field_path

    def move_in(self, element):
        self._path = self._path + "/%s" % _create_node_name(
            element.libgraphql_type, element.name
        )

    def move_out(self):
        self._path = "/".join(self._path.split("/")[:-1])

    def move_in_field(self, element):
        self._field_path.append(element.name)

    def move_out_field(self):
        if self.depth > 0:
            self._field_path.pop()
            self.node = self.node.parent

    def compute_type_cond(self, type_cond_depth):
        if self.depth == type_cond_depth or (
            self.inline_fragment_info
            and self.depth == self.inline_fragment_info.depth
        ):
            return self.type_condition
        return None
