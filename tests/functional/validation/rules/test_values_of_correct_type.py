import pytest

from tartiflette import (
    UNDEFINED_VALUE,
    Scalar,
    TartifletteError,
    create_engine,
)
from tartiflette.language.ast import Location
from tartiflette.language.parsers.libgraphqlparser import parse_to_document
from tartiflette.validation.rules import ValuesOfCorrectTypeRule
from tartiflette.validation.validate import validate_query
from tests.functional.utils import assert_unordered_lists


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(name="harness")
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
            {
              complicatedArgs {
                intArgField(intArg: 2)
              }
            }
            """,
            [],
        ),
        (
            """
            {
              complicatedArgs {
                intArgField(intArg: -2)
              }
            }
            """,
            [],
        ),
        (
            """
            {
              complicatedArgs {
                booleanArgField(booleanArg: true)
              }
            }
            """,
            [],
        ),
        (
            """
            {
              complicatedArgs {
                stringArgField(stringArg: "foo")
              }
            }
            """,
            [],
        ),
        (
            """
            {
              complicatedArgs {
                floatArgField(floatArg: 1.1)
              }
            }
            """,
            [],
        ),
        (
            """
            {
              complicatedArgs {
                floatArgField(floatArg: -1.1)
              }
            }
            """,
            [],
        ),
        (
            """
            {
              complicatedArgs {
                floatArgField(floatArg: 1)
              }
            }
            """,
            [],
        ),
        (
            """
            {
              complicatedArgs {
                idArgField(idArg: 1)
              }
            }
            """,
            [],
        ),
        (
            """
            {
              complicatedArgs {
                idArgField(idArg: "someIdString")
              }
            }
            """,
            [],
        ),
        (
            """
            {
              dog {
                doesKnowCommand(dogCommand: SIT)
              }
            }
            """,
            [],
        ),
        (
            """
            {
              complicatedArgs {
                enumArgField(enumArg: UNKNOWN)
              }
            }
            """,
            [],
        ),
        (
            """
            {
              complicatedArgs {
                enumArgField(enumArg: NO_FUR)
              }
            }
            """,
            [],
        ),
        (
            """
            {
              complicatedArgs {
                intArgField(intArg: null)
              }
            }
            """,
            [],
        ),
        (
            """
            {
              dog(a: null, b: null, c:{ requiredField: true, intField: null }) {
                name
              }
            }
            """,
            [],
        ),
        (
            """
            {
              complicatedArgs {
                stringArgField(stringArg: 1)
              }
            }
            """,
            [
                TartifletteError(
                    message="String cannot represent a non string value: 1.",
                    locations=[
                        Location(line=4, column=43, line_end=4, column_end=44)
                    ],
                    extensions={},
                )
            ],
        ),
        (
            """
            {
              complicatedArgs {
                stringArgField(stringArg: 1.0)
              }
            }
            """,
            [
                TartifletteError(
                    message="String cannot represent a non string value: 1.0.",
                    locations=[
                        Location(line=4, column=43, line_end=4, column_end=46)
                    ],
                    extensions={},
                )
            ],
        ),
        (
            """
            {
              complicatedArgs {
                stringArgField(stringArg: true)
              }
            }
            """,
            [
                TartifletteError(
                    message="String cannot represent a non string value: true.",
                    locations=[
                        Location(line=4, column=43, line_end=4, column_end=47)
                    ],
                    extensions={},
                )
            ],
        ),
        (
            """
            {
              complicatedArgs {
                stringArgField(stringArg: BAR)
              }
            }
            """,
            [
                TartifletteError(
                    message="String cannot represent a non string value: BAR.",
                    locations=[
                        Location(line=4, column=43, line_end=4, column_end=46)
                    ],
                    extensions={},
                )
            ],
        ),
        (
            """
            {
              complicatedArgs {
                intArgField(intArg: "3")
              }
            }
            """,
            [
                TartifletteError(
                    message='Int cannot represent non-integer value: "3".',
                    locations=[
                        Location(line=4, column=37, line_end=4, column_end=40)
                    ],
                    extensions={},
                )
            ],
        ),
        (
            """
            {
              complicatedArgs {
                intArgField(intArg: 829384293849283498239482938)
              }
            }
            """,
            [
                TartifletteError(
                    message="Int cannot represent non 32-bit signed integer value: 829384293849283498239482938.",
                    locations=[
                        Location(line=4, column=37, line_end=4, column_end=64)
                    ],
                    extensions={},
                )
            ],
        ),
        (
            """
            {
              complicatedArgs {
                intArgField(intArg: FOO)
              }
            }
            """,
            [
                TartifletteError(
                    message="Int cannot represent non-integer value: FOO.",
                    locations=[
                        Location(line=4, column=37, line_end=4, column_end=40)
                    ],
                    extensions={},
                )
            ],
        ),
        (
            """
            {
              complicatedArgs {
                intArgField(intArg: 3.0)
              }
            }
            """,
            [
                TartifletteError(
                    message="Int cannot represent non-integer value: 3.0.",
                    locations=[
                        Location(line=4, column=37, line_end=4, column_end=40)
                    ],
                    extensions={},
                )
            ],
        ),
        (
            """
            {
              complicatedArgs {
                intArgField(intArg: 3.333)
              }
            }
            """,
            [
                TartifletteError(
                    message="Int cannot represent non-integer value: 3.333.",
                    locations=[
                        Location(line=4, column=37, line_end=4, column_end=42)
                    ],
                    extensions={},
                )
            ],
        ),
        (
            """
            {
              complicatedArgs {
                floatArgField(floatArg: "3.333")
              }
            }
            """,
            [
                TartifletteError(
                    message='Float cannot represent non numeric value: "3.333".',
                    locations=[
                        Location(line=4, column=41, line_end=4, column_end=48)
                    ],
                    extensions={},
                )
            ],
        ),
        (
            """
            {
              complicatedArgs {
                floatArgField(floatArg: true)
              }
            }
            """,
            [
                TartifletteError(
                    message="Float cannot represent non numeric value: true.",
                    locations=[
                        Location(line=4, column=41, line_end=4, column_end=45)
                    ],
                    extensions={},
                )
            ],
        ),
        (
            """
            {
              complicatedArgs {
                floatArgField(floatArg: FOO)
              }
            }
            """,
            [
                TartifletteError(
                    message="Float cannot represent non numeric value: FOO.",
                    locations=[
                        Location(line=4, column=41, line_end=4, column_end=44)
                    ],
                    extensions={},
                )
            ],
        ),
        (
            """
            {
              complicatedArgs {
                booleanArgField(booleanArg: 2)
              }
            }
            """,
            [
                TartifletteError(
                    message="Boolean cannot represent a non boolean value: 2.",
                    locations=[
                        Location(line=4, column=45, line_end=4, column_end=46)
                    ],
                    extensions={},
                )
            ],
        ),
        (
            """
            {
              complicatedArgs {
                booleanArgField(booleanArg: 1.0)
              }
            }
            """,
            [
                TartifletteError(
                    message="Boolean cannot represent a non boolean value: 1.0.",
                    locations=[
                        Location(line=4, column=45, line_end=4, column_end=48)
                    ],
                    extensions={},
                )
            ],
        ),
        (
            """
            {
              complicatedArgs {
                booleanArgField(booleanArg: "true")
              }
            }
            """,
            [
                TartifletteError(
                    message='Boolean cannot represent a non boolean value: "true".',
                    locations=[
                        Location(line=4, column=45, line_end=4, column_end=51)
                    ],
                    extensions={},
                )
            ],
        ),
        (
            """
            {
              complicatedArgs {
                booleanArgField(booleanArg: TRUE)
              }
            }
            """,
            [
                TartifletteError(
                    message="Boolean cannot represent a non boolean value: TRUE.",
                    locations=[
                        Location(line=4, column=45, line_end=4, column_end=49)
                    ],
                    extensions={},
                )
            ],
        ),
        (
            """
            {
              complicatedArgs {
                idArgField(idArg: 1.0)
              }
            }
            """,
            [
                TartifletteError(
                    message="ID cannot represent a non-string and non-integer value: 1.0.",
                    locations=[
                        Location(line=4, column=35, line_end=4, column_end=38)
                    ],
                    extensions={},
                )
            ],
        ),
        (
            """
            {
              complicatedArgs {
                idArgField(idArg: true)
              }
            }
            """,
            [
                TartifletteError(
                    message="ID cannot represent a non-string and non-integer value: true.",
                    locations=[
                        Location(line=4, column=35, line_end=4, column_end=39)
                    ],
                    extensions={},
                )
            ],
        ),
        (
            """
            {
              complicatedArgs {
                idArgField(idArg: SOMETHING)
              }
            }
            """,
            [
                TartifletteError(
                    message="ID cannot represent a non-string and non-integer value: SOMETHING.",
                    locations=[
                        Location(line=4, column=35, line_end=4, column_end=44)
                    ],
                    extensions={},
                )
            ],
        ),
        (
            """
            {
              dog {
                doesKnowCommand(dogCommand: 2)
              }
            }
            """,
            [
                TartifletteError(
                    message="Enum < DogCommand > cannot represent non-enum value: 2.",
                    locations=[
                        Location(line=4, column=45, line_end=4, column_end=46)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.6.1",
                        "tag": "values-of-correct-type",
                        "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                    },
                )
            ],
        ),
        (
            """
            {
              dog {
                doesKnowCommand(dogCommand: 1.0)
              }
            }
            """,
            [
                TartifletteError(
                    message="Enum < DogCommand > cannot represent non-enum value: 1.0.",
                    locations=[
                        Location(line=4, column=45, line_end=4, column_end=48)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.6.1",
                        "tag": "values-of-correct-type",
                        "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                    },
                )
            ],
        ),
        (
            """
            {
              dog {
                doesKnowCommand(dogCommand: "SIT")
              }
            }
            """,
            [
                TartifletteError(
                    message='Enum < DogCommand > cannot represent non-enum value: "SIT".',
                    locations=[
                        Location(line=4, column=45, line_end=4, column_end=50)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.6.1",
                        "tag": "values-of-correct-type",
                        "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                    },
                )
            ],
        ),
        (
            """
            {
              dog {
                doesKnowCommand(dogCommand: true)
              }
            }
            """,
            [
                TartifletteError(
                    message="Enum < DogCommand > cannot represent non-enum value: true.",
                    locations=[
                        Location(line=4, column=45, line_end=4, column_end=49)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.6.1",
                        "tag": "values-of-correct-type",
                        "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                    },
                )
            ],
        ),
        (
            """
            {
              dog {
                doesKnowCommand(dogCommand: JUGGLE)
              }
            }
            """,
            [
                TartifletteError(
                    message="Value < JUGGLE > does not exist in < DogCommand > enum.",
                    locations=[
                        Location(line=4, column=45, line_end=4, column_end=51)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.6.1",
                        "tag": "values-of-correct-type",
                        "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                    },
                )
            ],
        ),
        (
            """
            {
              dog {
                doesKnowCommand(dogCommand: sit)
              }
            }
            """,
            [
                TartifletteError(
                    message="Value < sit > does not exist in < DogCommand > enum.",
                    locations=[
                        Location(line=4, column=45, line_end=4, column_end=48)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.6.1",
                        "tag": "values-of-correct-type",
                        "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                    },
                )
            ],
        ),
        (
            """
            {
              complicatedArgs {
                stringListArgField(stringListArg: ["one", null, "two"])
              }
            }
            """,
            [],
        ),
        (
            """
            {
              complicatedArgs {
                stringListArgField(stringListArg: [])
              }
            }
            """,
            [],
        ),
        (
            """
            {
              complicatedArgs {
                stringListArgField(stringListArg: null)
              }
            }
            """,
            [],
        ),
        (
            """
            {
              complicatedArgs {
                stringListArgField(stringListArg: "one")
              }
            }
            """,
            [],
        ),
        (
            """
            {
              complicatedArgs {
                stringListArgField(stringListArg: ["one", 2])
              }
            }
            """,
            [
                TartifletteError(
                    message="String cannot represent a non string value: 2.",
                    locations=[
                        Location(line=4, column=59, line_end=4, column_end=60)
                    ],
                    extensions={},
                )
            ],
        ),
        (
            """
            {
              complicatedArgs {
                stringListArgField(stringListArg: 1)
              }
            }
            """,
            [
                TartifletteError(
                    message="String cannot represent a non string value: 1.",
                    locations=[
                        Location(line=4, column=51, line_end=4, column_end=52)
                    ],
                    extensions={},
                )
            ],
        ),
        (
            """
            {
              dog {
                isHouseTrained(atOtherHomes: true)
              }
            }
            """,
            [],
        ),
        (
            """
            {
              dog {
                isHouseTrained
              }
            }
            """,
            [],
        ),
        (
            """
            {
              complicatedArgs {
                multipleReqs(req1: 1, req2: 2)
              }
            }
            """,
            [],
        ),
        (
            """
            {
              complicatedArgs {
                multipleReqs(req2: 2, req1: 1)
              }
            }
            """,
            [],
        ),
        (
            """
            {
              complicatedArgs {
                multipleOpts
              }
            }
            """,
            [],
        ),
        (
            """
            {
              complicatedArgs {
                multipleOpts(opt1: 1)
              }
            }
            """,
            [],
        ),
        (
            """
            {
              complicatedArgs {
                multipleOpts(opt2: 1)
              }
            }
            """,
            [],
        ),
        (
            """
            {
              complicatedArgs {
                multipleOptAndReq(req1: 3, req2: 4)
              }
            }
            """,
            [],
        ),
        (
            """
            {
              complicatedArgs {
                multipleOptAndReq(req1: 3, req2: 4, opt1: 5)
              }
            }
            """,
            [],
        ),
        (
            """
            {
              complicatedArgs {
                multipleOptAndReq(req1: 3, req2: 4, opt1: 5, opt2: 6)
              }
            }
            """,
            [],
        ),
        (
            """
            {
              complicatedArgs {
                multipleReqs(req2: "two", req1: "one")
              }
            }
            """,
            [
                TartifletteError(
                    message='Int cannot represent non-integer value: "two".',
                    locations=[
                        Location(line=4, column=36, line_end=4, column_end=41)
                    ],
                    extensions={},
                ),
                TartifletteError(
                    message='Int cannot represent non-integer value: "one".',
                    locations=[
                        Location(line=4, column=49, line_end=4, column_end=54)
                    ],
                    extensions={},
                ),
            ],
        ),
        (
            """
            {
              complicatedArgs {
                multipleReqs(req1: "one")
              }
            }
            """,
            [
                TartifletteError(
                    message='Int cannot represent non-integer value: "one".',
                    locations=[
                        Location(line=4, column=36, line_end=4, column_end=41)
                    ],
                    extensions={},
                )
            ],
        ),
        (
            """
            {
              complicatedArgs {
                multipleReqs(req1: null)
              }
            }
            """,
            [
                TartifletteError(
                    message="Expected value of type < Int! >, found < null >.",
                    locations=[
                        Location(line=4, column=36, line_end=4, column_end=40)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.6.1",
                        "tag": "values-of-correct-type",
                        "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                    },
                )
            ],
        ),
        (
            """
            {
              complicatedArgs {
                complexArgField
              }
            }
            """,
            [],
        ),
        (
            """
            {
              complicatedArgs {
                complexArgField(complexArg: { requiredField: true })
              }
            }
            """,
            [],
        ),
        (
            """
            {
              complicatedArgs {
                complexArgField(complexArg: { requiredField: false })
              }
            }
            """,
            [],
        ),
        (
            """
            {
              complicatedArgs {
                complexArgField(complexArg: { requiredField: true, intField: 4 })
              }
            }
            """,
            [],
        ),
        (
            """
            {
              complicatedArgs {
                complexArgField(complexArg: {
                  requiredField: true,
                  intField: 4,
                  stringField: "foo",
                  booleanField: false,
                  stringListField: ["one", "two"]
                })
              }
            }
            """,
            [],
        ),
        (
            """
            {
              complicatedArgs {
                complexArgField(complexArg: {
                  stringListField: ["one", "two"],
                  booleanField: false,
                  requiredField: true,
                  stringField: "foo",
                  intField: 4,
                })
              }
            }
            """,
            [],
        ),
        (
            """
            {
              complicatedArgs {
                complexArgField(complexArg: { intField: 4 })
              }
            }
            """,
            [
                TartifletteError(
                    message="Field < ComplexInput.requiredField > of required type < Boolean! > was not provided.",
                    locations=[
                        Location(line=4, column=45, line_end=4, column_end=60)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.6.1",
                        "tag": "values-of-correct-type",
                        "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                    },
                )
            ],
        ),
        (
            """
            {
              complicatedArgs {
                complexArgField(complexArg: {
                  stringListField: ["one", 2],
                  requiredField: true,
                })
              }
            }
            """,
            [
                TartifletteError(
                    message="String cannot represent a non string value: 2.",
                    locations=[
                        Location(line=5, column=44, line_end=5, column_end=45)
                    ],
                    extensions={},
                )
            ],
        ),
        (
            """
            {
              complicatedArgs {
                complexArgField(complexArg: {
                  requiredField: true,
                  nonNullField: null,
                })
              }
            }
            """,
            [
                TartifletteError(
                    message="Expected value of type < Boolean! >, found < null >.",
                    locations=[
                        Location(line=6, column=33, line_end=6, column_end=37)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.6.1",
                        "tag": "values-of-correct-type",
                        "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                    },
                )
            ],
        ),
        (
            """
            {
              complicatedArgs {
                complexArgField(complexArg: {
                  requiredField: true,
                  invalidField: "value"
                })
              }
            }
            """,
            [
                TartifletteError(
                    message="Field < invalidField > is not defined by type < $ComplexInput >. Did you mean intField or stringField?",
                    locations=[
                        Location(line=6, column=19, line_end=6, column_end=40)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.6.1",
                        "tag": "values-of-correct-type",
                        "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                    },
                )
            ],
        ),
        (
            """
            {
              dog @include(if: true) {
                name
              }
              human @skip(if: false) {
                name
              }
            }
            """,
            [],
        ),
        (
            """
            {
              dog @include(if: "yes") {
                name @skip(if: ENUM)
              }
            }
            """,
            [
                TartifletteError(
                    message='Boolean cannot represent a non boolean value: "yes".',
                    locations=[
                        Location(line=3, column=32, line_end=3, column_end=37)
                    ],
                    extensions={},
                ),
                TartifletteError(
                    message="Boolean cannot represent a non boolean value: ENUM.",
                    locations=[
                        Location(line=4, column=32, line_end=4, column_end=36)
                    ],
                    extensions={},
                ),
            ],
        ),
        (
            """
            query WithDefaultValues(
              $a: Int = 1,
              $b: String = "ok",
              $c: ComplexInput = { requiredField: true, intField: 3 }
              $d: Int! = 123
            ) {
              dog { name }
            }
            """,
            [],
        ),
        (
            """
            query WithDefaultValues(
              $a: Int = null,
              $b: String = null,
              $c: ComplexInput = { requiredField: true, intField: null }
            ) {
              dog { name }
            }
            """,
            [],
        ),
        (
            """
            query WithDefaultValues(
              $a: Int! = null,
              $b: String! = null,
              $c: ComplexInput = { requiredField: null, intField: null }
            ) {
              dog { name }
            }
            """,
            [
                TartifletteError(
                    message="Expected value of type < Int! >, found < null >.",
                    locations=[
                        Location(line=3, column=26, line_end=3, column_end=30)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.6.1",
                        "tag": "values-of-correct-type",
                        "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                    },
                ),
                TartifletteError(
                    message="Expected value of type < String! >, found < null >.",
                    locations=[
                        Location(line=4, column=29, line_end=4, column_end=33)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.6.1",
                        "tag": "values-of-correct-type",
                        "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                    },
                ),
                TartifletteError(
                    message="Expected value of type < Boolean! >, found < null >.",
                    locations=[
                        Location(line=5, column=51, line_end=5, column_end=55)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.6.1",
                        "tag": "values-of-correct-type",
                        "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                    },
                ),
            ],
        ),
        (
            """
            query InvalidDefaultValues(
              $a: Int = "one",
              $b: String = 4,
              $c: ComplexInput = "NotVeryComplex"
            ) {
              dog { name }
            }
            """,
            [
                TartifletteError(
                    message='Int cannot represent non-integer value: "one".',
                    locations=[
                        Location(line=3, column=25, line_end=3, column_end=30)
                    ],
                    extensions={},
                ),
                TartifletteError(
                    message="String cannot represent a non string value: 4.",
                    locations=[
                        Location(line=4, column=28, line_end=4, column_end=29)
                    ],
                    extensions={},
                ),
                TartifletteError(
                    message='Expected value of type < ComplexInput >, found < "NotVeryComplex" >.',
                    locations=[
                        Location(line=5, column=34, line_end=5, column_end=50)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.6.1",
                        "tag": "values-of-correct-type",
                        "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                    },
                ),
            ],
        ),
        (
            """
            query WithDefaultValues(
              $a: ComplexInput = { requiredField: 123, intField: "abc" }
            ) {
              dog { name }
            }
            """,
            [
                TartifletteError(
                    message="Boolean cannot represent a non boolean value: 123.",
                    locations=[
                        Location(line=3, column=51, line_end=3, column_end=54)
                    ],
                    extensions={},
                ),
                TartifletteError(
                    message='Int cannot represent non-integer value: "abc".',
                    locations=[
                        Location(line=3, column=66, line_end=3, column_end=71)
                    ],
                    extensions={},
                ),
            ],
        ),
        (
            """
            query MissingRequiredField($a: ComplexInput = {intField: 3}) {
              dog { name }
            }
            """,
            [
                TartifletteError(
                    message="Field < ComplexInput.requiredField > of required type < Boolean! > was not provided.",
                    locations=[
                        Location(line=2, column=59, line_end=2, column_end=72)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.6.1",
                        "tag": "values-of-correct-type",
                        "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                    },
                )
            ],
        ),
        (
            """
            query InvalidItem($a: [String] = ["one", 2]) {
              dog { name }
            }
            """,
            [
                TartifletteError(
                    message="String cannot represent a non string value: 2.",
                    locations=[
                        Location(line=2, column=54, line_end=2, column_end=55)
                    ],
                    extensions={},
                )
            ],
        ),
    ],
)
async def test_values_of_correct_type(engine, query, expected):
    assert_unordered_lists(
        validate_query(
            engine._schema,
            parse_to_document(query, engine._schema),
            rules=[ValuesOfCorrectTypeRule],
        ),
        expected,
    )


def always_error_literal_parser(ast):
    raise Exception(f"Invalid scalar is always invalid: < {ast} >.")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "literal_parser,expected",
    [
        (
            always_error_literal_parser,
            [
                TartifletteError(
                    message="Expected value of type < CustomScalar >, found < 123 >; Invalid scalar is always invalid: < 123 >.",
                    locations=[
                        Location(line=1, column=19, line_end=1, column_end=22)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.6.1",
                        "tag": "values-of-correct-type",
                        "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                    },
                )
            ],
        ),
        (
            lambda ast: UNDEFINED_VALUE,
            [
                TartifletteError(
                    message="Expected value of type < CustomScalar >, found < 123 >.",
                    locations=[
                        Location(line=1, column=19, line_end=1, column_end=22)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.6.1",
                        "tag": "values-of-correct-type",
                        "details": "https://spec.graphql.org/June2018/#sec-Values-of-Correct-Type",
                    },
                )
            ],
        ),
    ],
)
async def test_values_of_correct_type_custom_scalar(literal_parser, expected):
    schema_name = str(hash(literal_parser))

    @Scalar("CustomScalar", schema_name=schema_name)
    class CustomScalar:
        @staticmethod
        def coerce_output(val):
            return val

        @staticmethod
        def coerce_input(val):
            return val

        parse_literal = staticmethod(literal_parser)

    engine = await create_engine(
        """
        scalar CustomScalar
        type Query {
          invalidArg(arg: CustomScalar): String
        }
        """,
        schema_name=schema_name,
    )

    result = validate_query(
        engine._schema,
        parse_to_document("{ invalidArg(arg: 123) }", engine._schema),
        rules=[ValuesOfCorrectTypeRule],
    )

    assert len(expected) == len(result)
    for expected_error, result_error in zip(expected, result):
        assert expected_error.message == result_error.message
        assert expected_error.user_message == result_error.user_message
        assert expected_error.more_info == result_error.more_info
        assert expected_error.path == result_error.path
        assert expected_error.locations == result_error.locations
        assert expected_error.extensions == result_error.extensions
