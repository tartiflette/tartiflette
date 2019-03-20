import pytest

from tartiflette.language.ast import Location


def test_location__init__():
    location = Location(
        line="locationLine",
        column="locationColumn",
        line_end="locationLineEnd",
        column_end="locationColumnEnd",
    )
    assert location.line == "locationLine"
    assert location.column == "locationColumn"
    assert location.line_end == "locationLineEnd"
    assert location.column_end == "locationColumnEnd"


@pytest.mark.parametrize(
    "location,other,expected",
    [
        (
            Location(
                line="locationLine",
                column="locationColumn",
                line_end="locationLineEnd",
                column_end="locationColumnEnd",
            ),
            Ellipsis,
            False,
        ),
        (
            Location(
                line="locationLine",
                column="locationColumn",
                line_end="locationLineEnd",
                column_end="locationColumnEnd",
            ),
            Location(
                line="locationLineBis",
                column="locationColumn",
                line_end="locationLineEnd",
                column_end="locationColumnEnd",
            ),
            False,
        ),
        (
            Location(
                line="locationLine",
                column="locationColumn",
                line_end="locationLineEnd",
                column_end="locationColumnEnd",
            ),
            Location(
                line="locationLine",
                column="locationColumnBis",
                line_end="locationLineEnd",
                column_end="locationColumnEnd",
            ),
            False,
        ),
        (
            Location(
                line="locationLine",
                column="locationColumn",
                line_end="locationLineEnd",
                column_end="locationColumnEnd",
            ),
            Location(
                line="locationLine",
                column="locationColumn",
                line_end="locationLineEndBis",
                column_end="locationColumnEnd",
            ),
            False,
        ),
        (
            Location(
                line="locationLine",
                column="locationColumn",
                line_end="locationLineEnd",
                column_end="locationColumnEnd",
            ),
            Location(
                line="locationLine",
                column="locationColumn",
                line_end="locationLineEnd",
                column_end="locationColumnEndBis",
            ),
            False,
        ),
        (
            Location(
                line="locationLine",
                column="locationColumn",
                line_end="locationLineEnd",
                column_end="locationColumnEnd",
            ),
            Location(
                line="locationLine",
                column="locationColumn",
                line_end="locationLineEnd",
                column_end="locationColumnEnd",
            ),
            True,
        ),
    ],
)
def test_location__eq__(location, other, expected):
    assert (location == other) is expected


@pytest.mark.parametrize(
    "location,expected",
    [
        (
            Location(
                line="locationLine",
                column="locationColumn",
                line_end="locationLineEnd",
                column_end="locationColumnEnd",
            ),
            "Location("
            "line='locationLine', "
            "column='locationColumn', "
            "line_end='locationLineEnd', "
            "column_end='locationColumnEnd')",
        )
    ],
)
def test_location__repr__(location, expected):
    assert location.__repr__() == expected
