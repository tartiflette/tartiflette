import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import Location
from tartiflette.language.parsers.lark import parse_to_document
from tartiflette.validation.rules.valid_names import ValidNamesRule
from tartiflette.validation.validate import validate_sdl


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "sdl,expected",
    [
        (
            """
            scalar String
            type SomeObject
            interface SomeInterface
            union SomeUnion = SomeObject
            enum SomeEnum
            input SomeInput

            directive @someDirective on FIELD
            """,
            [],
        ),
        (
            """
            scalar String
            type SomeObject {
              field: String
            }
            interface SomeInterface {
              field: String
            }
            union SomeUnion = SomeObject
            enum SomeEnum {
              ENUM_VALUE
            }
            input SomeInput {
              field: String
            }

            directive @someDirective(arg: String) on FIELD
            """,
            [],
        ),
        (
            """
            scalar String
            type SomeObject {
              field(arg: String): String
            }
            interface SomeInterface {
              field(arg: String): String
            }
            union SomeUnion = SomeObject
            enum SomeEnum {
              ENUM_VALUE
            }
            input SomeInput {
              field: String
            }

            directive @someDirective(arg: String) on FIELD
            """,
            [],
        ),
        (
            """
            scalar __String
            type __SomeObject
            interface __SomeInterface
            union __SomeUnion = __SomeObject
            enum __SomeEnum
            input __SomeInput

            directive @__someDirective on FIELD
            """,
            [
                TartifletteError(
                    message='Name < __String > must not begin with "__", which is reserved by GraphQL introspection.',
                    locations=[
                        Location(line=2, column=20, line_end=2, column_end=28)
                    ],
                ),
                TartifletteError(
                    message='Name < __SomeObject > must not begin with "__", which is reserved by GraphQL introspection.',
                    locations=[
                        Location(line=3, column=18, line_end=3, column_end=30)
                    ],
                ),
                TartifletteError(
                    message='Name < __SomeInterface > must not begin with "__", which is reserved by GraphQL introspection.',
                    locations=[
                        Location(line=4, column=23, line_end=4, column_end=38)
                    ],
                ),
                TartifletteError(
                    message='Name < __SomeUnion > must not begin with "__", which is reserved by GraphQL introspection.',
                    locations=[
                        Location(line=5, column=19, line_end=5, column_end=30)
                    ],
                ),
                TartifletteError(
                    message='Name < __SomeEnum > must not begin with "__", which is reserved by GraphQL introspection.',
                    locations=[
                        Location(line=6, column=18, line_end=6, column_end=28)
                    ],
                ),
                TartifletteError(
                    message='Name < __SomeInput > must not begin with "__", which is reserved by GraphQL introspection.',
                    locations=[
                        Location(line=7, column=19, line_end=7, column_end=30)
                    ],
                ),
                TartifletteError(
                    message='Name < __someDirective > must not begin with "__", which is reserved by GraphQL introspection.',
                    locations=[
                        Location(line=9, column=24, line_end=9, column_end=39)
                    ],
                ),
            ],
        ),
        (
            """
            scalar String
            type SomeObject {
              __field: String
            }
            interface SomeInterface {
              __field: String
            }
            union SomeUnion = SomeObject
            enum SomeEnum {
              __ENUM_VALUE
            }
            input SomeInput {
              __field: String
            }

            directive @someDirective(__arg: String) on FIELD
            """,
            [
                TartifletteError(
                    message='Name < __field > must not begin with "__", which is reserved by GraphQL introspection.',
                    locations=[
                        Location(line=4, column=15, line_end=4, column_end=22)
                    ],
                ),
                TartifletteError(
                    message='Name < __field > must not begin with "__", which is reserved by GraphQL introspection.',
                    locations=[
                        Location(line=7, column=15, line_end=7, column_end=22)
                    ],
                ),
                TartifletteError(
                    message='Name < __ENUM_VALUE > must not begin with "__", which is reserved by GraphQL introspection.',
                    locations=[
                        Location(
                            line=11, column=15, line_end=11, column_end=27
                        )
                    ],
                ),
                TartifletteError(
                    message='Name < __field > must not begin with "__", which is reserved by GraphQL introspection.',
                    locations=[
                        Location(
                            line=14, column=15, line_end=14, column_end=22
                        )
                    ],
                ),
                TartifletteError(
                    message='Name < __arg > must not begin with "__", which is reserved by GraphQL introspection.',
                    locations=[
                        Location(
                            line=17, column=38, line_end=17, column_end=43
                        )
                    ],
                ),
            ],
        ),
        (
            """
            scalar String
            type SomeObject {
              field(__arg: String): String
            }
            interface SomeInterface {
              field(__arg: String): String
            }
            union SomeUnion = SomeObject
            enum SomeEnum {
              ENUM_VALUE
            }
            input SomeInput {
              field: String
            }

            directive @someDirective(__arg: String) on FIELD
            """,
            [
                TartifletteError(
                    message='Name < __arg > must not begin with "__", which is reserved by GraphQL introspection.',
                    locations=[
                        Location(line=4, column=21, line_end=4, column_end=26)
                    ],
                ),
                TartifletteError(
                    message='Name < __arg > must not begin with "__", which is reserved by GraphQL introspection.',
                    locations=[
                        Location(line=7, column=21, line_end=7, column_end=26)
                    ],
                ),
                TartifletteError(
                    message='Name < __arg > must not begin with "__", which is reserved by GraphQL introspection.',
                    locations=[
                        Location(
                            line=17, column=38, line_end=17, column_end=43
                        )
                    ],
                ),
            ],
        ),
        (
            """
            type __Schema
            type __Type
            type __Field
            type __InputValue
            type __EnumValue
            enum __TypeKind
            type __Directive
            enum __DirectiveLocation
            """,
            [],
        ),
    ],
)
async def test_valid_names(sdl, expected):
    assert (
        validate_sdl(parse_to_document(sdl), rules=[ValidNamesRule])
        == expected
    )
