import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import Location
from tartiflette.language.parsers.lark import parse_to_document
from tartiflette.validation.rules import PossibleTypeExtensionsRule
from tartiflette.validation.validate import validate_sdl


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "sdl,expected",
    [
        (
            """
            scalar FooScalar
            type FooObject
            interface FooInterface
            union FooUnion
            enum FooEnum
            input FooInputObject
            """,
            [],
        ),
        (
            """
            scalar FooScalar
            type FooObject
            interface FooInterface
            union FooUnion
            enum FooEnum
            input FooInputObject

            extend scalar FooScalar @dummy
            extend type FooObject @dummy
            extend interface FooInterface @dummy
            extend union FooUnion @dummy
            extend enum FooEnum @dummy
            extend input FooInputObject @dummy
            """,
            [],
        ),
        (
            """
            scalar FooScalar
            type FooObject
            interface FooInterface
            union FooUnion
            enum FooEnum
            input FooInputObject

            extend scalar FooScalar @dummy
            extend type FooObject @dummy
            extend interface FooInterface @dummy
            extend union FooUnion @dummy
            extend enum FooEnum @dummy
            extend input FooInputObject @dummy

            extend scalar FooScalar @dummy
            extend type FooObject @dummy
            extend interface FooInterface @dummy
            extend union FooUnion @dummy
            extend enum FooEnum @dummy
            extend input FooInputObject @dummy
            """,
            [],
        ),
        (
            """
            type Known

            extend scalar Unknown @dummy
            extend type Unknown @dummy
            extend interface Unknown @dummy
            extend union Unknown @dummy
            extend enum Unknown @dummy
            extend input Unknown @dummy
            """,
            [
                TartifletteError(
                    message="Cannot extend type < Unknown > because it is not defined. Did you mean Known?",
                    locations=[
                        Location(line=4, column=27, line_end=4, column_end=34)
                    ],
                ),
                TartifletteError(
                    message="Cannot extend type < Unknown > because it is not defined. Did you mean Known?",
                    locations=[
                        Location(line=5, column=25, line_end=5, column_end=32)
                    ],
                ),
                TartifletteError(
                    message="Cannot extend type < Unknown > because it is not defined. Did you mean Known?",
                    locations=[
                        Location(line=6, column=30, line_end=6, column_end=37)
                    ],
                ),
                TartifletteError(
                    message="Cannot extend type < Unknown > because it is not defined. Did you mean Known?",
                    locations=[
                        Location(line=7, column=26, line_end=7, column_end=33)
                    ],
                ),
                TartifletteError(
                    message="Cannot extend type < Unknown > because it is not defined. Did you mean Known?",
                    locations=[
                        Location(line=8, column=25, line_end=8, column_end=32)
                    ],
                ),
                TartifletteError(
                    message="Cannot extend type < Unknown > because it is not defined. Did you mean Known?",
                    locations=[
                        Location(line=9, column=26, line_end=9, column_end=33)
                    ],
                ),
            ],
        ),
        (
            """
            directive @Foo on SCHEMA

            extend scalar Foo @dummy
            extend type Foo @dummy
            extend interface Foo @dummy
            extend union Foo @dummy
            extend enum Foo @dummy
            extend input Foo @dummy
            """,
            [
                TartifletteError(
                    message="Cannot extend type < Foo > because it is not defined.",
                    locations=[
                        Location(line=4, column=27, line_end=4, column_end=30)
                    ],
                ),
                TartifletteError(
                    message="Cannot extend type < Foo > because it is not defined.",
                    locations=[
                        Location(line=5, column=25, line_end=5, column_end=28)
                    ],
                ),
                TartifletteError(
                    message="Cannot extend type < Foo > because it is not defined.",
                    locations=[
                        Location(line=6, column=30, line_end=6, column_end=33)
                    ],
                ),
                TartifletteError(
                    message="Cannot extend type < Foo > because it is not defined.",
                    locations=[
                        Location(line=7, column=26, line_end=7, column_end=29)
                    ],
                ),
                TartifletteError(
                    message="Cannot extend type < Foo > because it is not defined.",
                    locations=[
                        Location(line=8, column=25, line_end=8, column_end=28)
                    ],
                ),
                TartifletteError(
                    message="Cannot extend type < Foo > because it is not defined.",
                    locations=[
                        Location(line=9, column=26, line_end=9, column_end=29)
                    ],
                ),
            ],
        ),
        (
            """
            scalar FooScalar
            type FooObject
            interface FooInterface
            union FooUnion
            enum FooEnum
            input FooInputObject

            extend type FooScalar @dummy
            extend interface FooObject @dummy
            extend union FooInterface @dummy
            extend enum FooUnion @dummy
            extend input FooEnum @dummy
            extend scalar FooInputObject @dummy
            """,
            [
                TartifletteError(
                    message="Cannot extend non-scalar type < FooScalar >.",
                    locations=[
                        Location(line=2, column=13, line_end=2, column_end=29),
                        Location(line=9, column=13, line_end=9, column_end=41),
                    ],
                ),
                TartifletteError(
                    message="Cannot extend non-object type < FooObject >.",
                    locations=[
                        Location(line=3, column=13, line_end=3, column_end=27),
                        Location(
                            line=10, column=13, line_end=10, column_end=46
                        ),
                    ],
                ),
                TartifletteError(
                    message="Cannot extend non-interface type < FooInterface >.",
                    locations=[
                        Location(line=4, column=13, line_end=4, column_end=35),
                        Location(
                            line=11, column=13, line_end=11, column_end=45
                        ),
                    ],
                ),
                TartifletteError(
                    message="Cannot extend non-union type < FooUnion >.",
                    locations=[
                        Location(line=5, column=13, line_end=5, column_end=27),
                        Location(
                            line=12, column=13, line_end=12, column_end=40
                        ),
                    ],
                ),
                TartifletteError(
                    message="Cannot extend non-enum type < FooEnum >.",
                    locations=[
                        Location(line=6, column=13, line_end=6, column_end=25),
                        Location(
                            line=13, column=13, line_end=13, column_end=40
                        ),
                    ],
                ),
                TartifletteError(
                    message="Cannot extend non-input object type < FooInputObject >.",
                    locations=[
                        Location(line=7, column=13, line_end=7, column_end=33),
                        Location(
                            line=14, column=13, line_end=14, column_end=48
                        ),
                    ],
                ),
            ],
        ),
    ],
)
async def test_possible_type_extensions(sdl, expected):
    assert (
        validate_sdl(
            parse_to_document(sdl), rules=[PossibleTypeExtensionsRule]
        )
        == expected
    )
