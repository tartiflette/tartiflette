import pytest

from tartiflette.language.ast import DocumentNode


def test_documentnode__init__():
    document_node = DocumentNode(
        definitions="documentDefinitions", location="documentLocation"
    )
    assert document_node.definitions == "documentDefinitions"
    assert document_node.location == "documentLocation"


@pytest.mark.parametrize(
    "document_node,other,expected",
    [
        (
            DocumentNode(
                definitions="documentDefinitions", location="documentLocation"
            ),
            Ellipsis,
            False,
        ),
        (
            DocumentNode(
                definitions="documentDefinitions", location="documentLocation"
            ),
            DocumentNode(
                definitions="documentDefinitionsBis",
                location="documentLocation",
            ),
            False,
        ),
        (
            DocumentNode(
                definitions="documentDefinitions", location="documentLocation"
            ),
            DocumentNode(
                definitions="documentDefinitions",
                location="documentLocationBis",
            ),
            False,
        ),
        (
            DocumentNode(
                definitions="documentDefinitions", location="documentLocation"
            ),
            DocumentNode(
                definitions="documentDefinitions", location="documentLocation"
            ),
            True,
        ),
    ],
)
def test_documentnode__eq__(document_node, other, expected):
    assert (document_node == other) is expected


@pytest.mark.parametrize(
    "document_node,expected",
    [
        (
            DocumentNode(
                definitions="documentDefinitions", location="documentLocation"
            ),
            "DocumentNode(definitions='documentDefinitions', "
            "location='documentLocation')",
        )
    ],
)
def test_documentnode__repr__(document_node, expected):
    assert document_node.__repr__() == expected
