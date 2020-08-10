import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import Location
from tartiflette.language.parsers.libgraphqlparser import parse_to_document
from tartiflette.validation.rules import NoUnusedFragmentsRule
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
              human(id: 4) {
                ...HumanFields1
                ... on Human {
                  ...HumanFields2
                }
              }
            }
            fragment HumanFields1 on Human {
              name
              ...HumanFields3
            }
            fragment HumanFields2 on Human {
              name
            }
            fragment HumanFields3 on Human {
              name
            }
            """,
            [],
        ),
        (
            """
            query Foo {
              human(id: 4) {
                ...HumanFields1
              }
            }
            query Bar {
              human(id: 4) {
                ...HumanFields2
              }
            }
            fragment HumanFields1 on Human {
              name
              ...HumanFields3
            }
            fragment HumanFields2 on Human {
              name
            }
            fragment HumanFields3 on Human {
              name
            }
            """,
            [],
        ),
        (
            """
            query Foo {
              human(id: 4) {
                ...HumanFields1
              }
            }
            query Bar {
              human(id: 4) {
                ...HumanFields2
              }
            }
            fragment HumanFields1 on Human {
              name
              ...HumanFields3
            }
            fragment HumanFields2 on Human {
              name
            }
            fragment HumanFields3 on Human {
              name
            }
            fragment Unused1 on Human {
              name
            }
            fragment Unused2 on Human {
              name
            }
            """,
            [
                TartifletteError(
                    message="Fragment < Unused1 > is never used.",
                    locations=[
                        Location(
                            line=22, column=13, line_end=24, column_end=14
                        )
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.5.1.4",
                        "tag": "fragment-must-be-used",
                        "details": "https://spec.graphql.org/June2018/#sec-Fragments-Must-Be-Used",
                    },
                ),
                TartifletteError(
                    message="Fragment < Unused2 > is never used.",
                    locations=[
                        Location(
                            line=25, column=13, line_end=27, column_end=14
                        )
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.5.1.4",
                        "tag": "fragment-must-be-used",
                        "details": "https://spec.graphql.org/June2018/#sec-Fragments-Must-Be-Used",
                    },
                ),
            ],
        ),
        (
            """
            query Foo {
              human(id: 4) {
                ...HumanFields1
              }
            }
            query Bar {
              human(id: 4) {
                ...HumanFields2
              }
            }
            fragment HumanFields1 on Human {
              name
              ...HumanFields3
            }
            fragment HumanFields2 on Human {
              name
            }
            fragment HumanFields3 on Human {
              name
            }
            fragment Unused1 on Human {
              name
              ...Unused2
            }
            fragment Unused2 on Human {
              name
              ...Unused1
            }
            """,
            [
                TartifletteError(
                    message="Fragment < Unused1 > is never used.",
                    locations=[
                        Location(
                            line=22, column=13, line_end=25, column_end=14
                        )
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.5.1.4",
                        "tag": "fragment-must-be-used",
                        "details": "https://spec.graphql.org/June2018/#sec-Fragments-Must-Be-Used",
                    },
                ),
                TartifletteError(
                    message="Fragment < Unused2 > is never used.",
                    locations=[
                        Location(
                            line=26, column=13, line_end=29, column_end=14
                        )
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.5.1.4",
                        "tag": "fragment-must-be-used",
                        "details": "https://spec.graphql.org/June2018/#sec-Fragments-Must-Be-Used",
                    },
                ),
            ],
        ),
        (
            """
            query Foo {
              human(id: 4) {
                ...bar
              }
            }
            fragment foo on Human {
              name
            }
            """,
            [
                TartifletteError(
                    message="Fragment < foo > is never used.",
                    locations=[
                        Location(line=7, column=13, line_end=9, column_end=14)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.5.1.4",
                        "tag": "fragment-must-be-used",
                        "details": "https://spec.graphql.org/June2018/#sec-Fragments-Must-Be-Used",
                    },
                )
            ],
        ),
    ],
)
async def test_no_unused_fragment(engine, query, expected):
    assert_unordered_lists(
        validate_query(
            engine._schema,
            parse_to_document(query, engine._schema),
            rules=[NoUnusedFragmentsRule],
        ),
        expected,
    )
