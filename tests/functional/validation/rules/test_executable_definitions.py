import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import (
    ArgumentNode,
    DocumentNode,
    EnumTypeDefinitionNode,
    EnumValueDefinitionNode,
    EnumValueNode,
    FieldDefinitionNode,
    FieldNode,
    Location,
    NamedTypeNode,
    NameNode,
    ObjectTypeDefinitionNode,
    OperationDefinitionNode,
    OperationTypeDefinitionNode,
    SchemaDefinitionNode,
    SelectionSetNode,
    StringValueNode,
)
from tartiflette.language.parsers.libgraphqlparser import parse_to_document
from tartiflette.validation.rules import ExecutableDefinitionsRule
from tartiflette.validation.validate import validate_query
from tests.functional.utils import assert_unordered_lists


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(name="harness")
@pytest.mark.parametrize(
    "document_node,expected",
    [
        (
            DocumentNode(
                definitions=[
                    OperationDefinitionNode(
                        operation_type="query",
                        name=None,
                        variable_definitions=[],
                        directives=[],
                        selection_set=SelectionSetNode(
                            selections=[
                                FieldNode(
                                    alias=None,
                                    name=NameNode(
                                        value="hello",
                                        location=Location(
                                            line=3,
                                            column=15,
                                            line_end=3,
                                            column_end=20,
                                        ),
                                    ),
                                    arguments=[
                                        ArgumentNode(
                                            name=NameNode(
                                                value="name",
                                                location=Location(
                                                    line=3,
                                                    column=21,
                                                    line_end=3,
                                                    column_end=25,
                                                ),
                                            ),
                                            value=StringValueNode(
                                                value="John",
                                                location=Location(
                                                    line=3,
                                                    column=27,
                                                    line_end=3,
                                                    column_end=33,
                                                ),
                                            ),
                                            location=Location(
                                                line=3,
                                                column=21,
                                                line_end=3,
                                                column_end=33,
                                            ),
                                        )
                                    ],
                                    directives=[],
                                    selection_set=None,
                                    location=Location(
                                        line=3,
                                        column=15,
                                        line_end=3,
                                        column_end=34,
                                    ),
                                )
                            ],
                            location=Location(
                                line=2, column=19, line_end=4, column_end=14
                            ),
                        ),
                        location=Location(
                            line=2, column=13, line_end=4, column_end=14
                        ),
                    )
                ],
                location=Location(
                    line=2, column=13, line_end=4, column_end=14
                ),
            ),
            [],
        ),
        (
            DocumentNode(
                definitions=[
                    ObjectTypeDefinitionNode(
                        description=None,
                        name=NameNode(
                            value="Foo",
                            location=Location(
                                line=2, column=18, line_end=2, column_end=21
                            ),
                        ),
                        interfaces=[],
                        directives=[],
                        fields=[
                            FieldDefinitionNode(
                                description=None,
                                name=NameNode(
                                    value="foo",
                                    location=Location(
                                        line=3,
                                        column=15,
                                        line_end=3,
                                        column_end=18,
                                    ),
                                ),
                                arguments=[],
                                type=NamedTypeNode(
                                    name=NameNode(
                                        value="String",
                                        location=Location(
                                            line=3,
                                            column=20,
                                            line_end=3,
                                            column_end=26,
                                        ),
                                    ),
                                    location=Location(
                                        line=3,
                                        column=20,
                                        line_end=3,
                                        column_end=26,
                                    ),
                                ),
                                directives=[],
                                location=Location(
                                    line=3,
                                    column=15,
                                    line_end=3,
                                    column_end=26,
                                ),
                            )
                        ],
                        location=Location(
                            line=2, column=13, line_end=4, column_end=14
                        ),
                    )
                ],
                location=Location(
                    line=2, column=13, line_end=4, column_end=14
                ),
            ),
            [
                TartifletteError(
                    message="The < Foo > definition is not executable.",
                    locations=[
                        Location(line=2, column=13, line_end=4, column_end=14)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.1.1",
                        "tag": "executable-definitions",
                        "details": "https://spec.graphql.org/June2018/#sec-Executable-Definitions",
                    },
                )
            ],
        ),
        (
            DocumentNode(
                definitions=[
                    EnumTypeDefinitionNode(
                        description=None,
                        name=NameNode(
                            value="Foo",
                            location=Location(
                                line=2, column=18, line_end=2, column_end=21
                            ),
                        ),
                        directives=[],
                        values=[
                            EnumValueDefinitionNode(
                                description=None,
                                name=EnumValueNode(
                                    value="BAR",
                                    location=Location(
                                        line=3,
                                        column=15,
                                        line_end=3,
                                        column_end=18,
                                    ),
                                ),
                                directives=[],
                                location=Location(
                                    line=3,
                                    column=15,
                                    line_end=3,
                                    column_end=18,
                                ),
                            )
                        ],
                        location=Location(
                            line=2, column=13, line_end=4, column_end=14
                        ),
                    )
                ],
                location=Location(
                    line=2, column=13, line_end=4, column_end=14
                ),
            ),
            [
                TartifletteError(
                    message="The < Foo > definition is not executable.",
                    locations=[
                        Location(line=2, column=13, line_end=4, column_end=14)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.1.1",
                        "tag": "executable-definitions",
                        "details": "https://spec.graphql.org/June2018/#sec-Executable-Definitions",
                    },
                )
            ],
        ),
        (
            DocumentNode(
                definitions=[
                    SchemaDefinitionNode(
                        directives=[],
                        operation_type_definitions=[
                            OperationTypeDefinitionNode(
                                operation_type="query",
                                type=NamedTypeNode(
                                    name=NameNode(
                                        value="Foo",
                                        location=Location(
                                            line=3,
                                            column=22,
                                            line_end=3,
                                            column_end=25,
                                        ),
                                    ),
                                    location=Location(
                                        line=3,
                                        column=22,
                                        line_end=3,
                                        column_end=25,
                                    ),
                                ),
                                location=Location(
                                    line=3,
                                    column=15,
                                    line_end=3,
                                    column_end=25,
                                ),
                            )
                        ],
                        location=Location(
                            line=2, column=13, line_end=4, column_end=14
                        ),
                    )
                ],
                location=Location(
                    line=2, column=13, line_end=4, column_end=14
                ),
            ),
            [
                TartifletteError(
                    message="The < schema > definition is not executable.",
                    locations=[
                        Location(line=2, column=13, line_end=4, column_end=14)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.1.1",
                        "tag": "executable-definitions",
                        "details": "https://spec.graphql.org/June2018/#sec-Executable-Definitions",
                    },
                )
            ],
        ),
    ],
)
async def test_executable_definitions(engine, document_node, expected):
    assert_unordered_lists(
        validate_query(
            engine._schema, document_node, rules=[ExecutableDefinitionsRule],
        ),
        expected,
    )
