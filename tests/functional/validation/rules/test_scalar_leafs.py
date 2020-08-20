import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import Location
from tartiflette.language.parsers.libgraphqlparser import parse_to_document
from tartiflette.validation.rules import ScalarLeafsRule
from tartiflette.validation.validate import validate_query
from tests.functional.utils import assert_unordered_lists


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="harness")
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
            fragment scalarSelection on Dog {
              barks
            }
            """,
            [],
        ),
        (
            """
            query directQueryOnObjectWithoutSubFields {
              human
            }
            """,
            [
                TartifletteError(
                    message="Field < human > of type < Human > must have a selection of subfields. Did you mean < human { ... } >?",
                    locations=[
                        Location(line=3, column=15, line_end=3, column_end=20)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.3.3",
                        "tag": "leaf-field-selections",
                        "details": "https://spec.graphql.org/June2018/#sec-Leaf-Field-Selections",
                    },
                )
            ],
        ),
        (
            """
            {
              human { pets }
            }
            """,
            [
                TartifletteError(
                    message="Field < pets > of type < [Pet] > must have a selection of subfields. Did you mean < pets { ... } >?",
                    locations=[
                        Location(line=3, column=23, line_end=3, column_end=27)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.3.3",
                        "tag": "leaf-field-selections",
                        "details": "https://spec.graphql.org/June2018/#sec-Leaf-Field-Selections",
                    },
                )
            ],
        ),
        (
            """
            fragment scalarSelectionWithArgs on Dog {
              doesKnowCommand(dogCommand: SIT)
            }
            """,
            [],
        ),
        (
            """
            fragment scalarSelectionsNotAllowedOnBoolean on Dog {
              barks { sinceWhen }
            }
            """,
            [
                TartifletteError(
                    message="Field < barks > must not have a selection since type < Boolean > has no subfields.",
                    locations=[
                        Location(line=3, column=21, line_end=3, column_end=34)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.3.3",
                        "tag": "leaf-field-selections",
                        "details": "https://spec.graphql.org/June2018/#sec-Leaf-Field-Selections",
                    },
                )
            ],
        ),
        (
            """
            fragment scalarSelectionsNotAllowedOnEnum on Cat {
              furColor { inHexDec }
            }
            """,
            [
                TartifletteError(
                    message="Field < furColor > must not have a selection since type < FurColor > has no subfields.",
                    locations=[
                        Location(line=3, column=24, line_end=3, column_end=36)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.3.3",
                        "tag": "leaf-field-selections",
                        "details": "https://spec.graphql.org/June2018/#sec-Leaf-Field-Selections",
                    },
                )
            ],
        ),
        (
            """
            fragment scalarSelectionsNotAllowedWithArgs on Dog {
              doesKnowCommand(dogCommand: SIT) { sinceWhen }
            }
            """,
            [
                TartifletteError(
                    message="Field < doesKnowCommand > must not have a selection since type < Boolean > has no subfields.",
                    locations=[
                        Location(line=3, column=48, line_end=3, column_end=61)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.3.3",
                        "tag": "leaf-field-selections",
                        "details": "https://spec.graphql.org/June2018/#sec-Leaf-Field-Selections",
                    },
                )
            ],
        ),
        (
            """
            fragment scalarSelectionsNotAllowedWithDirectives on Dog {
              name @include(if: true) { isAlsoHumanName }
            }
            """,
            [
                TartifletteError(
                    message="Field < name > must not have a selection since type < String > has no subfields.",
                    locations=[
                        Location(line=3, column=39, line_end=3, column_end=58)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.3.3",
                        "tag": "leaf-field-selections",
                        "details": "https://spec.graphql.org/June2018/#sec-Leaf-Field-Selections",
                    },
                )
            ],
        ),
        (
            """
            fragment scalarSelectionsNotAllowedWithDirectivesAndArgs on Dog {
              doesKnowCommand(dogCommand: SIT) @include(if: true) { sinceWhen }
            }
            """,
            [
                TartifletteError(
                    message="Field < doesKnowCommand > must not have a selection since type < Boolean > has no subfields.",
                    locations=[
                        Location(line=3, column=67, line_end=3, column_end=80)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.3.3",
                        "tag": "leaf-field-selections",
                        "details": "https://spec.graphql.org/June2018/#sec-Leaf-Field-Selections",
                    },
                )
            ],
        ),
    ],
)
async def test_scalar_leafs(schema_stack, query, expected):
    assert_unordered_lists(
        validate_query(
            schema_stack.schema,
            parse_to_document(query),
            rules=[ScalarLeafsRule],
        ),
        expected,
    )
