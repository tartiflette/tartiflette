import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import Location
from tartiflette.language.parsers.libgraphqlparser import parse_to_document
from tartiflette.validation.rules import VariablesInAllowedPositionRule
from tartiflette.validation.validate import validate_query
from tests.functional.utils import assert_unordered_lists


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="harness")
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
            query Query($booleanArg: Boolean)
            {
              complicatedArgs {
                booleanArgField(booleanArg: $booleanArg)
              }
            }
            """,
            [],
        ),
        (
            """
            fragment booleanArgFrag on ComplicatedArgs {
              booleanArgField(booleanArg: $booleanArg)
            }
            query Query($booleanArg: Boolean)
            {
              complicatedArgs {
                ...booleanArgFrag
              }
            }
            """,
            [],
        ),
        (
            """
            query Query($booleanArg: Boolean)
            {
              complicatedArgs {
                ...booleanArgFrag
              }
            }
            fragment booleanArgFrag on ComplicatedArgs {
              booleanArgField(booleanArg: $booleanArg)
            }
            """,
            [],
        ),
        (
            """
            query Query($nonNullBooleanArg: Boolean!)
            {
              complicatedArgs {
                booleanArgField(booleanArg: $nonNullBooleanArg)
              }
            }
            """,
            [],
        ),
        (
            """
            fragment booleanArgFrag on ComplicatedArgs {
              booleanArgField(booleanArg: $nonNullBooleanArg)
            }

            query Query($nonNullBooleanArg: Boolean!)
            {
              complicatedArgs {
                ...booleanArgFrag
              }
            }
            """,
            [],
        ),
        (
            """
            query Query($stringListVar: [String])
            {
              complicatedArgs {
                stringListArgField(stringListArg: $stringListVar)
              }
            }
            """,
            [],
        ),
        (
            """
            query Query($stringListVar: [String!])
            {
              complicatedArgs {
                stringListArgField(stringListArg: $stringListVar)
              }
            }
            """,
            [],
        ),
        (
            """
            query Query($stringVar: String)
            {
              complicatedArgs {
                stringListArgField(stringListArg: [$stringVar])
              }
            }
            """,
            [],
        ),
        (
            """
            query Query($stringVar: String!)
            {
              complicatedArgs {
                stringListArgField(stringListArg: [$stringVar])
              }
            }
            """,
            [],
        ),
        (
            """
            query Query($complexVar: ComplexInput)
            {
              complicatedArgs {
                complexArgField(complexArg: $complexVar)
              }
            }
            """,
            [],
        ),
        (
            """
            query Query($boolVar: Boolean = false)
            {
              complicatedArgs {
                complexArgField(complexArg: {requiredArg: $boolVar})
              }
            }
            """,
            [],
        ),
        (
            """
            query Query($boolVar: Boolean!)
            {
              dog @include(if: $boolVar)
            }
            """,
            [],
        ),
        (
            """
            query Query($intArg: Int) {
              complicatedArgs {
                nonNullIntArgField(nonNullIntArg: $intArg)
              }
            }
            """,
            [
                TartifletteError(
                    message="Variable < $intArg > of type < Int > used in position expecting type < Int! >.",
                    locations=[
                        Location(line=2, column=25, line_end=2, column_end=37),
                        Location(line=4, column=51, line_end=4, column_end=58),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.8.5",
                        "tag": "all-variable-usages-are-allowed",
                        "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                    },
                )
            ],
        ),
        (
            """
            fragment nonNullIntArgFieldFrag on ComplicatedArgs {
              nonNullIntArgField(nonNullIntArg: $intArg)
            }

            query Query($intArg: Int) {
              complicatedArgs {
                ...nonNullIntArgFieldFrag
              }
            }
            """,
            [
                TartifletteError(
                    message="Variable < $intArg > of type < Int > used in position expecting type < Int! >.",
                    locations=[
                        Location(line=6, column=25, line_end=6, column_end=37),
                        Location(line=3, column=49, line_end=3, column_end=56),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.8.5",
                        "tag": "all-variable-usages-are-allowed",
                        "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                    },
                )
            ],
        ),
        (
            """
            fragment outerFrag on ComplicatedArgs {
              ...nonNullIntArgFieldFrag
            }

            fragment nonNullIntArgFieldFrag on ComplicatedArgs {
              nonNullIntArgField(nonNullIntArg: $intArg)
            }

            query Query($intArg: Int) {
              complicatedArgs {
                ...outerFrag
              }
            }
            """,
            [
                TartifletteError(
                    message="Variable < $intArg > of type < Int > used in position expecting type < Int! >.",
                    locations=[
                        Location(
                            line=10, column=25, line_end=10, column_end=37
                        ),
                        Location(line=7, column=49, line_end=7, column_end=56),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.8.5",
                        "tag": "all-variable-usages-are-allowed",
                        "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                    },
                )
            ],
        ),
        (
            """
            query Query($stringVar: String) {
              complicatedArgs {
                booleanArgField(booleanArg: $stringVar)
              }
            }
            """,
            [
                TartifletteError(
                    message="Variable < $stringVar > of type < String > used in position expecting type < Boolean >.",
                    locations=[
                        Location(line=2, column=25, line_end=2, column_end=43),
                        Location(line=4, column=45, line_end=4, column_end=55),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.8.5",
                        "tag": "all-variable-usages-are-allowed",
                        "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                    },
                )
            ],
        ),
        (
            """
            query Query($stringVar: String) {
              complicatedArgs {
                stringListArgField(stringListArg: $stringVar)
              }
            }
            """,
            [
                TartifletteError(
                    message="Variable < $stringVar > of type < String > used in position expecting type < [String] >.",
                    locations=[
                        Location(line=2, column=25, line_end=2, column_end=43),
                        Location(line=4, column=51, line_end=4, column_end=61),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.8.5",
                        "tag": "all-variable-usages-are-allowed",
                        "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                    },
                )
            ],
        ),
        (
            """
            query Query($boolVar: Boolean) {
              dog @include(if: $boolVar)
            }
            """,
            [
                TartifletteError(
                    message="Variable < $boolVar > of type < Boolean > used in position expecting type < Boolean! >.",
                    locations=[
                        Location(line=2, column=25, line_end=2, column_end=42),
                        Location(line=3, column=32, line_end=3, column_end=40),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.8.5",
                        "tag": "all-variable-usages-are-allowed",
                        "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                    },
                )
            ],
        ),
        (
            """
            query Query($stringVar: String) {
              dog @include(if: $stringVar)
            }
            """,
            [
                TartifletteError(
                    message="Variable < $stringVar > of type < String > used in position expecting type < Boolean! >.",
                    locations=[
                        Location(line=2, column=25, line_end=2, column_end=43),
                        Location(line=3, column=32, line_end=3, column_end=42),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.8.5",
                        "tag": "all-variable-usages-are-allowed",
                        "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                    },
                )
            ],
        ),
        (
            """
            query Query($stringListVar: [String])
            {
              complicatedArgs {
                stringListNonNullArgField(stringListNonNullArg: $stringListVar)
              }
            }
            """,
            [
                TartifletteError(
                    message="Variable < $stringListVar > of type < [String] > used in position expecting type < [String!] >.",
                    locations=[
                        Location(line=2, column=25, line_end=2, column_end=49),
                        Location(line=5, column=65, line_end=5, column_end=79),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.8.5",
                        "tag": "all-variable-usages-are-allowed",
                        "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                    },
                )
            ],
        ),
        (
            """
            query Query($intVar: Int = null) {
              complicatedArgs {
                nonNullIntArgField(nonNullIntArg: $intVar)
              }
            }
            """,
            [
                TartifletteError(
                    message="Variable < $intVar > of type < Int > used in position expecting type < Int! >.",
                    locations=[
                        Location(line=2, column=25, line_end=2, column_end=44),
                        Location(line=4, column=51, line_end=4, column_end=58),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.8.5",
                        "tag": "all-variable-usages-are-allowed",
                        "details": "https://spec.graphql.org/June2018/#sec-All-Variable-Usages-are-Allowed",
                    },
                )
            ],
        ),
        (
            """
            query Query($intVar: Int = 1) {
              complicatedArgs {
                nonNullIntArgField(nonNullIntArg: $intVar)
              }
            }
            """,
            [],
        ),
        (
            """
            query Query($intVar: Int) {
              complicatedArgs {
                nonNullFieldWithDefault(nonNullIntArg: $intVar)
              }
            }
            """,
            [],
        ),
        (
            """
            query Query($boolVar: Boolean = false) {
              dog @include(if: $boolVar)
            }
            """,
            [],
        ),
    ],
)
async def test_variables_in_allowed_position(schema_stack, query, expected):
    assert_unordered_lists(
        validate_query(
            schema_stack.schema,
            parse_to_document(query),
            rules=[VariablesInAllowedPositionRule],
        ),
        expected,
    )
