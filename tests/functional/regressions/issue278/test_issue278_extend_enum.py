from typing import Any, Callable, Dict, Optional

import pytest

from tartiflette import Directive, Resolver, create_engine
from tartiflette.types.exceptions.tartiflette import GraphQLSchemaError


@pytest.fixture(scope="module")
async def ttftt_engine():
    schema_sdl = """
        enum Test {
            Value1
            Value2
            Value3
        }

        type Query {
            enumTest1: Test
            enumTest2: Test
            enumTest3: Test
        }

        directive @switchValue(oldValue: Test, newValue: Test) on ENUM | ENUM_VALUE

        extend enum Test @switchValue(oldValue: Value2, newValue: ExtendedValue5) {
            ExtendedValue4 @switchValue(newValue: EXTENDEDVALUE7)
            ExtendedValue5
            ExtendedValue6
            EXTENDEDVALUE7
        }

        enum anEnum {
            A
        }

        extend enum anEnum @switchValue
    """

    @Directive(name="switchValue", schema_name="test_issue_278_enum_extend")
    class SwitchValue:
        @staticmethod
        async def on_pre_output_coercion(
            directive_args: Dict[str, Any],
            next_directive: Callable,
            value: Any,
            ctx: Optional[Any],
            info: "ResolveInfo",
        ):
            value = await next_directive(value, ctx, info)
            if value == directive_args.get("oldValue"):
                return directive_args["newValue"]

            if not directive_args.get("oldValue"):
                return directive_args["newValue"]

            return value

    @Resolver("Query.enumTest1", schema_name="test_issue_278_enum_extend")
    async def resolver_enum_test_1(*args, **kwargs):
        return "Value2"

    @Resolver("Query.enumTest2", schema_name="test_issue_278_enum_extend")
    async def resolver_enum_test_2(*args, **kwargs):
        return "ExtendedValue4"

    @Resolver("Query.enumTest3", schema_name="test_issue_278_enum_extend")
    async def resolver_enum_test_3(*args, **kwargs):
        return "ExtendedValue6"

    return await create_engine(
        schema_sdl, schema_name="test_issue_278_enum_extend"
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
        query {
            __type(name: "Test") {
            name
            kind
            enumValues {
                name
            }
        } }
        """,
            {
                "data": {
                    "__type": {
                        "name": "Test",
                        "kind": "ENUM",
                        "enumValues": [
                            {"name": "Value1"},
                            {"name": "Value2"},
                            {"name": "Value3"},
                            {"name": "ExtendedValue4"},
                            {"name": "ExtendedValue5"},
                            {"name": "ExtendedValue6"},
                            {"name": "EXTENDEDVALUE7"},
                        ],
                    }
                }
            },
        ),
        (
            """
        query {
            enumTest1
        }""",
            {"data": {"enumTest1": "ExtendedValue5"}},
        ),
        (
            """
        query {
            enumTest2
        }""",
            {"data": {"enumTest2": "EXTENDEDVALUE7"}},
        ),
        (
            """
        query {
            enumTest3
        }""",
            {"data": {"enumTest3": "ExtendedValue6"}},
        ),
    ],
)
async def test_issue_278_enum_extend(query, expected, ttftt_engine):
    assert await ttftt_engine.execute(query) == expected


@pytest.mark.asyncio
async def test_issue_278_extend_enum_invalid_sdl():
    with pytest.raises(
        GraphQLSchemaError,
        match="""

0: Can't add < A > Value to < bob > ENUM, cause value already exists.
1: Can't add < A > Value to < bob > ENUM, cause value already exists.
2: Can't add < C > Directive to < bob > ENUM, cause it's already there.
3: Can't extend a non existing type < dontexists >.
4: Can't extend ENUM < aType > cause it's not an ENUM.""",
    ):
        await create_engine(
            sdl="""
                directive @C on ENUM

                enum bob @C {
                    A
                    B
                }

                extend enum bob @C {
                    A
                    A
                }

                type aType {
                    b: bob
                }

                type Query {
                    a: bob
                }

                extend enum dontexists @C

                extend enum aType {
                    D
                }
            """,
            schema_name="test_issue_278_invalid_sdl",
        )
