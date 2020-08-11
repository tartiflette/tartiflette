import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import Location
from tartiflette.language.parsers.lark import parse_to_document
from tartiflette.validation.rules import ValidFieldDefinitionTypesRule
from tartiflette.validation.validate import validate_sdl


@pytest.mark.asyncio
@pytest.mark.parametrize("kind_definition_type", ["interface", "type"])
@pytest.mark.parametrize(
    "field_type_sdl,field_type,expected",
    [
        ("scalar Foo", "Foo", []),
        ("scalar Foo", "Foo!", []),
        ("scalar Foo", "[Foo]", []),
        ("scalar Foo", "[Foo]!", []),
        ("scalar Foo", "[[Foo!]!]!", []),
        ("type Foo", "Foo", []),
        ("type Foo", "Foo!", []),
        ("type Foo", "[Foo]", []),
        ("type Foo", "[Foo]!", []),
        ("type Foo", "[[Foo!]!]!", []),
        ("interface Foo", "Foo", []),
        ("interface Foo", "Foo!", []),
        ("interface Foo", "[Foo]", []),
        ("interface Foo", "[Foo]!", []),
        ("interface Foo", "[[Foo!]!]!", []),
        (
            """
            type Baz
            union Foo = Baz
            """,
            "Foo",
            [],
        ),
        (
            """
            type Baz
            union Foo = Baz
            """,
            "Foo!",
            [],
        ),
        (
            """
            type Baz
            union Foo = Baz
            """,
            "[Foo]",
            [],
        ),
        (
            """
            type Baz
            union Foo = Baz
            """,
            "[Foo]!",
            [],
        ),
        (
            """
            type Baz
            union Foo = Baz
            """,
            "[[Foo!]!]!",
            [],
        ),
        ("enum Foo", "Foo", []),
        ("enum Foo", "Foo!", []),
        ("enum Foo", "[Foo]", []),
        ("enum Foo", "[Foo]!", []),
        ("enum Foo", "[[Foo!]!]!", []),
        (
            "input Foo",
            "Foo",
            [
                TartifletteError(
                    message="The type of < Bar.field > must be Output type but got: Foo.",
                    locations=[
                        Location(line=4, column=14, line_end=4, column_end=17)
                    ],
                )
            ],
        ),
        (
            "input Foo",
            "Foo!",
            [
                TartifletteError(
                    message="The type of < Bar.field > must be Output type but got: Foo!.",
                    locations=[
                        Location(line=4, column=14, line_end=4, column_end=18)
                    ],
                )
            ],
        ),
        (
            "input Foo",
            "[Foo]",
            [
                TartifletteError(
                    message="The type of < Bar.field > must be Output type but got: [Foo].",
                    locations=[
                        Location(line=4, column=14, line_end=4, column_end=19)
                    ],
                )
            ],
        ),
        (
            "input Foo",
            "[Foo]!",
            [
                TartifletteError(
                    message="The type of < Bar.field > must be Output type but got: [Foo]!.",
                    locations=[
                        Location(line=4, column=14, line_end=4, column_end=20)
                    ],
                )
            ],
        ),
        (
            "input Foo",
            "[[Foo!]!]!",
            [
                TartifletteError(
                    message="The type of < Bar.field > must be Output type but got: [[Foo!]!]!.",
                    locations=[
                        Location(line=4, column=14, line_end=4, column_end=24)
                    ],
                )
            ],
        ),
        (
            "directive @Foo on FIELD",
            "Foo",
            [
                TartifletteError(
                    message="The type of < Bar.field > must be Output type but got: Foo.",
                    locations=[
                        Location(line=4, column=14, line_end=4, column_end=17)
                    ],
                )
            ],
        ),
        (
            "directive @Foo on FIELD",
            "Foo!",
            [
                TartifletteError(
                    message="The type of < Bar.field > must be Output type but got: Foo!.",
                    locations=[
                        Location(line=4, column=14, line_end=4, column_end=18)
                    ],
                )
            ],
        ),
        (
            "directive @Foo on FIELD",
            "[Foo]",
            [
                TartifletteError(
                    message="The type of < Bar.field > must be Output type but got: [Foo].",
                    locations=[
                        Location(line=4, column=14, line_end=4, column_end=19)
                    ],
                )
            ],
        ),
        (
            "directive @Foo on FIELD",
            "[Foo]!",
            [
                TartifletteError(
                    message="The type of < Bar.field > must be Output type but got: [Foo]!.",
                    locations=[
                        Location(line=4, column=14, line_end=4, column_end=20)
                    ],
                )
            ],
        ),
        (
            "directive @Foo on FIELD",
            "[[Foo!]!]!",
            [
                TartifletteError(
                    message="The type of < Bar.field > must be Output type but got: [[Foo!]!]!.",
                    locations=[
                        Location(line=4, column=14, line_end=4, column_end=24)
                    ],
                )
            ],
        ),
    ],
)
async def test_valid_field_definition_types(
    kind_definition_type, field_type_sdl, field_type, expected
):
    sdl = f"""
    {field_type_sdl}
    {kind_definition_type} Bar {{
      field: {field_type}
    }}
    """
    assert (
        validate_sdl(
            parse_to_document(sdl), rules=[ValidFieldDefinitionTypesRule]
        )
        == expected
    )
