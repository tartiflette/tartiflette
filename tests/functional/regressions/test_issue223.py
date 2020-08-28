import json

from typing import Any, Callable, Dict, Optional

import pytest

from tartiflette import Directive, Resolver, Scalar


def bakery(schema_name):
    @Resolver("Query.test5", schema_name=schema_name)
    async def resolver_test5(_pr, _args, _ctx, _info):
        return {"weight": {"value": 2}, "height": {"value": 6}}

    @Directive("addValue", schema_name=schema_name)
    class AddValue:
        @staticmethod
        async def on_post_input_coercion(
            directive_args: Dict[str, Any],
            next_directive: Callable,
            parent_node,
            input_definition_node,
            value: Any,
            ctx: Optional[Any],
        ):
            value["value"] = value["value"] + directive_args["value"]
            return await next_directive(
                parent_node, input_definition_node, value, ctx
            )

        @staticmethod
        async def on_pre_output_coercion(
            directive_args: Dict[str, Any],
            next_directive: Callable,
            output_definition_node,
            value: Any,
            ctx: Optional[Any],
            info: "ResolveInfo",
        ):
            value["value"] = value["value"] + directive_args["value"]
            return await next_directive(
                output_definition_node, value, ctx, info
            )

    @Directive("mapToValue", schema_name=schema_name)
    class MapToValue:
        my_map = {"RED": "BROWN", "BROWN": "RED"}

        @staticmethod
        async def on_pre_output_coercion(
            directive_args: Dict[str, Any],
            next_directive: Callable,
            output_definition_node,
            value: Any,
            ctx: Optional[Any],
            info: "ResolveInfo",
        ):
            value = MapToValue.my_map.get(value, value)
            return await next_directive(
                output_definition_node, value, ctx, info
            )

        @staticmethod
        async def on_post_input_coercion(
            directive_args: Dict[str, Any],
            next_directive: Callable,
            parent_node,
            input_definition_node,
            value: Any,
            ctx: Optional[Any],
        ):
            value = MapToValue.my_map.get(value, value)
            return await next_directive(
                parent_node, input_definition_node, value, ctx
            )

    @Resolver("Query.test4", schema_name=schema_name)
    async def resolver_test4(_pr, _args, _ctx, _info):
        return "BROWN"

    @Resolver("Query.test3", schema_name=schema_name)
    @Resolver("Query.test6", schema_name=schema_name)
    async def resolver_test3(_pr, args, _ctx, _info):
        return json.dumps(args)

    @Scalar("Bobby", schema_name=schema_name)
    class BobbyScalar:
        @staticmethod
        def coerce_output(val):
            return str(val)

        @staticmethod
        def coerce_input(val):
            return str(val)

        @staticmethod
        def parse_literal(ast):
            return ast.value

    @Directive("capitalized", schema_name=schema_name)
    class Capitalized:
        @staticmethod
        async def on_pre_output_coercion(
            directive_args: Dict[str, Any],
            next_directive: Callable,
            output_definition_node,
            value: Any,
            ctx: Optional[Any],
            info: "ResolveInfo",
        ):
            return await next_directive(
                output_definition_node, value.capitalize(), ctx, info
            )

    @Directive("lower", schema_name=schema_name)
    @Directive("lower2", schema_name=schema_name)
    class Lower:
        @staticmethod
        async def on_pre_output_coercion(
            directive_args: Dict[str, Any],
            next_directive: Callable,
            output_definition_node,
            value: Any,
            ctx: Optional[Any],
            info: "ResolveInfo",
        ):
            return await next_directive(
                output_definition_node, value.lower(), ctx, info
            )

    @Directive("upper", schema_name=schema_name)
    class Upper:
        @staticmethod
        async def on_pre_output_coercion(
            directive_args: Dict[str, Any],
            next_directive: Callable,
            output_definition_node,
            value: Any,
            ctx: Optional[Any],
            info: "ResolveInfo",
        ):
            return await next_directive(
                output_definition_node, value.upper(), ctx, info
            )

    @Resolver("Query.wardrobe", schema_name=schema_name)
    async def wardrobe_resolver(_pr, _args, _ctx, _info):
        return [
            {"size": "XL", "color": "GREEN"},
            {"size": "M", "color": "BLACK"},
            {"size": "M", "color": "YELLOW"},
        ]

    @Resolver("Query.bobby", schema_name=schema_name)
    async def bobby_resolver(_pr, _args, _ctx, _info):
        return "lol"


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl="""
    directive @lower on ENUM_VALUE
    directive @lower2 on ENUM_VALUE
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
        YELLOW @lower @upper @lower2
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
        weight: OKLM
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
    """,
    bakery=bakery,
)
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
            "query { test5 { weight { value } height { value } } }",
            {
                "data": {
                    "test5": {"weight": {"value": 55}, "height": {"value": 59}}
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
async def test_issue223(schema_stack, query, expected):
    assert await schema_stack.execute(query) == expected
