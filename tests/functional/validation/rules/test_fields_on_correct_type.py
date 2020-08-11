import pytest

from tartiflette import TartifletteError, create_engine
from tartiflette.language.ast import Location
from tartiflette.language.parsers.libgraphqlparser import parse_to_document
from tartiflette.validation.rules import FieldsOnCorrectTypeRule
from tartiflette.validation.validate import validate_query
from tests.functional.utils import assert_unordered_lists


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(name="harness")
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
            fragment objectFieldSelection on Dog {
              __typename
              name
            }
            """,
            [],
        ),
        (
            """
            fragment aliasedObjectFieldSelection on Dog {
              tn : __typename
              otherName : name
            }
            """,
            [],
        ),
        (
            """
            fragment interfaceFieldSelection on Pet {
              __typename
              name
            }
            """,
            [],
        ),
        (
            """
            fragment interfaceFieldSelection on Pet {
              otherName : name
            }
            """,
            [],
        ),
        (
            """
            fragment lyingAliasSelection on Dog {
              name : nickname
            }
            """,
            [],
        ),
        (
            """
            fragment unknownSelection on UnknownType {
              unknownField
            }
            """,
            [],
        ),
        (
            """
            fragment typeKnownAgain on Pet {
              unknown_pet_field {
                ... on Cat {
                  unknown_cat_field
                }
              }
            }
            """,
            [
                TartifletteError(
                    message="Cannot query field < unknown_pet_field > on type < Pet >.",
                    locations=[
                        Location(line=3, column=15, line_end=7, column_end=16)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.3.1",
                        "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                    },
                ),
                TartifletteError(
                    message="Cannot query field < unknown_cat_field > on type < Cat >.",
                    locations=[
                        Location(line=5, column=19, line_end=5, column_end=36)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.3.1",
                        "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                    },
                ),
            ],
        ),
        (
            """
            fragment fieldNotDefined on Dog {
              meowVolume
            }
            """,
            [
                TartifletteError(
                    message="Cannot query field < meowVolume > on type < Dog >.",
                    locations=[
                        Location(line=3, column=15, line_end=3, column_end=25)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.3.1",
                        "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                    },
                )
            ],
        ),
        (
            """
            fragment deepFieldNotDefined on Dog {
              unknown_field {
                deeper_unknown_field
              }
            }
            """,
            [
                TartifletteError(
                    message="Cannot query field < unknown_field > on type < Dog >.",
                    locations=[
                        Location(line=3, column=15, line_end=5, column_end=16)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.3.1",
                        "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                    },
                )
            ],
        ),
        (
            """
            fragment subFieldNotDefined on Human {
              pets {
                unknown_field
              }
            }
            """,
            [
                TartifletteError(
                    message="Cannot query field < unknown_field > on type < Pet >.",
                    locations=[
                        Location(line=4, column=17, line_end=4, column_end=30)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.3.1",
                        "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                    },
                )
            ],
        ),
        (
            """
            fragment fieldNotDefined on Pet {
              ... on Dog {
                meowVolume
              }
            }
            """,
            [
                TartifletteError(
                    message="Cannot query field < meowVolume > on type < Dog >.",
                    locations=[
                        Location(line=4, column=17, line_end=4, column_end=27)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.3.1",
                        "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                    },
                )
            ],
        ),
        (
            """
            fragment aliasedFieldTargetNotDefined on Dog {
              volume : mooVolume
            }
            """,
            [
                TartifletteError(
                    message="Cannot query field < mooVolume > on type < Dog >.",
                    locations=[
                        Location(line=3, column=15, line_end=3, column_end=33)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.3.1",
                        "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                    },
                )
            ],
        ),
        (
            """
            fragment aliasedLyingFieldTargetNotDefined on Dog {
              barkVolume : kawVolume
            }
            """,
            [
                TartifletteError(
                    message="Cannot query field < kawVolume > on type < Dog >.",
                    locations=[
                        Location(line=3, column=15, line_end=3, column_end=37)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.3.1",
                        "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                    },
                )
            ],
        ),
        (
            """
            fragment notDefinedOnInterface on Pet {
              tailLength
            }
            """,
            [
                TartifletteError(
                    message="Cannot query field < tailLength > on type < Pet >.",
                    locations=[
                        Location(line=3, column=15, line_end=3, column_end=25)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.3.1",
                        "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                    },
                )
            ],
        ),
        (
            """
            fragment definedOnImplementorsButNotInterface on Pet {
              nickname
            }
            """,
            [
                TartifletteError(
                    message="Cannot query field < nickname > on type < Pet >.",
                    locations=[
                        Location(line=3, column=15, line_end=3, column_end=23)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.3.1",
                        "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                    },
                )
            ],
        ),
        (
            """
            fragment directFieldSelectionOnUnion on CatOrDog {
              __typename
            }
            """,
            [],
        ),
        (
            """
            fragment directFieldSelectionOnUnion on CatOrDog {
              directField
            }
            """,
            [
                TartifletteError(
                    message="Cannot query field < directField > on type < CatOrDog >.",
                    locations=[
                        Location(line=3, column=15, line_end=3, column_end=26)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.3.1",
                        "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                    },
                )
            ],
        ),
        (
            """
            fragment definedOnImplementorsQueriedOnUnion on CatOrDog {
              name
            }
            """,
            [
                TartifletteError(
                    message="Cannot query field < name > on type < CatOrDog >.",
                    locations=[
                        Location(line=3, column=15, line_end=3, column_end=19)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.3.1",
                        "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                    },
                )
            ],
        ),
        (
            """
            fragment objectFieldSelection on Pet {
              ... on Dog {
                name
              }
              ... {
                name
              }
            }
            """,
            [],
        ),
    ],
)
async def test_fields_on_correct_type(engine, query, expected):
    assert_unordered_lists(
        validate_query(
            engine._schema,
            parse_to_document(query, engine._schema),
            rules=[FieldsOnCorrectTypeRule],
        ),
        expected,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "sdl,query,expected",
    [
        (
            """
            type T {
              fieldWithVeryLongNameThatWillNeverBeSuggested: String
            }
            type Query { t: T }
            """,
            """
            { t { f } }
            """,
            [
                TartifletteError(
                    message="Cannot query field < f > on type < T >.",
                    locations=[
                        Location(line=2, column=19, line_end=2, column_end=20)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.3.1",
                        "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                    },
                )
            ],
        ),
        (
            """
            union T = A | B
            type Query { t: T }

            type A { f: String }
            type B { f: String }
            """,
            """
            { t { f } }
            """,
            [
                TartifletteError(
                    message="Cannot query field < f > on type < T >.",
                    locations=[
                        Location(line=2, column=19, line_end=2, column_end=20)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.3.1",
                        "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                    },
                )
            ],
        ),
        (
            """
            type T {
              y: String
              z: String
            }
            type Query { t: T }
            """,
            """
            { t { f } }
            """,
            [
                TartifletteError(
                    message="Cannot query field < f > on type < T >.",
                    locations=[
                        Location(line=2, column=19, line_end=2, column_end=20)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.3.1",
                        "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                    },
                )
            ],
        ),
        (
            """
            interface T {
              y: String
              z: String
            }
            type Query { t: T }

            type A implements T {
              f: String
              y: String
              z: String
            }
            type B implements T {
              f: String
              y: String
              z: String
            }
            """,
            """
            { t { f } }
            """,
            [
                TartifletteError(
                    message="Cannot query field < f > on type < T >.",
                    locations=[
                        Location(line=2, column=19, line_end=2, column_end=20)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.3.1",
                        "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                    },
                )
            ],
        ),
        (
            """
            interface T { bar: String }
            type Query { t: T }

            interface Z {
              foo: String
            }

            interface Y {
              foo: String
              bar: String
            }

            type X implements Y & Z & T {
              foo: String
              bar: String
            }
            """,
            """
            { t { foo } }
            """,
            [
                TartifletteError(
                    message="Cannot query field < foo > on type < T >.",
                    locations=[
                        Location(line=2, column=19, line_end=2, column_end=22)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.3.1",
                        "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                    },
                )
            ],
        ),
        (
            """
            union T = A | B | C | D | E | F
            type Query { t: T }

            type A { f: String }
            type B { f: String }
            type C { f: String }
            type D { f: String }
            type E { f: String }
            type F { f: String }
            """,
            """
            { t { f } }
            """,
            [
                TartifletteError(
                    message="Cannot query field < f > on type < T >.",
                    locations=[
                        Location(line=2, column=19, line_end=2, column_end=20)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.3.1",
                        "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                    },
                )
            ],
        ),
        (
            """
            type T {
              u: String
              v: String
              w: String
              x: String
              y: String
              z: String
            }
            type Query { t: T }
            """,
            """
            { t { f } }
            """,
            [
                TartifletteError(
                    message="Cannot query field < f > on type < T >.",
                    locations=[
                        Location(line=2, column=19, line_end=2, column_end=20)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.3.1",
                        "tag": "field-selections-on-objects-interfaces-and-unions-types",
                        "details": "https://spec.graphql.org/June2018/#sec-Field-Selections-on-Objects-Interfaces-and-Unions-Types",
                    },
                )
            ],
        ),
    ],
)
async def test_fields_on_correct_type_custom_schema(sdl, query, expected):
    engine = await create_engine(sdl, schema_name=str(hash(sdl)))
    assert_unordered_lists(
        validate_query(
            engine._schema,
            parse_to_document(query, engine._schema),
            rules=[FieldsOnCorrectTypeRule],
        ),
        expected,
    )
