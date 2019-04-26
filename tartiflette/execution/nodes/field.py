from typing import Any, Callable, Dict, List, Optional


class ExecutableFieldNode:
    """
    Node representing a GraphQL executable field.
    """

    def __init__(
        self,
        name: str,
        schema: "GraphQLSchema",
        resolver: Callable,
        path: List[str],
        type_condition: str,
        alias: Optional[str] = None,
        subscribe: Optional[Callable] = None,
        parent: Optional["ExecutableFieldNode"] = None,
        fields: Optional[List["ExecutableFieldNode"]] = None,
        arguments: Optional[Dict[str, Any]] = None,
        directives: Optional[List["DirectiveNode"]] = None,
    ) -> None:
        """
        :param name: name of the field
        :param schema: GraphQLSchema to use while executing the field
        :param resolver: callable to use to resolve the field
        :param path: path of the field in the query
        :param type_condition: type condition of the field
        :param alias: alias of the field
        :param subscribe: callable to use on subscription requests
        :param parent: parent executable field of the field
        :param fields: collected executable fields of the field
        :param arguments: arguments of the field
        :param directives: directives of the field
        :type name: str
        :type schema: GraphQLSchema
        :type resolver: Callable
        :type path: List[str]
        :type type_condition: str
        :type alias: Optional[str]
        :type subscribe: Optional[Callable]
        :type parent: Optional[ExecutableFieldNode]
        :type fields: Optional[List[ExecutableFieldNode]]
        :type arguments: Optional[Dict[str, Any]]
        :type directives: Optional[List[DirectiveNode]]
        """
        # pylint: disable=too-many-arguments,too-many-locals
        self.name = name
        self.schema = schema
        self.resolver = resolver
        self.path = path
        self.type_condition = type_condition
        self.alias = alias
        self.subscribe = subscribe
        self.parent = parent
        self.fields = fields if fields is not None else {}
        self.arguments = arguments if arguments is not None else {}
        self.directives = directives if directives is not None else []
        self.definitions: List["FieldNode"] = []

    def __repr__(self) -> str:
        """
        Returns the representation of an ExecutableFieldNode instance.
        :return: the representation of an ExecutableFieldNode instance
        :rtype: str
        """
        return (
            "ExecutableFieldNode(alias=%r, name=%r, type_condition=%r, "
            "path=%r, fields=%r, arguments=%r, directives=%r, "
            "definitions=%r)"
            % (
                self.alias,
                self.name,
                self.type_condition,
                self.path,
                self.fields,
                self.arguments,
                self.directives,
                self.definitions,
            )
        )
