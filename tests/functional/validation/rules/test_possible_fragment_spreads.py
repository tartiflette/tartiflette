import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import Location
from tartiflette.language.parsers.libgraphqlparser import parse_to_document
from tartiflette.validation.rules import PossibleFragmentSpreadsRule
from tartiflette.validation.validate import validate_query
from tests.functional.utils import assert_unordered_lists


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="harness")
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
            fragment objectWithinObject on Dog { ...dogFragment }
            fragment dogFragment on Dog { barkVolume }
            """,
            [],
        ),
        (
            """
            fragment objectWithinObjectAnon on Dog { ... on Dog { barkVolume } }
            """,
            [],
        ),
        (
            """
            fragment objectWithinInterface on Pet { ...dogFragment }
            fragment dogFragment on Dog { barkVolume }
            """,
            [],
        ),
        (
            """
            fragment objectWithinUnion on CatOrDog { ...dogFragment }
            fragment dogFragment on Dog { barkVolume }
            """,
            [],
        ),
        (
            """
            fragment unionWithinObject on Dog { ...catOrDogFragment }
            fragment catOrDogFragment on CatOrDog { __typename }
            """,
            [],
        ),
        (
            """
            fragment unionWithinInterface on Pet { ...catOrDogFragment }
            fragment catOrDogFragment on CatOrDog { __typename }
            """,
            [],
        ),
        (
            """
            fragment unionWithinUnion on DogOrHuman { ...catOrDogFragment }
            fragment catOrDogFragment on CatOrDog { __typename }
            """,
            [],
        ),
        (
            """
            fragment interfaceWithinObject on Dog { ...petFragment }
            fragment petFragment on Pet { name }
            """,
            [],
        ),
        (
            """
            fragment interfaceWithinInterface on Pet { ...beingFragment }
            fragment beingFragment on Being { name }
            """,
            [],
        ),
        (
            """
            fragment interfaceWithinInterface on Pet { ... on Being { name } }
            """,
            [],
        ),
        (
            """
            fragment interfaceWithinUnion on CatOrDog { ...petFragment }
            fragment petFragment on Pet { name }
            """,
            [],
        ),
        (
            """
            fragment petFragment on Pet { ...badInADifferentWay }
            fragment badInADifferentWay on String { name }
            """,
            [],
        ),
        (
            """
            fragment petFragment on Pet { ...UnknownFragment }
            """,
            [],
        ),
        (
            """
            fragment invalidObjectWithinObject on Cat { ...dogFragment }
            fragment dogFragment on Dog { barkVolume }
            """,
            [
                TartifletteError(
                    message="Fragment < dogFragment > cannot be spread here as objects of type < Cat > can never be of type < Dog >.",
                    locations=[
                        Location(line=2, column=57, line_end=2, column_end=71)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.5.2.3",
                        "tag": "fragment-spread-is-possible",
                        "details": "https://spec.graphql.org/June2018/#sec-Fragment-spread-is-possible",
                    },
                )
            ],
        ),
        (
            """
            fragment invalidObjectWithinObjectAnon on Cat {
              ... on Dog { barkVolume }
            }
            """,
            [
                TartifletteError(
                    message="Fragment cannot be spread here as objects of type < Cat > can never be of type < Dog >.",
                    locations=[
                        Location(line=3, column=15, line_end=3, column_end=40)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.5.2.3",
                        "tag": "fragment-spread-is-possible",
                        "details": "https://spec.graphql.org/June2018/#sec-Fragment-spread-is-possible",
                    },
                )
            ],
        ),
        (
            """
            fragment invalidObjectWithinInterface on Pet { ...humanFragment }
            fragment humanFragment on Human { pets { name } }
            """,
            [
                TartifletteError(
                    message="Fragment < humanFragment > cannot be spread here as objects of type < Pet > can never be of type < Human >.",
                    locations=[
                        Location(line=2, column=60, line_end=2, column_end=76)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.5.2.3",
                        "tag": "fragment-spread-is-possible",
                        "details": "https://spec.graphql.org/June2018/#sec-Fragment-spread-is-possible",
                    },
                )
            ],
        ),
        (
            """
            fragment invalidObjectWithinUnion on CatOrDog { ...humanFragment }
            fragment humanFragment on Human { pets { name } }
            """,
            [
                TartifletteError(
                    message="Fragment < humanFragment > cannot be spread here as objects of type < CatOrDog > can never be of type < Human >.",
                    locations=[
                        Location(line=2, column=61, line_end=2, column_end=77)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.5.2.3",
                        "tag": "fragment-spread-is-possible",
                        "details": "https://spec.graphql.org/June2018/#sec-Fragment-spread-is-possible",
                    },
                )
            ],
        ),
        (
            """
            fragment invalidUnionWithinObject on Human { ...catOrDogFragment }
            fragment catOrDogFragment on CatOrDog { __typename }
            """,
            [
                TartifletteError(
                    message="Fragment < catOrDogFragment > cannot be spread here as objects of type < Human > can never be of type < CatOrDog >.",
                    locations=[
                        Location(line=2, column=58, line_end=2, column_end=77)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.5.2.3",
                        "tag": "fragment-spread-is-possible",
                        "details": "https://spec.graphql.org/June2018/#sec-Fragment-spread-is-possible",
                    },
                )
            ],
        ),
        (
            """
            fragment invalidUnionWithinInterface on Pet { ...humanOrAlienFragment }
            fragment humanOrAlienFragment on HumanOrAlien { __typename }
            """,
            [
                TartifletteError(
                    message="Fragment < humanOrAlienFragment > cannot be spread here as objects of type < Pet > can never be of type < HumanOrAlien >.",
                    locations=[
                        Location(line=2, column=59, line_end=2, column_end=82)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.5.2.3",
                        "tag": "fragment-spread-is-possible",
                        "details": "https://spec.graphql.org/June2018/#sec-Fragment-spread-is-possible",
                    },
                )
            ],
        ),
        (
            """
            fragment invalidUnionWithinUnion on CatOrDog { ...humanOrAlienFragment }
            fragment humanOrAlienFragment on HumanOrAlien { __typename }
            """,
            [
                TartifletteError(
                    message="Fragment < humanOrAlienFragment > cannot be spread here as objects of type < CatOrDog > can never be of type < HumanOrAlien >.",
                    locations=[
                        Location(line=2, column=60, line_end=2, column_end=83)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.5.2.3",
                        "tag": "fragment-spread-is-possible",
                        "details": "https://spec.graphql.org/June2018/#sec-Fragment-spread-is-possible",
                    },
                )
            ],
        ),
        (
            """
            fragment invalidInterfaceWithinObject on Cat { ...intelligentFragment }
            fragment intelligentFragment on Intelligent { iq }
            """,
            [
                TartifletteError(
                    message="Fragment < intelligentFragment > cannot be spread here as objects of type < Cat > can never be of type < Intelligent >.",
                    locations=[
                        Location(line=2, column=60, line_end=2, column_end=82)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.5.2.3",
                        "tag": "fragment-spread-is-possible",
                        "details": "https://spec.graphql.org/June2018/#sec-Fragment-spread-is-possible",
                    },
                )
            ],
        ),
        (
            """
            fragment invalidInterfaceWithinInterface on Pet {
              ...intelligentFragment
            }
            fragment intelligentFragment on Intelligent { iq }
            """,
            [
                TartifletteError(
                    message="Fragment < intelligentFragment > cannot be spread here as objects of type < Pet > can never be of type < Intelligent >.",
                    locations=[
                        Location(line=3, column=15, line_end=3, column_end=37)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.5.2.3",
                        "tag": "fragment-spread-is-possible",
                        "details": "https://spec.graphql.org/June2018/#sec-Fragment-spread-is-possible",
                    },
                )
            ],
        ),
        (
            """
            fragment invalidInterfaceWithinInterfaceAnon on Pet {
              ...on Intelligent { iq }
            }
            """,
            [
                TartifletteError(
                    message="Fragment cannot be spread here as objects of type < Pet > can never be of type < Intelligent >.",
                    locations=[
                        Location(line=3, column=15, line_end=3, column_end=39)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.5.2.3",
                        "tag": "fragment-spread-is-possible",
                        "details": "https://spec.graphql.org/June2018/#sec-Fragment-spread-is-possible",
                    },
                )
            ],
        ),
        (
            """
            fragment invalidInterfaceWithinUnion on HumanOrAlien { ...petFragment }
            fragment petFragment on Pet { name }
            """,
            [
                TartifletteError(
                    message="Fragment < petFragment > cannot be spread here as objects of type < HumanOrAlien > can never be of type < Pet >.",
                    locations=[
                        Location(line=2, column=68, line_end=2, column_end=82)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.5.2.3",
                        "tag": "fragment-spread-is-possible",
                        "details": "https://spec.graphql.org/June2018/#sec-Fragment-spread-is-possible",
                    },
                )
            ],
        ),
    ],
)
async def test_possible_fragment_spreads(schema_stack, query, expected):
    assert_unordered_lists(
        validate_query(
            schema_stack.schema,
            parse_to_document(query),
            rules=[PossibleFragmentSpreadsRule],
        ),
        expected,
    )
