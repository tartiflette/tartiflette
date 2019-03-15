from typing import List, Optional

from tartiflette.language.ast.base import Node, ValueNode


class BooleanValueNode(ValueNode):
    """
    TODO:
    """

    __slots__ = ("value", "location")

    def __init__(
        self, value: bool, location: Optional["Location"] = None
    ) -> None:
        """
        TODO:
        :param value: TODO:
        :param location: TODO:
        :type value: TODO:
        :type location: TODO:
        """
        self.value = value
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
            isinstance(other, BooleanValueNode)
            and (self.value == other.value and self.location == other.location)
        )

    def __repr__(self) -> str:
        """
        TODO:
        :return: TODO:
        :rtype: TODO:
        """
        return "BooleanValueNode(value=%r, location=%r)" % (
            self.value,
            self.location,
        )


class EnumValueNode(ValueNode):
    """
    TODO:
    """

    __slots__ = ("value", "location")

    def __init__(
        self, value: str, location: Optional["Location"] = None
    ) -> None:
        """
        TODO:
        :param value: TODO:
        :param location: TODO:
        :type value: TODO:
        :type location: TODO:
        """
        self.value = value
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
            isinstance(other, EnumValueNode)
            and (self.value == other.value and self.location == other.location)
        )

    def __repr__(self) -> str:
        """
        TODO:
        :return: TODO:
        :rtype: TODO:
        """
        return "EnumValueNode(value=%r, location=%r)" % (
            self.value,
            self.location,
        )


class FloatValueNode(ValueNode):
    """
    TODO:
    """

    __slots__ = ("value", "location")

    def __init__(
        self, value: str, location: Optional["Location"] = None
    ) -> None:
        """
        TODO:
        :param value: TODO:
        :param location: TODO:
        :type value: TODO:
        :type location: TODO:
        """
        self.value = value
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
            isinstance(other, FloatValueNode)
            and (self.value == other.value and self.location == other.location)
        )

    def __repr__(self) -> str:
        """
        TODO:
        :return: TODO:
        :rtype: TODO:
        """
        return "FloatValueNode(value=%r, location=%r)" % (
            self.value,
            self.location,
        )


class IntValueNode(ValueNode):
    """
    TODO:
    """

    __slots__ = ("value", "location")

    def __init__(
        self, value: str, location: Optional["Location"] = None
    ) -> None:
        """
        TODO:
        :param value: TODO:
        :param location: TODO:
        :type value: TODO:
        :type location: TODO:
        """
        self.value = value
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
            isinstance(other, IntValueNode)
            and (self.value == other.value and self.location == other.location)
        )

    def __repr__(self) -> str:
        """
        TODO:
        :return: TODO:
        :rtype: TODO:
        """
        return "IntValueNode(value=%r, location=%r)" % (
            self.value,
            self.location,
        )


class NullValueNode(ValueNode):
    """
    TODO:
    """

    __slots__ = ("value", "location")

    def __init__(self, location: Optional["Location"] = None) -> None:
        """
        TODO:
        :param location: TODO:
        :type location: TODO:
        """
        self.value = None
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
            isinstance(other, NullValueNode)
            and (self.value == other.value and self.location == other.location)
        )

    def __repr__(self) -> str:
        """
        TODO:
        :return: TODO:
        :rtype: TODO:
        """
        return "NullValueNode(location=%r)" % self.location


class StringValueNode(ValueNode):
    """
    TODO:
    """

    __slots__ = ("value", "location")

    def __init__(
        self, value: str, location: Optional["Location"] = None
    ) -> None:
        """
        TODO:
        :param value: TODO:
        :param location: TODO:
        :type value: TODO:
        :type location: TODO:
        """
        self.value = value
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
            isinstance(other, StringValueNode)
            and (self.value == other.value and self.location == other.location)
        )

    def __repr__(self) -> str:
        """
        TODO:
        :return: TODO:
        :rtype: TODO:
        """
        return "StringValueNode(value=%r, location=%r)" % (
            self.value,
            self.location,
        )


class ListValueNode(ValueNode):
    """
    TODO:
    """

    __slots__ = ("values", "location")

    def __init__(
        self, values: List["ValueNode"], location: Optional["Location"] = None
    ) -> None:
        """
        TODO:
        :param values: TODO:
        :param location: TODO:
        :type values: TODO:
        :type location: TODO:
        """
        self.values = values
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
            isinstance(other, ListValueNode)
            and (
                self.values == other.values and self.location == other.location
            )
        )

    def __repr__(self) -> str:
        """
        TODO:
        :return: TODO:
        :rtype: TODO:
        """
        return "ListValueNode(values=%r, location=%r)" % (
            self.values,
            self.location,
        )


class ObjectFieldNode(Node):
    """
    TODO:
    """

    __slots__ = ("name", "value", "location")

    def __init__(
        self,
        name: "NameNode",
        value: "ValueNode",
        location: Optional["Location"] = None,
    ) -> None:
        """
        TODO:
        :param name: TODO:
        :param value: TODO:
        :param location: TODO:
        :type name: TODO:
        :type value: TODO:
        :type location: TODO:
        """
        self.name = name
        self.value = value
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
            isinstance(other, ObjectFieldNode)
            and (
                self.name == other.name
                and self.value == other.value
                and self.location == other.location
            )
        )

    def __repr__(self) -> str:
        """
        TODO:
        :return: TODO:
        :rtype: TODO:
        """
        return "ObjectFieldNode(name=%r, value=%r, location=%r)" % (
            self.name,
            self.value,
            self.location,
        )


class ObjectValueNode(Node):
    """
    TODO:
    """

    __slots__ = ("fields", "location")

    def __init__(
        self,
        fields: List["ObjectFieldNode"],
        location: Optional["Location"] = None,
    ) -> None:
        """
        TODO:
        :param fields: TODO:
        :param location: TODO:
        :type fields: TODO:
        :type location: TODO:
        """
        self.fields = fields
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
            isinstance(other, ObjectValueNode)
            and (
                self.fields == other.fields and self.location == other.location
            )
        )

    def __repr__(self) -> str:
        """
        TODO:
        :return: TODO:
        :rtype: TODO:
        """
        return "ObjectValueNode(fields=%r, location=%r)" % (
            self.fields,
            self.location,
        )
