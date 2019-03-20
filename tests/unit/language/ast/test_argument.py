import pytest

from tartiflette.language.ast import ArgumentNode


def test_argumentnode__init__():
    argument_node = ArgumentNode(
        name="argumentName", value="argumentValue", location="argumentLocation"
    )
    assert argument_node.name == "argumentName"
    assert argument_node.value == "argumentValue"
    assert argument_node.location == "argumentLocation"


@pytest.mark.parametrize(
    "argument_node,other,expected",
    [
        (
            ArgumentNode(
                name="argumentName",
                value="argumentValue",
                location="argumentLocation",
            ),
            Ellipsis,
            False,
        ),
        (
            ArgumentNode(
                name="argumentName",
                value="argumentValue",
                location="argumentLocation",
            ),
            ArgumentNode(
                name="argumentNameBis",
                value="argumentValue",
                location="argumentLocation",
            ),
            False,
        ),
        (
            ArgumentNode(
                name="argumentName",
                value="argumentValue",
                location="argumentLocation",
            ),
            ArgumentNode(
                name="argumentName",
                value="argumentValueBis",
                location="argumentLocation",
            ),
            False,
        ),
        (
            ArgumentNode(
                name="argumentName",
                value="argumentValue",
                location="argumentLocation",
            ),
            ArgumentNode(
                name="argumentName",
                value="argumentValue",
                location="argumentLocationBis",
            ),
            False,
        ),
        (
            ArgumentNode(
                name="argumentName",
                value="argumentValue",
                location="argumentLocation",
            ),
            ArgumentNode(
                name="argumentName",
                value="argumentValue",
                location="argumentLocation",
            ),
            True,
        ),
    ],
)
def test_argumentnode__eq__(argument_node, other, expected):
    assert (argument_node == other) is expected


@pytest.mark.parametrize(
    "argument_node,expected",
    [
        (
            ArgumentNode(
                name="argumentName",
                value="argumentValue",
                location="argumentLocation",
            ),
            "ArgumentNode(name='argumentName', value='argumentValue', "
            "location='argumentLocation')",
        )
    ],
)
def test_argumentnode__repr__(argument_node, expected):
    assert argument_node.__repr__() == expected
