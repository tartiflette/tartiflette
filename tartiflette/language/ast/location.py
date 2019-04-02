from typing import Any, Optional


class Location:
    """
    AST node representing a GraphQL location.
    """

    __slots__ = ("line", "column", "line_end", "column_end")

    def __init__(
        self,
        line: int,
        column: int,
        line_end: Optional[int] = None,
        column_end: Optional[int] = None,
    ) -> None:
        """
        :param line: start line number of the location
        :param column: start column number of the location
        :param line_end: end line number of the location
        :param column_end: end column number of the location
        :type line: int
        :type column: int
        :type line_end: Optional[int]
        :type column_end: Optional[int]
        """
        self.line = line
        self.column = column
        self.line_end = line_end
        self.column_end = column_end

    def __eq__(self, other: Any) -> bool:
        """
        Returns True if `other` instance is identical to `self`.
        :param other: object instance to compare to `self`
        :type other: Any
        :return: whether or not `other` is identical to `self`
        :rtype: bool
        """
        return self is other or (
            isinstance(other, Location)
            and (
                self.line == other.line
                and self.column == other.column
                and self.line_end == other.line_end
                and self.column_end == other.column_end
            )
        )

    def __repr__(self) -> str:
        """
        Returns the representation of a Location instance.
        :return: the representation of a Location instance
        :rtype: str
        """
        return "Location(line=%r, column=%r, line_end=%r, column_end=%r)" % (
            self.line,
            self.column,
            self.line_end,
            self.column_end,
        )
