from typing import Any, Callable, Dict, Optional, Union

__all__ = ("GraphQLType", "GraphQLWrappingType", "GraphQLAbstractType")


class GraphQLType:
    """
    Definition of a GraphQL type.
    """

    is_wrapping_type = False
    is_list_type = False
    is_non_null_type = False
    is_abstract_type = False

    # Introspection attributes
    kind = "TYPE"
    ofType = None

    def __eq__(self, other: Any) -> bool:
        """
        Returns True if `other` instance is identical to `self`.
        :param other: object instance to compare to `self`
        :type other: Any
        :return: whether or not `other` is identical to `self`
        :rtype: bool
        """
        return self is other or type(self) is type(other)

    def __repr__(self) -> str:
        """
        Returns the representation of a GraphQLType instance.
        :return: the representation of a GraphQLType instance
        :rtype: str
        """
        return "{}()".format(self.__class__.__name__)


class GraphQLWrappingType(GraphQLType):
    """
    Definition of a GraphQL wrapping type.
    """

    is_wrapping_type = True

    def __init__(
        self,
        gql_type: Union["GraphQLList", str],
        schema: Optional["GraphQLSchema"] = None,
    ) -> None:
        """
        :param gql_type: inner GraphQL type of the wrapping type
        :param schema: the GraphQLSchema instance linked to the type
        :type gql_type: Union[GraphQLList, str]
        :type schema: Optional[GraphQLSchema]
        """
        self._schema = schema
        self.gql_type = gql_type

    # Introspection attribute
    @property
    def ofType(self) -> "GraphQLType":  # pylint: disable=invalid-name
        """
        Returns the inner type of the wrapping type which is used by the
        introspection query.
        :return: the inner type of the wrapping type
        :rtype: GraphQLType
        """
        return self.wrapped_type

    @property
    def wrapped_type(self) -> "GraphQLType":
        """
        Returns the wrapped GraphQL type of the wrapping type.
        :return: the wrapped GraphQL type of the wrapping type
        :rtype: GraphQLType
        """
        return (
            self.gql_type
            if isinstance(self.gql_type, GraphQLType)
            else self._schema.find_type(self.gql_type)
        )


class GraphQLAbstractType(GraphQLType):
    """
    Definition of a GraphQL abstract type.
    """

    is_abstract_type = True

    def __init__(self) -> None:
        self.type_resolver: Optional[Callable] = None
        self._fields_type_resolvers: Dict[str, Callable] = {}

    def add_field_type_resolver(
        self, field_name: str, implementation: Callable
    ) -> None:
        """
        Adds a type resolver callable for a dedicated field.
        :param field_name: field related to the type resolver
        :param implementation: implementation of the type resolver
        :type field_name: str
        :type implementation: Callable
        """
        self._fields_type_resolvers[field_name] = implementation

    def get_type_resolver(
        self, field_name: str, default_type_resolver: Callable
    ) -> Callable:
        """
        Returns the appropriate type resolver for the field name.
        :param field_name: field name for which returns the type resolver
        :param default_type_resolver: TODO:
        :type field_name: str
        :type default_type_resolver: Callable
        :return: appropriate type resolver for the field name
        :rtype: Callable
        """
        if field_name in self._fields_type_resolvers:
            return self._fields_type_resolvers[field_name]
        return self.type_resolver or default_type_resolver
