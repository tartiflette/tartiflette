from typing import Any, List, Optional

from tartiflette.language.ast.base import Node, ValueNode


class BooleanValueNode(ValueNode):
    """
    AST node representing a GraphQL boolean value.
    """

    __slots__ = ("value", "location")

    def __init__(
        self, value: bool, location: Optional["Location"] = None
    ) -> None:
        """
        :param value: value of the boolean value
        :param location: location of the boolean value in the query/SDL
        :type value: bool
        :type location: Optional[Location]
        """
        self.value = value
        self.location = location

    def __eq__(self, other: Any) -> bool:
        """
        Returns True if `other` instance is identical to `self`.
        :param other: object instance to compare to `self`
        :type other: Any
        :return: whether or not `other` is identical to `self`
        :rtype: bool
        """
        return self is other or (
            isinstance(other, BooleanValueNode)
            and (self.value == other.value and self.location == other.location)
        )

    def __repr__(self) -> str:
        """
        Returns the representation of a BooleanValueNode instance.
        :return: the representation of a BooleanValueNode instance
        :rtype: str
        """
        return "BooleanValueNode(value=%r, location=%r)" % (
            self.value,
            self.location,
        )


class EnumValueNode(ValueNode):
    """
    AST node representing a GraphQL enum value.
    """

    __slots__ = ("value", "location")

    def __init__(
        self, value: str, location: Optional["Location"] = None
    ) -> None:
        """
        :param value: value of the enum value
        :param location: location of the enum value in the query/SDL
        :type value: str
        :type location: Optional[Location]
        """
        self.value = value
        self.location = location

    def __eq__(self, other: Any) -> bool:
        """
        Returns True if `other` instance is identical to `self`.
        :param other: object instance to compare to `self`
        :type other: Any
        :return: whether or not `other` is identical to `self`
        :rtype: bool
        """
        return self is other or (
            isinstance(other, EnumValueNode)
            and (self.value == other.value and self.location == other.location)
        )

    def __repr__(self) -> str:
        """
        Returns the representation of an EnumValueNode instance.
        :return: the representation of an EnumValueNode instance
        :rtype: str
        """
        return "EnumValueNode(value=%r, location=%r)" % (
            self.value,
            self.location,
        )


class FloatValueNode(ValueNode):
    """
    AST node representing a GraphQL float value.
    """

    __slots__ = ("value", "location")

    def __init__(
        self, value: float, location: Optional["Location"] = None
    ) -> None:
        """
        :param value: value of the float value:
        :param location: location of the float value in the query/SDL
        :type value: float
        :type location: Optional[Location]
        """
        self.value = value
        self.location = location

    def __eq__(self, other: Any) -> bool:
        """
        Returns True if `other` instance is identical to `self`.
        :param other: object instance to compare to `self`
        :type other: Any
        :return: whether or not `other` is identical to `self`
        :rtype: bool
        """
        return self is other or (
            isinstance(other, FloatValueNode)
            and (self.value == other.value and self.location == other.location)
        )

    def __repr__(self) -> str:
        """
        Returns the representation of a FloatValueNode instance.
        :return: the representation of a FloatValueNode instance
        :rtype: str
        """
        return "FloatValueNode(value=%r, location=%r)" % (
            self.value,
            self.location,
        )


class IntValueNode(ValueNode):
    """
    AST node representing a GraphQL integer value.
    """

    __slots__ = ("value", "location")

    def __init__(
        self, value: int, location: Optional["Location"] = None
    ) -> None:
        """
        :param value: value of the int value
        :param location: location of the int value in the query/SDL
        :type value: int
        :type location: Optional[Location]
        """
        self.value = value
        self.location = location

    def __eq__(self, other: Any) -> bool:
        """
        Returns True if `other` instance is identical to `self`.
        :param other: object instance to compare to `self`
        :type other: Any
        :return: whether or not `other` is identical to `self`
        :rtype: bool
        """
        return self is other or (
            isinstance(other, IntValueNode)
            and (self.value == other.value and self.location == other.location)
        )

    def __repr__(self) -> str:
        """
        Returns the representation of an IntValueNode instance.
        :return: the representation of an IntValueNode instance
        :rtype: str
        """
        return "IntValueNode(value=%r, location=%r)" % (
            self.value,
            self.location,
        )


class NullValueNode(ValueNode):
    """
    AST node representing a GraphQL null value.
    """

    __slots__ = ("value", "location")

    def __init__(self, location: Optional["Location"] = None) -> None:
        """
        :param location: location of the null value in the query/SDL
        :type location: Optional[Location]
        """
        self.value: None = None
        self.location = location

    def __eq__(self, other: Any) -> bool:
        """
        Returns True if `other` instance is identical to `self`.
        :param other: object instance to compare to `self`
        :type other: Any
        :return: whether or not `other` is identical to `self`
        :rtype: bool
        """
        return self is other or (
            isinstance(other, NullValueNode)
            and (self.value == other.value and self.location == other.location)
        )

    def __repr__(self) -> str:
        """
        Returns the representation of a NullValueNode instance.
        :return: the representation of a NullValueNode instance
        :rtype: str
        """
        return "NullValueNode(location=%r)" % self.location


class StringValueNode(ValueNode):
    """
    AST node representing a GraphQL string value.
    """

    __slots__ = ("value", "location")

    def __init__(
        self, value: str, location: Optional["Location"] = None
    ) -> None:
        """
        :param value: value of the string value
        :param location: location of the string value in the query/SDL
        :type value: str
        :type location: Optional[Location]
        """
        self.value = value
        self.location = location

    def __eq__(self, other: Any) -> bool:
        """
        Returns True if `other` instance is identical to `self`.
        :param other: object instance to compare to `self`
        :type other: Any
        :return: whether or not `other` is identical to `self`
        :rtype: bool
        """
        return self is other or (
            isinstance(other, StringValueNode)
            and (self.value == other.value and self.location == other.location)
        )

    def __repr__(self) -> str:
        """
        Returns the representation of a StringValueNode instance.
        :return: the representation of a StringValueNode instance
        :rtype: str
        """
        return "StringValueNode(value=%r, location=%r)" % (
            self.value,
            self.location,
        )


class ListValueNode(ValueNode):
    """
    AST node representing a GraphQL list value.
    """

    __slots__ = ("values", "location")

    def __init__(
        self, values: List["ValueNode"], location: Optional["Location"] = None
    ) -> None:
        """
        :param values: values of the list value
        :param location: location of the list value in the query/SDL
        :type values: List[ValueNode]
        :type location: Optional[Location]
        """
        self.values = values
        self.location = location

    def __eq__(self, other: Any) -> bool:
        """
        Returns True if `other` instance is identical to `self`.
        :param other: object instance to compare to `self`
        :type other: Any
        :return: whether or not `other` is identical to `self`
        :rtype: bool
        """
        return self is other or (
            isinstance(other, ListValueNode)
            and (
                self.values == other.values and self.location == other.location
            )
        )

    def __repr__(self) -> str:
        """
        Returns the representation of a ListValueNode instance.
        :return: the representation of a ListValueNode instance
        :rtype: str
        """
        return "ListValueNode(values=%r, location=%r)" % (
            self.values,
            self.location,
        )


class ObjectFieldNode(Node):
    """
    AST node representing a GraphQL object field.
    """

    __slots__ = ("name", "value", "location")

    def __init__(
        self,
        name: "NameNode",
        value: "ValueNode",
        location: Optional["Location"] = None,
    ) -> None:
        """
        :param name: name of the object field
        :param value: value of the object field
        :param location: location of the object field in the query/SDL
        :type name: NameNode
        :type value: ValueNode
        :type location: Optional[Location]
        """
        self.name = name
        self.value = value
        self.location = location

    def __eq__(self, other: Any) -> bool:
        """
        Returns True if `other` instance is identical to `self`.
        :param other: object instance to compare to `self`
        :type other: Any
        :return: whether or not `other` is identical to `self`
        :rtype: bool
        """
        return self is other or (
            isinstance(other, ObjectFieldNode)
            and (
                self.name == other.name
                and self.value == other.value
                and self.location == other.location
            )
        )

    def __repr__(self) -> str:
        """
        Returns the representation of an ObjectFieldNode instance.
        :return: the representation of an ObjectFieldNode instance
        :rtype: str
        """
        return "ObjectFieldNode(name=%r, value=%r, location=%r)" % (
            self.name,
            self.value,
            self.location,
        )


class ObjectValueNode(ValueNode):
    """
    AST node representing a GraphQL object value.
    """

    __slots__ = ("fields", "location")

    def __init__(
        self,
        fields: List["ObjectFieldNode"],
        location: Optional["Location"] = None,
    ) -> None:
        """
        :param fields: fields of the object value
        :param location: location of the object value in the query/SDL
        :type fields: List[ObjectFieldNode]
        :type location: Optional[Location]
        """
        self.fields = fields
        self.location = location

    def __eq__(self, other: Any) -> bool:
        """
        Returns True if `other` instance is identical to `self`.
        :param other: object instance to compare to `self`
        :type other: Any
        :return: whether or not `other` is identical to `self`
        :rtype: bool
        """
        return self is other or (
            isinstance(other, ObjectValueNode)
            and (
                self.fields == other.fields and self.location == other.location
            )
        )

    def __repr__(self) -> str:
        """
        Returns the representation of an ObjectValueNode instance.
        :return: the representation of an ObjectValueNode instance
        :rtype: str
        """
        return "ObjectValueNode(fields=%r, location=%r)" % (
            self.fields,
            self.location,
        )
