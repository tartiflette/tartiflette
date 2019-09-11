from typing import Any, Iterable, List, Optional, Union

from tartiflette.types.exceptions.tartiflette import CoercionError

__all__ = ("Path", "CoercionResult", "coercion_error")


class Path:
    """
    Representations of the path traveled during the coercion.
    """

    __slots__ = ("prev", "key")

    def __init__(self, prev: Optional["Path"], key: Union[str, int]) -> None:
        """
        :param prev: the previous value of the path
        :param key: the current value of the path
        :type prev: Optional[Path]
        :type key: Union[str, int]
        """
        self.prev = prev
        self.key = key

    def __repr__(self) -> str:
        """
        Returns the representation of an Path instance.
        :return: the representation of an Path instance
        :rtype: str
        """
        return "Path(prev=%r, key=%r)" % (self.prev, self.key)

    def __str__(self) -> str:
        """
        Returns a human-readable representation of the full path.
        :return: a human-readable representation of the full path
        :rtype: str
        """
        path_str = ""
        current_path = self
        while current_path:
            path_str = (
                f".{current_path.key}"
                if isinstance(current_path.key, str)
                else f"[{current_path.key}]"
            ) + path_str
            current_path = current_path.prev
        return f"value{path_str}" if path_str else ""

    def as_list(self) -> List[str]:
        """
        Computes and returns the path as a list.
        :return: the full path as a list
        :rtype: List[str]
        """
        path = []
        current_path = self
        while current_path:
            path.append(current_path.key)
            current_path = current_path.prev
        return path[::-1]


class CoercionResult:
    """
    Represents the result of a coercion.
    """

    __slots__ = ("value", "errors")

    def __init__(
        self,
        value: Optional[Any] = None,
        errors: Optional[List["TartifletteError"]] = None,
    ) -> None:
        """
        :param value: the computed value
        :param errors: the errors encountered
        :type value: Optional[Any]
        :type errors: Optional[List[TartifletteError]]
        """
        self.value = value if not errors else None
        self.errors = errors

    def __repr__(self) -> str:
        """
        Returns the representation of a CoercionResult instance.
        :return: the representation of a CoercionResult instance
        :rtype: str
        """
        return "CoercionResult(value=%r, errors=%r)" % (
            self.value,
            self.errors,
        )

    def __iter__(self) -> Iterable:
        """
        Returns an iterator over the computed value and errors encountered to
        allow unpacking the value like a tuple.
        :return: an iterator over the computed value and errors encountered
        :rtype: Iterable
        """
        yield from [self.value, self.errors]


def coercion_error(
    message: str,
    node: Optional["Node"] = None,
    path: Optional["Path"] = None,
    sub_message: Optional[str] = None,
    original_error: Optional[Exception] = None,
) -> "CoercionError":
    """
    Returns a CoercionError whose message is formatted according to the
    message, path, and sub-message filled in.
    :param message: the message of the error
    :param node: the AST node linked to the error
    :param path: the path where the error occurred
    :param sub_message: the sub-message to append
    :param original_error: the original raw exception
    :type message: str
    :type node: Optional[Node]
    :type path: Optional[Path]
    :type sub_message: Optional[str]
    :type original_error: Optional[Exception]
    :return: a CoercionError
    :rtype: CoercionError
    """
    return CoercionError(
        message
        + (" at " + str(path) if path else "")
        + ("; " + sub_message if sub_message else "."),
        locations=[node.location] if node else None,
        original_error=original_error,
    )
