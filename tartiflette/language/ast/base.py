class Node:
    __slots__ = ()


class DefinitionNode(Node):
    __slots__ = ()


class ExecutableDefinitionNode(DefinitionNode):
    __slots__ = ()


class TypeSystemDefinitionNode(DefinitionNode):
    __slots__ = ()


class TypeSystemExtensionNode(DefinitionNode):
    __slots__ = ()


class TypeDefinitionNode(TypeSystemDefinitionNode):
    __slots__ = ()


class TypeExtensionNode(TypeSystemExtensionNode):
    __slots__ = ()


class SelectionNode(Node):
    __slots__ = ()


class ValueNode(Node):
    __slots__ = ()


class TypeNode(Node):
    __slots__ = ()
