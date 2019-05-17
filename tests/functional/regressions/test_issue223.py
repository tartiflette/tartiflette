import json

import pytest

from tartiflette import Directive, Engine, Resolver, Scalar
from tartiflette.scalar.builtins.string import ScalarString

_SDL = """

directive @lower on ENUM_VALUE
directive @upper on ENUM_VALUE
directive @capitalized on SCALAR
directive @mapToValue on ENUM
directive @addValue(value: Int = 1) on OBJECT | INPUT_OBJECT

scalar Bobby @capitalized

enum Size {
    XL
    L
    m
    M @lower
    S
    XS
}

enum Color @mapToValue {
    RED
    GREEN @lower @upper
    black
    BLACK @lower
    yellow
    YELLOW @lower @upper @lower
    BROWN
}

input ThisIsAnInputObject @addValue(value: 17) {
    aColor: Color
    value: Int
}

type TShirt {
    size: Size
    color: Color
}

type OKLM @addValue(value: 53) {
    value: Int
}

type Wahou {
    wieght: OKLM
    height: OKLM
}

type Query {
    wardrobe: [TShirt]
    bobby: Bobby
    test3(argument1: Color): String
    test4: Color
    test5: Wahou
    test6(argument1: ThisIsAnInputObject): String
}
"""


@Resolver("Query.test5", schema_name="issue223")
async def resolver_test5(_pr, _args, _ctx, _info):
    return {"wieght": {"value": 2}, "height": {"value": 6}}


@Directive("addValue", schema_name="issue223")
class AddValue:
    @staticmethod
    async def on_post_input_coercion(
        directive_args, next_directive, value, argument_definition, ctx, info
    ):
        value["value"] = value["value"] + directive_args["value"]
        return await next_directive(value, argument_definition, ctx, info)

    @staticmethod
    async def on_pre_output_coercion(
        directive_args, next_directive, value, field_definition, ctx, info
    ):
        value["value"] = value["value"] + directive_args["value"]
        return await next_directive(value, field_definition, ctx, info)


@Directive("mapToValue", schema_name="issue223")
class MapToValue:
    my_map = {"RED": "BROWN", "BROWN": "RED"}

    @staticmethod
    async def on_pre_output_coercion(
        directive_args, next_directive, value, field_definition, ctx, info
    ):
        value = MapToValue.my_map.get(value, value)
        return await next_directive(value, field_definition, ctx, info)

    @staticmethod
    async def on_post_input_coercion(
        directive_args, next_directive, value, argument_definition, ctx, info
    ):
        value = MapToValue.my_map.get(value, value)
        return await next_directive(value, argument_definition, ctx, info)


@Resolver("Query.test4", schema_name="issue223")
async def resolver_test4(_pr, _args, _ctx, _info):
    return "BROWN"


@Resolver("Query.test3", schema_name="issue223")
@Resolver("Query.test6", schema_name="issue223")
async def resolver_test3(_pr, args, _ctx, _info):
    return json.dumps(args)


@Scalar("Bobby", schema_name="issue223")
class BobbyScalar:
    @staticmethod
    def coerce_output(val):
        return str(val)

    @staticmethod
    def coerce_input(val):
        return str(val)


@Directive("capitalized", schema_name="issue223")
class Capitalized:
    @staticmethod
    async def on_pre_output_coercion(
        directive_args, next_directive, value, field_definition, ctx, info
    ):
        return await next_directive(
            value.capitalize(), field_definition, ctx, info
        )


@Directive("lower", schema_name="issue223")
class Lower:
    @staticmethod
    async def on_pre_output_coercion(
        directive_args, next_directive, value, field_definition, ctx, info
    ):
        return await next_directive(value.lower(), field_definition, ctx, info)


@Directive("upper", schema_name="issue223")
class Upper:
    @staticmethod
    async def on_pre_output_coercion(
        directive_args, next_directive, value, field_definition, ctx, info
    ):
        return await next_directive(value.upper(), field_definition, ctx, info)


@Resolver("Query.wardrobe", schema_name="issue223")
async def wardrobe_resolver(_pr, _args, _ctx, _info):
    return [
        {"size": "XL", "color": "GREEN"},
        {"size": "M", "color": "BLACK"},
        {"size": "M", "color": "YELLOW"},
    ]


@Resolver("Query.bobby", schema_name="issue223")
async def bobby_resolver(_pr, _args, _ctx, _info):
    return "lol"


_ENGINE = Engine(_SDL, schema_name="issue223")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            "query { wardrobe { size color }}",
            {
                "data": {
                    "wardrobe": [
                        {"size": "XL", "color": "GREEN"},
                        {"size": "m", "color": "black"},
                        {"size": "m", "color": "yellow"},
                    ]
                }
            },
        ),
        ("query { bobby }", {"data": {"bobby": "Lol"}}),
        (
            "query { test3(argument1: RED) }",
            {"data": {"test3": '{"argument1": "BROWN"}'}},
        ),
        ("query { test4 }", {"data": {"test4": "RED"}}),
        (
            "query { test5 { wieght { value } height { value } } }",
            {
                "data": {
                    "test5": {"wieght": {"value": 55}, "height": {"value": 59}}
                }
            },
        ),
        (
            "query { test6(argument1: { value: 3, aColor: RED })}",
            {
                "data": {
                    "test6": '{"argument1": {"aColor": "BROWN", "value": 20}}'
                }
            },
        ),
    ],
)
async def test_issue223(query, expected):
    assert await _ENGINE.execute(query) == expected
