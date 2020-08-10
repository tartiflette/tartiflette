import pytest

from tartiflette import TartifletteError, create_engine
from tartiflette.language.ast import Location
from tartiflette.language.parsers.libgraphqlparser import parse_to_document
from tartiflette.validation.rules import OverlappingFieldsCanBeMergedRule
from tartiflette.validation.validate import validate_query
from tests.functional.utils import assert_unordered_lists


@pytest.fixture(scope="module")
async def ttftt_engine():
    return await create_engine(
        """
        interface SomeBox {
          deepBox: SomeBox
          unrelatedField: String
        }
        
        type StringBox implements SomeBox {
          scalar: String
          deepBox: StringBox
          unrelatedField: String
          listStringBox: [StringBox]
          stringBox: StringBox
          intBox: IntBox
        }
        
        type IntBox implements SomeBox {
          scalar: Int
          deepBox: IntBox
          unrelatedField: String
          listStringBox: [StringBox]
          stringBox: StringBox
          intBox: IntBox
        }
        
        interface NonNullStringBox1 {
          scalar: String!
        }
        
        type NonNullStringBox1Impl implements SomeBox & NonNullStringBox1 {
          scalar: String!
          unrelatedField: String
          deepBox: SomeBox
        }
        
        interface NonNullStringBox2 {
          scalar: String!
        }
        
        type NonNullStringBox2Impl implements SomeBox & NonNullStringBox2 {
          scalar: String!
          unrelatedField: String
          deepBox: SomeBox
        }
        
        type Connection {
          edges: [Edge]
        }
        
        type Edge {
          node: Node
        }
        
        type Node {
          id: ID
          name: String
        }
        
        type Query {
          someBox: SomeBox
          connection: Connection
        }
        """,
        schema_name="test_overlapping_fields_can_be_merged_box",
    )


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(name="harness")
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
            fragment uniqueFields on Dog {
              name
              nickname
            }
            """,
            [],
        ),
        (
            """
            fragment mergeIdenticalFields on Dog {
              name
              name
            }
            """,
            [],
        ),
        (
            """
            fragment mergeIdenticalFieldsWithIdenticalArgs on Dog {
              doesKnowCommand(dogCommand: SIT)
              doesKnowCommand(dogCommand: SIT)
            }
            """,
            [],
        ),
        (
            """
            fragment mergeSameFieldsWithSameDirectives on Dog {
              name @include(if: true)
              name @include(if: true)
            }
            """,
            [],
        ),
        (
            """
            fragment differentArgsWithDifferentAliases on Dog {
              knowsSit: doesKnowCommand(dogCommand: SIT)
              knowsDown: doesKnowCommand(dogCommand: DOWN)
            }
            """,
            [],
        ),
        (
            """
            fragment differentDirectivesWithDifferentAliases on Dog {
              nameIfTrue: name @include(if: true)
              nameIfFalse: name @include(if: false)
            }
            """,
            [],
        ),
        (
            """
            fragment differentDirectivesWithDifferentAliases on Dog {
              name @include(if: true)
              name @include(if: false)
            }
            """,
            [],
        ),
        (
            """
            fragment sameAliasesWithDifferentFieldTargets on Dog {
              fido: name
              fido: nickname
            }
            """,
            [
                TartifletteError(
                    message="Fields < fido > conflict because < name > and < nickname > are different fields. Use different aliases on the fields to fetch both if this was intentional.",
                    locations=[
                        Location(line=3, column=15, line_end=3, column_end=25),
                        Location(line=4, column=15, line_end=4, column_end=29),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.3.2",
                        "tag": "field-selection-merging",
                        "details": "http://spec.graphql.org/June2018/#sec-Field-Selection-Merging",
                    },
                )
            ],
        ),
        (
            """
            fragment sameAliasesWithDifferentFieldTargets on Pet {
              ... on Dog {
                name
              }
              ... on Cat {
                name: nickname
              }
            }
            """,
            [],
        ),
        (
            """
            fragment aliasMaskingDirectFieldAccess on Dog {
              name: nickname
              name
            }
            """,
            [
                TartifletteError(
                    message="Fields < name > conflict because < nickname > and < name > are different fields. Use different aliases on the fields to fetch both if this was intentional.",
                    locations=[
                        Location(line=3, column=15, line_end=3, column_end=29),
                        Location(line=4, column=15, line_end=4, column_end=19),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.3.2",
                        "tag": "field-selection-merging",
                        "details": "http://spec.graphql.org/June2018/#sec-Field-Selection-Merging",
                    },
                )
            ],
        ),
        (
            """
            fragment conflictingArgs on Dog {
              doesKnowCommand
              doesKnowCommand(dogCommand: HEEL)
            }
            """,
            [
                TartifletteError(
                    message="Fields < doesKnowCommand > conflict because they have differing arguments. Use different aliases on the fields to fetch both if this was intentional.",
                    locations=[
                        Location(line=3, column=15, line_end=3, column_end=30),
                        Location(line=4, column=15, line_end=4, column_end=48),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.3.2",
                        "tag": "field-selection-merging",
                        "details": "http://spec.graphql.org/June2018/#sec-Field-Selection-Merging",
                    },
                )
            ],
        ),
        (
            """
            fragment conflictingArgs on Dog {
              doesKnowCommand(dogCommand: SIT)
              doesKnowCommand
            }
            """,
            [
                TartifletteError(
                    message="Fields < doesKnowCommand > conflict because they have differing arguments. Use different aliases on the fields to fetch both if this was intentional.",
                    locations=[
                        Location(line=3, column=15, line_end=3, column_end=47),
                        Location(line=4, column=15, line_end=4, column_end=30),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.3.2",
                        "tag": "field-selection-merging",
                        "details": "http://spec.graphql.org/June2018/#sec-Field-Selection-Merging",
                    },
                )
            ],
        ),
        (
            """
            fragment conflictingArgs on Dog {
              doesKnowCommand(dogCommand: SIT)
              doesKnowCommand(dogCommand: HEEL)
            }
            """,
            [
                TartifletteError(
                    message="Fields < doesKnowCommand > conflict because they have differing arguments. Use different aliases on the fields to fetch both if this was intentional.",
                    locations=[
                        Location(line=3, column=15, line_end=3, column_end=47),
                        Location(line=4, column=15, line_end=4, column_end=48),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.3.2",
                        "tag": "field-selection-merging",
                        "details": "http://spec.graphql.org/June2018/#sec-Field-Selection-Merging",
                    },
                )
            ],
        ),
        (
            """
            fragment conflictingArgs on Dog {
              isAtLocation(x: 0)
              isAtLocation(y: 0)
            }
            """,
            [
                TartifletteError(
                    message="Fields < isAtLocation > conflict because they have differing arguments. Use different aliases on the fields to fetch both if this was intentional.",
                    locations=[
                        Location(line=3, column=15, line_end=3, column_end=33),
                        Location(line=4, column=15, line_end=4, column_end=33),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.3.2",
                        "tag": "field-selection-merging",
                        "details": "http://spec.graphql.org/June2018/#sec-Field-Selection-Merging",
                    },
                )
            ],
        ),
        (
            """
            fragment conflictingArgs on Pet {
              ... on Dog {
                name(surname: true)
              }
              ... on Cat {
                name
              }
            }
            """,
            [],
        ),
        (
            """
            {
              ...A
              ...B
            }
            fragment A on Type {
              x: a
            }
            fragment B on Type {
              x: b
            }
            """,
            [
                TartifletteError(
                    message="Fields < x > conflict because < a > and < b > are different fields. Use different aliases on the fields to fetch both if this was intentional.",
                    locations=[
                        Location(line=7, column=15, line_end=7, column_end=19),
                        Location(
                            line=10, column=15, line_end=10, column_end=19
                        ),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.3.2",
                        "tag": "field-selection-merging",
                        "details": "http://spec.graphql.org/June2018/#sec-Field-Selection-Merging",
                    },
                )
            ],
        ),
        (
            """
            {
              f1 {
                ...A
                ...B
              }
              f2 {
                ...B
                ...A
              }
              f3 {
                ...A
                ...B
                x: c
              }
            }
            fragment A on Type {
              x: a
            }
            fragment B on Type {
              x: b
            }
            """,
            [
                TartifletteError(
                    message="Fields < x > conflict because < a > and < b > are different fields. Use different aliases on the fields to fetch both if this was intentional.",
                    locations=[
                        Location(
                            line=18, column=15, line_end=18, column_end=19
                        ),
                        Location(
                            line=21, column=15, line_end=21, column_end=19
                        ),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.3.2",
                        "tag": "field-selection-merging",
                        "details": "http://spec.graphql.org/June2018/#sec-Field-Selection-Merging",
                    },
                ),
                TartifletteError(
                    message="Fields < x > conflict because < c > and < a > are different fields. Use different aliases on the fields to fetch both if this was intentional.",
                    locations=[
                        Location(
                            line=14, column=17, line_end=14, column_end=21
                        ),
                        Location(
                            line=18, column=15, line_end=18, column_end=19
                        ),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.3.2",
                        "tag": "field-selection-merging",
                        "details": "http://spec.graphql.org/June2018/#sec-Field-Selection-Merging",
                    },
                ),
                TartifletteError(
                    message="Fields < x > conflict because < c > and < b > are different fields. Use different aliases on the fields to fetch both if this was intentional.",
                    locations=[
                        Location(
                            line=14, column=17, line_end=14, column_end=21
                        ),
                        Location(
                            line=21, column=15, line_end=21, column_end=19
                        ),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.3.2",
                        "tag": "field-selection-merging",
                        "details": "http://spec.graphql.org/June2018/#sec-Field-Selection-Merging",
                    },
                ),
            ],
        ),
        (
            """
            {
              field {
                x: a
              },
              field {
                x: b
              }
            }
            """,
            [
                TartifletteError(
                    message="Fields < field > conflict because subfields < x > conflict because < a > and < b > are different fields. Use different aliases on the fields to fetch both if this was intentional.",
                    locations=[
                        Location(line=3, column=15, line_end=5, column_end=16),
                        Location(line=4, column=17, line_end=4, column_end=21),
                        Location(line=6, column=15, line_end=8, column_end=16),
                        Location(line=7, column=17, line_end=7, column_end=21),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.3.2",
                        "tag": "field-selection-merging",
                        "details": "http://spec.graphql.org/June2018/#sec-Field-Selection-Merging",
                    },
                )
            ],
        ),
        (
            """
            {
              field {
                x: a
                y: c
              },
              field {
                x: b
                y: d
              }
            }
            """,
            [
                TartifletteError(
                    message="Fields < field > conflict because subfields < x > conflict because < a > and < b > are different fields and subfields < y > conflict because < c > and < d > are different fields. Use different aliases on the fields to fetch both if this was intentional.",
                    locations=[
                        Location(line=3, column=15, line_end=6, column_end=16),
                        Location(line=4, column=17, line_end=4, column_end=21),
                        Location(line=5, column=17, line_end=5, column_end=21),
                        Location(
                            line=7, column=15, line_end=10, column_end=16
                        ),
                        Location(line=8, column=17, line_end=8, column_end=21),
                        Location(line=9, column=17, line_end=9, column_end=21),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.3.2",
                        "tag": "field-selection-merging",
                        "details": "http://spec.graphql.org/June2018/#sec-Field-Selection-Merging",
                    },
                )
            ],
        ),
        (
            """
            {
              field {
                deepField {
                  x: a
                }
              },
              field {
                deepField {
                  x: b
                }
              }
            }
            """,
            [
                TartifletteError(
                    message="Fields < field > conflict because subfields < deepField > conflict because subfields < x > conflict because < a > and < b > are different fields. Use different aliases on the fields to fetch both if this was intentional.",
                    locations=[
                        Location(line=3, column=15, line_end=7, column_end=16),
                        Location(line=4, column=17, line_end=6, column_end=18),
                        Location(line=5, column=19, line_end=5, column_end=23),
                        Location(
                            line=8, column=15, line_end=12, column_end=16
                        ),
                        Location(
                            line=9, column=17, line_end=11, column_end=18
                        ),
                        Location(
                            line=10, column=19, line_end=10, column_end=23
                        ),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.3.2",
                        "tag": "field-selection-merging",
                        "details": "http://spec.graphql.org/June2018/#sec-Field-Selection-Merging",
                    },
                )
            ],
        ),
        (
            """
            {
              field {
                deepField {
                  x: a
                }
                deepField {
                  x: b
                }
              },
              field {
                deepField {
                  y
                }
              }
            }
            """,
            [
                TartifletteError(
                    message="Fields < deepField > conflict because subfields < x > conflict because < a > and < b > are different fields. Use different aliases on the fields to fetch both if this was intentional.",
                    locations=[
                        Location(line=4, column=17, line_end=6, column_end=18),
                        Location(line=5, column=19, line_end=5, column_end=23),
                        Location(line=7, column=17, line_end=9, column_end=18),
                        Location(line=8, column=19, line_end=8, column_end=23),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.3.2",
                        "tag": "field-selection-merging",
                        "details": "http://spec.graphql.org/June2018/#sec-Field-Selection-Merging",
                    },
                )
            ],
        ),
        (
            """
            {
              field {
                ...F
              }
              field {
                ...F
              }
            }
            fragment F on T {
              deepField {
                deeperField {
                  x: a
                }
                deeperField {
                  x: b
                }
              },
              deepField {
                deeperField {
                  y
                }
              }
            }
            """,
            [
                TartifletteError(
                    message="Fields < deeperField > conflict because subfields < x > conflict because < a > and < b > are different fields. Use different aliases on the fields to fetch both if this was intentional.",
                    locations=[
                        Location(
                            line=12, column=17, line_end=14, column_end=18
                        ),
                        Location(
                            line=13, column=19, line_end=13, column_end=23
                        ),
                        Location(
                            line=15, column=17, line_end=17, column_end=18
                        ),
                        Location(
                            line=16, column=19, line_end=16, column_end=23
                        ),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.3.2",
                        "tag": "field-selection-merging",
                        "details": "http://spec.graphql.org/June2018/#sec-Field-Selection-Merging",
                    },
                )
            ],
        ),
        (
            """
            {
              field {
                ...F
              }
              field {
                ...I
              }
            }
            fragment F on T {
              x: a
              ...G
            }
            fragment G on T {
              y: c
            }
            fragment I on T {
              y: d
              ...J
            }
            fragment J on T {
              x: b
            }
            """,
            [
                TartifletteError(
                    message="Fields < field > conflict because subfields < x > conflict because < a > and < b > are different fields and subfields < y > conflict because < c > and < d > are different fields. Use different aliases on the fields to fetch both if this was intentional.",
                    locations=[
                        Location(line=3, column=15, line_end=5, column_end=16),
                        Location(
                            line=11, column=15, line_end=11, column_end=19
                        ),
                        Location(
                            line=15, column=15, line_end=15, column_end=19
                        ),
                        Location(line=6, column=15, line_end=8, column_end=16),
                        Location(
                            line=22, column=15, line_end=22, column_end=19
                        ),
                        Location(
                            line=18, column=15, line_end=18, column_end=19
                        ),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.3.2",
                        "tag": "field-selection-merging",
                        "details": "http://spec.graphql.org/June2018/#sec-Field-Selection-Merging",
                    },
                )
            ],
        ),
        (
            """
            {
              field
              ...Unknown
              ...Known
            }

            fragment Known on T {
              field
              ...OtherUnknown
            }
            """,
            [],
        ),
        # ...
        # ...
        # ...
        # ...
        # ...
        (
            """
            fragment fragA on Human { name, relatives { name, ...fragA } }
            """,
            [],
        ),
        (
            """
            fragment fragA on Human { name, ...fragA }
            """,
            [],
        ),
        (
            """
            fragment fragA on Human { name, ...fragB }
            fragment fragB on Human { name, ...fragC }
            fragment fragC on Human { name, ...fragA }
            """,
            [],
        ),
        (
            """
            fragment sameAliasesWithDifferentFieldTargets on Dog {
              ...sameAliasesWithDifferentFieldTargets
              fido: name
              fido: nickname
            }
            """,
            [
                TartifletteError(
                    message="Fields < fido > conflict because < name > and < nickname > are different fields. Use different aliases on the fields to fetch both if this was intentional.",
                    locations=[
                        Location(line=4, column=15, line_end=4, column_end=25),
                        Location(line=5, column=15, line_end=5, column_end=29),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.3.2",
                        "tag": "field-selection-merging",
                        "details": "http://spec.graphql.org/June2018/#sec-Field-Selection-Merging",
                    },
                )
            ],
        ),
    ],
)
async def test_overlapping_fields_can_be_merged_harness(
    engine, query, expected
):
    assert_unordered_lists(
        validate_query(
            engine._schema,
            parse_to_document(query, engine._schema),
            rules=[OverlappingFieldsCanBeMergedRule],
        ),
        expected,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
            {
              someBox {
                ...on IntBox {
                  scalar
                }
                ...on NonNullStringBox1 {
                  scalar
                }
              }
            }
            """,
            [
                TartifletteError(
                    message="Fields < scalar > conflict because they return conflicting types < Int > and < String! >. Use different aliases on the fields to fetch both if this was intentional.",
                    locations=[
                        Location(line=5, column=19, line_end=5, column_end=25),
                        Location(line=8, column=19, line_end=8, column_end=25),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.3.2",
                        "tag": "field-selection-merging",
                        "details": "http://spec.graphql.org/June2018/#sec-Field-Selection-Merging",
                    },
                )
            ],
        ),
        (
            """
            {
              someBox {
                ... on SomeBox {
                  deepBox {
                    unrelatedField
                  }
                }
                ... on StringBox {
                  deepBox {
                    unrelatedField
                  }
                }
              }
            }
            """,
            [],
        ),
        (
            """
            {
              someBox {
                ... on IntBox {
                  scalar
                }
                ... on StringBox {
                  scalar
                }
              }
            }
            """,
            [
                TartifletteError(
                    message="Fields < scalar > conflict because they return conflicting types < Int > and < String >. Use different aliases on the fields to fetch both if this was intentional.",
                    locations=[
                        Location(line=5, column=19, line_end=5, column_end=25),
                        Location(line=8, column=19, line_end=8, column_end=25),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.3.2",
                        "tag": "field-selection-merging",
                        "details": "http://spec.graphql.org/June2018/#sec-Field-Selection-Merging",
                    },
                )
            ],
        ),
        (
            """
            {
              someBox {
                ... on IntBox {
                  deepBox {
                    ...X
                  }
                }
              }
              someBox {
                ... on StringBox {
                  deepBox {
                    ...Y
                  }
                }
              }
              memoed: someBox {
                ... on IntBox {
                  deepBox {
                    ...X
                  }
                }
              }
              memoed: someBox {
                ... on StringBox {
                  deepBox {
                    ...Y
                  }
                }
              }
              other: someBox {
                ...X
              }
              other: someBox {
                ...Y
              }
            }
            fragment X on SomeBox {
              scalar
            }
            fragment Y on SomeBox {
              scalar: unrelatedField
            }
            """,
            [
                TartifletteError(
                    message="Fields < other > conflict because subfields < scalar > conflict because < scalar > and < unrelatedField > are different fields. Use different aliases on the fields to fetch both if this was intentional.",
                    locations=[
                        Location(
                            line=31, column=15, line_end=33, column_end=16
                        ),
                        Location(
                            line=39, column=15, line_end=39, column_end=21
                        ),
                        Location(
                            line=34, column=15, line_end=36, column_end=16
                        ),
                        Location(
                            line=42, column=15, line_end=42, column_end=37
                        ),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.3.2",
                        "tag": "field-selection-merging",
                        "details": "http://spec.graphql.org/June2018/#sec-Field-Selection-Merging",
                    },
                )
            ],
        ),
        (
            """
            {
              someBox {
                ... on NonNullStringBox1 {
                  scalar
                }
                ... on StringBox {
                  scalar
                }
              }
            }
            """,
            [
                TartifletteError(
                    message="Fields < scalar > conflict because they return conflicting types < String! > and < String >. Use different aliases on the fields to fetch both if this was intentional.",
                    locations=[
                        Location(line=5, column=19, line_end=5, column_end=25),
                        Location(line=8, column=19, line_end=8, column_end=25),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.3.2",
                        "tag": "field-selection-merging",
                        "details": "http://spec.graphql.org/June2018/#sec-Field-Selection-Merging",
                    },
                )
            ],
        ),
        (
            """
            {
              someBox {
                ... on IntBox {
                  box: listStringBox {
                    scalar
                  }
                }
                ... on StringBox {
                  box: stringBox {
                    scalar
                  }
                }
              }
            }
            """,
            [
                TartifletteError(
                    message="Fields < box > conflict because they return conflicting types < [StringBox] > and < StringBox >. Use different aliases on the fields to fetch both if this was intentional.",
                    locations=[
                        Location(line=5, column=19, line_end=7, column_end=20),
                        Location(
                            line=10, column=19, line_end=12, column_end=20
                        ),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.3.2",
                        "tag": "field-selection-merging",
                        "details": "http://spec.graphql.org/June2018/#sec-Field-Selection-Merging",
                    },
                )
            ],
        ),
        (
            """
            {
              someBox {
                ... on IntBox {
                  box: stringBox {
                    scalar
                  }
                }
                ... on StringBox {
                  box: listStringBox {
                    scalar
                  }
                }
              }
            }
            """,
            [
                TartifletteError(
                    message="Fields < box > conflict because they return conflicting types < StringBox > and < [StringBox] >. Use different aliases on the fields to fetch both if this was intentional.",
                    locations=[
                        Location(line=5, column=19, line_end=7, column_end=20),
                        Location(
                            line=10, column=19, line_end=12, column_end=20
                        ),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.3.2",
                        "tag": "field-selection-merging",
                        "details": "http://spec.graphql.org/June2018/#sec-Field-Selection-Merging",
                    },
                )
            ],
        ),
        (
            """
            {
              someBox {
                ... on IntBox {
                  box: stringBox {
                    val: scalar
                    val: unrelatedField
                  }
                }
                ... on StringBox {
                  box: stringBox {
                    val: scalar
                  }
                }
              }
            }
            """,
            [
                TartifletteError(
                    message="Fields < val > conflict because < scalar > and < unrelatedField > are different fields. Use different aliases on the fields to fetch both if this was intentional.",
                    locations=[
                        Location(line=6, column=21, line_end=6, column_end=32),
                        Location(line=7, column=21, line_end=7, column_end=40),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.3.2",
                        "tag": "field-selection-merging",
                        "details": "http://spec.graphql.org/June2018/#sec-Field-Selection-Merging",
                    },
                )
            ],
        ),
        (
            """
            {
              someBox {
                ... on IntBox {
                  box: stringBox {
                    scalar
                  }
                }
                ... on StringBox {
                  box: intBox {
                    scalar
                  }
                }
              }
            }
            """,
            [
                TartifletteError(
                    message="Fields < box > conflict because subfields < scalar > conflict because they return conflicting types < String > and < Int >. Use different aliases on the fields to fetch both if this was intentional.",
                    locations=[
                        Location(line=5, column=19, line_end=7, column_end=20),
                        Location(line=6, column=21, line_end=6, column_end=27),
                        Location(
                            line=10, column=19, line_end=12, column_end=20
                        ),
                        Location(
                            line=11, column=21, line_end=11, column_end=27
                        ),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.3.2",
                        "tag": "field-selection-merging",
                        "details": "http://spec.graphql.org/June2018/#sec-Field-Selection-Merging",
                    },
                )
            ],
        ),
        (
            """
            {
              someBox {
                ... on IntBox {
                  scalar: unrelatedField
                }
                ... on StringBox {
                  scalar
                }
              }
            }
            """,
            [],
        ),
        (
            """
            {
              someBox {
                ...on NonNullStringBox1 {
                  scalar
                }
                ...on NonNullStringBox2 {
                  scalar
                }
              }
            }
            """,
            [],
        ),
        (
            """
            {
              a
              ... {
                a
              }
            }
            """,
            [],
        ),
        (
            """
            {
              connection {
                ...edgeID
                edges {
                  node {
                    id: name
                  }
                }
              }
            }

            fragment edgeID on Connection {
              edges {
                node {
                  id
                }
              }
            }
            """,
            [
                TartifletteError(
                    message="Fields < edges > conflict because subfields < node > conflict because subfields < id > conflict because < name > and < id > are different fields. Use different aliases on the fields to fetch both if this was intentional.",
                    locations=[
                        Location(line=5, column=17, line_end=9, column_end=18),
                        Location(line=6, column=19, line_end=8, column_end=20),
                        Location(line=7, column=21, line_end=7, column_end=29),
                        Location(
                            line=14, column=15, line_end=18, column_end=16
                        ),
                        Location(
                            line=15, column=17, line_end=17, column_end=18
                        ),
                        Location(
                            line=16, column=19, line_end=16, column_end=21
                        ),
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.3.2",
                        "tag": "field-selection-merging",
                        "details": "http://spec.graphql.org/June2018/#sec-Field-Selection-Merging",
                    },
                )
            ],
        ),
        (
            """
            {
              someBox {
                ...on UnknownType {
                  scalar
                }
                ...on NonNullStringBox2 {
                  scalar
                }
              }
            }
            """,
            [],
        ),
    ],
)
async def test_overlapping_fields_can_be_merged_box(
    ttftt_engine, query, expected
):
    assert_unordered_lists(
        validate_query(
            ttftt_engine._schema,
            parse_to_document(query, ttftt_engine._schema),
            rules=[OverlappingFieldsCanBeMergedRule],
        ),
        expected,
    )


@pytest.mark.asyncio
async def test_overlapping_fields_can_be_merged_foo():
    engine = await create_engine(
        """
        type Foo {
          items: String
          values: String
          str: String
          dict: String
          for: String
          isinstance: String
        }

        type Query {
          foo: Foo
        }
        """,
        schema_name="test_overlapping_fields_can_be_merged_foo",
    )

    assert_unordered_lists(
        validate_query(
            engine._schema,
            parse_to_document(
                """
                {
                  foo {
                    items
                    values
                    str
                    dict
                    for
                    isinstance
                  }
                }
                """,
                engine._schema,
            ),
            rules=[OverlappingFieldsCanBeMergedRule],
        ),
        [],
    )
