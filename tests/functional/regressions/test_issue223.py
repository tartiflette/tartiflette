import pytest

from tartiflette import Engine, Resolver
from tartiflette.directive import CommonDirective, Directive

_SDL = """

directive @lower on ENUM_VALUE
directive @upper on ENUM_VALUE

enum Size {
    XL
    L
    m
    M @lower
    S
    XS
}

enum Color {
    RED
    GREEN @lower @upper
    black
    BLACK @lower
    yellow
    YELLOW @lower @upper @lower
}

type TShirt {
    size: Size
    color: Color
}

type Query {
    wardrobe: [TShirt]
}
"""


@Directive("lower", schema_name="issue223")
class Lower(CommonDirective):
    @staticmethod
    async def on_enum_value_field_execution(
        directive_args,
        next_directive,
        enum_value,
        field,
        field_args,
        ctx,
        info,
    ):
        return await next_directive(
            enum_value.lower(), field, field_args, ctx, info
        )


@Directive("upper", schema_name="issue223")
class Upper(CommonDirective):
    @staticmethod
    async def on_enum_value_field_execution(
        directive_args,
        next_directive,
        enum_value,
        field,
        field_args,
        ctx,
        info,
    ):
        return await next_directive(
            enum_value.upper(), field, field_args, ctx, info
        )


@Resolver("Query.wardrobe", schema_name="issue223")
async def wardrobe_resolver(_pr, _args, _ctx, _info):
    return [
        {"size": "XL", "color": "GREEN"},
        {"size": "M", "color": "BLACK"},
        {"size": "M", "color": "YELLOW"},
    ]


_ENGINE = Engine(_SDL, schema_name="issue223")


@pytest.mark.asyncio
async def test_issue223():
    assert await _ENGINE.execute("query { wardrobe { size color }}") == {
        "data": {
            "wardrobe": [
                {"size": "XL", "color": "GREEN"},
                {"size": "m", "color": "black"},
                {"size": "m", "color": "yellow"},
            ]
        }
    }
