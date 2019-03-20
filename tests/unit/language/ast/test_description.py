import pytest

from tartiflette.language.ast import DescriptionNode


def test_descriptionnode__init__():
    description_node = DescriptionNode(
        value="descriptionValue", location="descriptionLocation"
    )
    assert description_node.value == "descriptionValue"
    assert description_node.location == "descriptionLocation"


@pytest.mark.parametrize(
    "description_node,other,expected",
    [
        (
            DescriptionNode(
                value="descriptionValue", location="descriptionLocation"
            ),
            Ellipsis,
            False,
        ),
        (
            DescriptionNode(
                value="descriptionValue", location="descriptionLocation"
            ),
            DescriptionNode(
                value="descriptionValueBis", location="descriptionLocation"
            ),
            False,
        ),
        (
            DescriptionNode(
                value="descriptionValue", location="descriptionLocation"
            ),
            DescriptionNode(
                value="descriptionValue", location="descriptionLocationBis"
            ),
            False,
        ),
        (
            DescriptionNode(
                value="descriptionValue", location="descriptionLocation"
            ),
            DescriptionNode(
                value="descriptionValue", location="descriptionLocation"
            ),
            True,
        ),
    ],
)
def test_descriptionnode__eq__(description_node, other, expected):
    assert (description_node == other) is expected


@pytest.mark.parametrize(
    "description_node,expected",
    [
        (
            DescriptionNode(
                value="descriptionValue", location="descriptionLocation"
            ),
            "DescriptionNode(value='descriptionValue', "
            "location='descriptionLocation')",
        )
    ],
)
def test_descriptionnode__repr__(description_node, expected):
    assert description_node.__repr__() == expected
