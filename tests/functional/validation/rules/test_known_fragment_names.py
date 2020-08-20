import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import Location
from tartiflette.language.parsers.libgraphqlparser import parse_to_document
from tartiflette.validation.rules import KnownFragmentNamesRule
from tartiflette.validation.validate import validate_query
from tests.functional.utils import assert_unordered_lists


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="harness")
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
                ... {
                  name
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
            {
              human(id: 4) {
                ...UnknownFragment1
                ... on Human {
                  ...UnknownFragment2
                }
              }
            }
            fragment HumanFields on Human {
              name
              ...UnknownFragment3
            }
            """,
            [
                TartifletteError(
                    message="Unknown fragment < UnknownFragment1 >.",
                    locations=[
                        Location(line=4, column=20, line_end=4, column_end=36)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.5.2.1",
                        "tag": "fragment-spread-target-defined",
                        "details": "https://spec.graphql.org/June2018/#sec-Fragment-spread-target-defined",
                    },
                ),
                TartifletteError(
                    message="Unknown fragment < UnknownFragment2 >.",
                    locations=[
                        Location(line=6, column=22, line_end=6, column_end=38)
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.5.2.1",
                        "tag": "fragment-spread-target-defined",
                        "details": "https://spec.graphql.org/June2018/#sec-Fragment-spread-target-defined",
                    },
                ),
                TartifletteError(
                    message="Unknown fragment < UnknownFragment3 >.",
                    locations=[
                        Location(
                            line=12, column=18, line_end=12, column_end=34
                        )
                    ],
                    extensions={
                        "spec": "June 2018",
                        "rule": "5.5.2.1",
                        "tag": "fragment-spread-target-defined",
                        "details": "https://spec.graphql.org/June2018/#sec-Fragment-spread-target-defined",
                    },
                ),
            ],
        ),
    ],
)
async def test_known_fragment_names(schema_stack, query, expected):
    assert_unordered_lists(
        validate_query(
            schema_stack.schema,
            parse_to_document(query),
            rules=[KnownFragmentNamesRule],
        ),
        expected,
    )
