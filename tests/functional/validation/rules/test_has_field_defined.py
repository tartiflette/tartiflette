import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import Location
from tartiflette.language.parsers.lark import parse_to_document
from tartiflette.validation.rules import HasFieldDefinedRule
from tartiflette.validation.validate import validate_sdl


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "sdl,expected",
    [
        (
            """
            interface Foo {
              field1: String
            }
            """,
            [],
        ),
        (
            """
            interface Foo
            extend interface Foo {
              field1: String
            }
            """,
            [],
        ),
        (
            """
            interface Foo {
              field1: String
              field2: String
            }
            interface Bar {
              field1: String
              field2: String
            }
            """,
            [],
        ),
        (
            """
            interface Foo
            interface Bar
            extend interface Foo {
              field1: String
              field2: String
            }
            extend interface Bar {
              field1: String
              field2: String
            }
            """,
            [],
        ),
        (
            """
            interface Foo {
              field1: String
            }
            """,
            [],
        ),
        (
            """
            interface Foo
            extend interface Foo {
              field1: String
            }
            """,
            [],
        ),
        (
            """
            interface Foo {
              field1: String
              field2: String
            }
            interface Bar {
              field1: String
              field2: String
            }
            """,
            [],
        ),
        (
            """
            interface Foo
            interface Bar
            extend interface Foo {
              field1: String
              field2: String
            }
            extend interface Bar {
              field1: String
              field2: String
            }
            """,
            [],
        ),
        (
            """
            interface Foo
            """,
            [
                TartifletteError(
                    message="Type < Foo > must define one or more fields.",
                    locations=[
                        Location(line=2, column=13, line_end=2, column_end=26)
                    ],
                )
            ],
        ),
        (
            """
            interface Foo
            extend interface Foo @noop
            """,
            [
                TartifletteError(
                    message="Type < Foo > must define one or more fields.",
                    locations=[
                        Location(line=2, column=13, line_end=2, column_end=26),
                        Location(line=3, column=13, line_end=3, column_end=39),
                    ],
                )
            ],
        ),
        (
            """
            interface Foo {
              field1: String
              field2: String
            }
            interface Bar
            """,
            [
                TartifletteError(
                    message="Type < Bar > must define one or more fields.",
                    locations=[
                        Location(line=6, column=13, line_end=6, column_end=26)
                    ],
                )
            ],
        ),
        (
            """
            interface Foo
            interface Bar
            extend interface Foo {
              field1: String
              field2: String
            }
            extend interface Bar @noop
            """,
            [
                TartifletteError(
                    message="Type < Bar > must define one or more fields.",
                    locations=[
                        Location(line=3, column=13, line_end=3, column_end=26),
                        Location(line=8, column=13, line_end=8, column_end=39),
                    ],
                )
            ],
        ),
        (
            """
                type Foo {
                  field1: String
                }
                """,
            [],
        ),
        (
            """
                type Foo
                extend type Foo {
                  field1: String
                }
                """,
            [],
        ),
        (
            """
                type Foo {
                  field1: String
                  field2: String
                }
                type Bar {
                  field1: String
                  field2: String
                }
                """,
            [],
        ),
        (
            """
                type Foo
                type Bar
                extend type Foo {
                  field1: String
                  field2: String
                }
                extend type Bar {
                  field1: String
                  field2: String
                }
                """,
            [],
        ),
        (
            """
                type Foo {
                  field1: String
                }
                """,
            [],
        ),
        (
            """
                type Foo
                extend type Foo {
                  field1: String
                }
                """,
            [],
        ),
        (
            """
                type Foo {
                  field1: String
                  field2: String
                }
                type Bar {
                  field1: String
                  field2: String
                }
                """,
            [],
        ),
        (
            """
                type Foo
                type Bar
                extend type Foo {
                  field1: String
                  field2: String
                }
                extend type Bar {
                  field1: String
                  field2: String
                }
                """,
            [],
        ),
        (
            """
                type Foo
                """,
            [
                TartifletteError(
                    message="Type < Foo > must define one or more fields.",
                    locations=[
                        Location(line=2, column=17, line_end=2, column_end=25)
                    ],
                )
            ],
        ),
        (
            """
                type Foo
                extend type Foo @noop
                """,
            [
                TartifletteError(
                    message="Type < Foo > must define one or more fields.",
                    locations=[
                        Location(line=2, column=17, line_end=2, column_end=25),
                        Location(line=3, column=17, line_end=3, column_end=38),
                    ],
                )
            ],
        ),
        (
            """
                type Foo {
                  field1: String
                  field2: String
                }
                type Bar
                """,
            [
                TartifletteError(
                    message="Type < Bar > must define one or more fields.",
                    locations=[
                        Location(line=6, column=17, line_end=6, column_end=25)
                    ],
                )
            ],
        ),
        (
            """
                type Foo
                type Bar
                extend type Foo {
                  field1: String
                  field2: String
                }
                extend type Bar @noop
                """,
            [
                TartifletteError(
                    message="Type < Bar > must define one or more fields.",
                    locations=[
                        Location(line=3, column=17, line_end=3, column_end=25),
                        Location(line=8, column=17, line_end=8, column_end=38),
                    ],
                )
            ],
        ),
    ],
)
async def test_has_field_defined(sdl, expected):
    assert (
        validate_sdl(parse_to_document(sdl), rules=[HasFieldDefinedRule])
        == expected
    )
