from enum import Enum

import pytest

from tartiflette import Directive, Resolver, create_engine

_SDL = """
directive @actAsPyEnum(name: String!) on ENUM

enum FirstEnum @actAsPyEnum(name: "FirstEnum") { V_1, V_2, V_3 }
enum SecondEnum @actAsPyEnum(name: "SecondEnum") { V_1, V_2, V_3 }

type Query {
  anEnum(param: FirstEnum): FirstEnum
  listEnum(param: [SecondEnum]): [SecondEnum]
}
"""


class FirstEnum(Enum):
    V_1 = "v1"
    V_2 = "v2"
    V_3 = "v3"


class SecondEnum(Enum):
    V_1 = 0
    V_2 = 1
    V_3 = 2


_ENUM_MAP = {"FirstEnum": FirstEnum, "SecondEnum": SecondEnum}


@pytest.fixture(scope="module")
async def ttftt_engine():
    @Directive("actAsPyEnum", schema_name="test_issue_233")
    class ActAsPyEnumDirective:
        @staticmethod
        async def on_post_input_coercion(
            directive_args,
            next_directive,
            value,
            argument_definition,
            ctx,
            info,
        ):
            value = await next_directive(value, argument_definition, ctx, info)
            if value is None:
                return value

            try:
                py_enum = _ENUM_MAP[directive_args["name"]]
                if isinstance(value, list):
                    return [
                        None if item is None else py_enum[item].value
                        for item in value
                    ]
                return py_enum[value].value
            except Exception:
                pass
            return value

        @staticmethod
        async def on_pre_output_coercion(
            directive_args, next_directive, value, field_definition, ctx, info
        ):
            value = await next_directive(value, field_definition, ctx, info)
            if value is None:
                return value

            try:
                py_enum = _ENUM_MAP[directive_args["name"]]
                if isinstance(value, list):
                    return [
                        None if item is None else py_enum(item).name
                        for item in value
                    ]
                return py_enum(value).name
            except Exception:
                pass
            return value

    @Resolver("Query.anEnum", schema_name="test_issue_233")
    @Resolver("Query.listEnum", schema_name="test_issue_233")
    async def resolve_query_fields(parent_result, args, ctx, info):
        return args.get("param")

    return await create_engine(sdl=_SDL, schema_name="test_issue_233")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        # anEnum
        ("""{ anEnum }""", None, {"data": {"anEnum": None}}),
        ("""{ anEnum(param: null) }""", None, {"data": {"anEnum": None}}),
        ("""{ anEnum(param: V_1) }""", None, {"data": {"anEnum": "V_1"}}),
        ("""{ anEnum(param: V_2) }""", None, {"data": {"anEnum": "V_2"}}),
        (
            """query ($param: FirstEnum) { anEnum(param: $param) }""",
            None,
            {"data": {"anEnum": None}},
        ),
        (
            """query ($param: FirstEnum) { anEnum(param: $param) }""",
            {"param": None},
            {"data": {"anEnum": None}},
        ),
        (
            """query ($param: FirstEnum) { anEnum(param: $param) }""",
            {"param": "V_1"},
            {"data": {"anEnum": "V_1"}},
        ),
        (
            """query ($param: FirstEnum) { anEnum(param: $param) }""",
            {"param": "V_2"},
            {"data": {"anEnum": "V_2"}},
        ),
        # listEnum
        ("""{ listEnum }""", None, {"data": {"listEnum": None}}),
        ("""{ listEnum(param: null) }""", None, {"data": {"listEnum": None}}),
        (
            """{ listEnum(param: [null]) }""",
            None,
            {"data": {"listEnum": [None]}},
        ),
        (
            """{ listEnum(param: V_1) }""",
            None,
            {"data": {"listEnum": ["V_1"]}},
        ),
        (
            """{ listEnum(param: [V_1]) }""",
            None,
            {"data": {"listEnum": ["V_1"]}},
        ),
        (
            """{ listEnum(param: V_2) }""",
            None,
            {"data": {"listEnum": ["V_2"]}},
        ),
        (
            """{ listEnum(param: [V_2]) }""",
            None,
            {"data": {"listEnum": ["V_2"]}},
        ),
        (
            """{ listEnum(param: [V_1, V_2]) }""",
            None,
            {"data": {"listEnum": ["V_1", "V_2"]}},
        ),
        (
            """{ listEnum(param: [V_1, V_2, null]) }""",
            None,
            {"data": {"listEnum": ["V_1", "V_2", None]}},
        ),
        (
            """query ($param: SecondEnum) { listEnum(param: $param) }""",
            None,
            {"data": {"listEnum": None}},
        ),
        (
            """query ($param: SecondEnum) { listEnum(param: $param) }""",
            {"param": None},
            {"data": {"listEnum": None}},
        ),
        (
            """query ($param: SecondEnum) { listEnum(param: $param) }""",
            {"param": [None]},
            {"data": {"listEnum": [None]}},
        ),
        (
            """query ($param: SecondEnum) { listEnum(param: $param) }""",
            {"param": "V_1"},
            {"data": {"listEnum": ["V_1"]}},
        ),
        (
            """query ($param: SecondEnum) { listEnum(param: $param) }""",
            {"param": ["V_1"]},
            {"data": {"listEnum": ["V_1"]}},
        ),
        (
            """query ($param: SecondEnum) { listEnum(param: $param) }""",
            {"param": "V_2"},
            {"data": {"listEnum": ["V_2"]}},
        ),
        (
            """query ($param: SecondEnum) { listEnum(param: $param) }""",
            {"param": ["V_2"]},
            {"data": {"listEnum": ["V_2"]}},
        ),
        (
            """query ($param: SecondEnum) { listEnum(param: $param) }""",
            {"param": ["V_1", "V_2"]},
            {"data": {"listEnum": ["V_1", "V_2"]}},
        ),
        (
            """query ($param: SecondEnum) { listEnum(param: $param) }""",
            {"param": ["V_1", "V_2", None]},
            {"data": {"listEnum": ["V_1", "V_2", None]}},
        ),
    ],
)
async def test_issue_233(query, variables, expected, ttftt_engine):
    assert await ttftt_engine.execute(query, variables=variables) == expected
