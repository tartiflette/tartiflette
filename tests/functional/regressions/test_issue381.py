import pytest

from tartiflette import Directive, Resolver, TypeResolver


def bakery(schema_name):
    @Directive(name="run_me_this_object", schema_name=schema_name)
    class RunMeThisObject:
        async def on_pre_output_coercion(
            self, directive_args, next_directive, value, ctx, info
        ):
            bob = await next_directive(value, ctx, info)
            return {"a": f"{bob['a']} obj"}

    @Directive(name="run_me_this_union", schema_name=schema_name)
    class RunMeThisUnion:
        async def on_pre_output_coercion(
            self, directive_args, next_directive, value, ctx, info
        ):
            bob = await next_directive(value, ctx, info)
            return {"a": f"{bob['a']} union"}

    @Directive(name="run_me_this_ifa", schema_name=schema_name)
    class RunMeThisIfa:
        async def on_pre_output_coercion(
            self, directive_args, next_directive, value, ctx, info
        ):
            bob = await next_directive(value, ctx, info)
            return {"a": f"{bob['a']} ifa"}

    @Resolver("Query.aFieldUnionObj", schema_name=schema_name)
    @Resolver("Query.aFieldObj", schema_name=schema_name)
    @Resolver("Query.aFieldIfa", schema_name=schema_name)
    @Resolver("Query.aFieldAnotherIfa", schema_name=schema_name)
    @Resolver("Query.aFieldIfaNoDir", schema_name=schema_name)
    async def resolve_root_query_field(pr, args, ctx, info):
        return {"a": "LOOOL"}

    @TypeResolver("CoupleOfResponses", schema_name=schema_name)
    @TypeResolver("CoupleOfResponsesNoUnionDir", schema_name=schema_name)
    def resolve_type_couple_of_responses(result, context, info, abstract_type):
        if "a" in result:
            return "ResponseOne"
        return "ResponseTwo"

    @TypeResolver("AnIfa", schema_name=schema_name)
    def resolve_type_an_ifa(result, context, info, abstract_type):
        return "ResponseThree"

    @TypeResolver("AnotherIfa", schema_name=schema_name)
    def resolve_type_another_ifa(result, context, info, abstract_type):
        return "ResponseFour"

    @TypeResolver("NoDirOnThisIface", schema_name=schema_name)
    def resolve_type_no_dir_on_this_iface(
        result, context, info, abstract_type
    ):
        return "ResponseFive"


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl="""
    schema {
        query: Query
    }

    directive @run_me_this_object on OBJECT
    directive @run_me_this_ifa on INTERFACE
    directive @run_me_this_union on UNION

    type Query {
        aFieldUnionObj: CoupleOfResponses
        aFieldObj: CoupleOfResponsesNoUnionDir
        aFieldIfa: AnIfa
        aFieldAnotherIfa: AnotherIfa
        aFieldIfaNoDir: NoDirOnThisIface
    }

    union CoupleOfResponses @run_me_this_union = ResponseOne | ResponseTwo
    union CoupleOfResponsesNoUnionDir = ResponseOne | ResponseTwo

    interface AnIfa @run_me_this_ifa {
        a: String
    }

    interface AnotherIfa @run_me_this_ifa {
        a: String
    }

    interface NoDirOnThisIface {
        a: String
    }

    type ResponseOne @run_me_this_object {
        a: String
    }

    type ResponseThree implements AnIfa {
        a: String
    }

    type ResponseFour implements AnotherIfa @run_me_this_object {
        a: String
    }

    type ResponseFive implements NoDirOnThisIface @run_me_this_object {
        a: String
    }

    type ResponseTwo {
        b: Int
    }
    """,
    bakery=bakery,
)
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
            query {
                aFieldUnionObj {
                    ...on ResponseOne {
                        a
                    }
                }
            }
            """,
            {"data": {"aFieldUnionObj": {"a": "LOOOL union obj"}}},
        ),
        (
            """
            query {
                aFieldObj {
                    ...on ResponseOne {
                        a
                    }
                }
            }
            """,
            {"data": {"aFieldObj": {"a": "LOOOL obj"}}},
        ),
        (
            """
            query {
                aFieldIfa {
                    ...on ResponseThree { a }
                }
            }
            """,
            {"data": {"aFieldIfa": {"a": "LOOOL ifa"}}},
        ),
        (
            """
            query {
                aFieldAnotherIfa {
                    ...on ResponseFour { a }
                }
            }
            """,
            {"data": {"aFieldAnotherIfa": {"a": "LOOOL ifa obj"}}},
        ),
        (
            """
            query {
                aFieldIfaNoDir {
                    ...on ResponseFive { a }
                }
            }
            """,
            {"data": {"aFieldIfaNoDir": {"a": "LOOOL obj"}}},
        ),
    ],
)
async def test_issue381_output_coercion_on_union(
    schema_stack, query, expected
):
    assert await schema_stack.execute(query) == expected
