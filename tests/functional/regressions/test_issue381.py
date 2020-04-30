import pytest

from tartiflette import Directive, Resolver, TypeResolver, create_engine

_SDL = """ schema {
  query: Query
}

directive @run_me_this on OBJECT

type Query {
  rootQueryField(resp: Int): CoupleOfResponses
}

union CoupleOfResponses = ResponseOne | ResponseTwo

type ResponseOne @run_me_this {
    a: String
}


type ResponseTwo {
   b: Int
}
"""


@Directive(name="run_me_this", schema_name="test_issue381")
class RunMeThis:
    async def on_pre_output_coercion(
        self, directive_args, next_directive, value, ctx, info
    ):
        bob = await next_directive(value, ctx, info)
        return {"a": f"{bob['a']} 2"}


@Resolver("Query.rootQueryField", schema_name="test_issue381")
async def resolve_root_query_field(pr, args, ctx, info):
    return {"a": "LOOOL "}


@TypeResolver("CoupleOfResponses", schema_name="test_issue381")
def resolve_type_couple_of_responses(result, context, info, abstract_type):
    if "a" in result:
        return "ResponseOne"
    return "ResponseTwo"


@pytest.mark.asyncio
async def test_issue381_output_coercion_on_union():
    e = await create_engine(sdl=_SDL, schema_name="test_issue381")
    assert (
        await e.execute(
            """
query {
    rootQueryField(resp: 1) {
        ...on ResponseOne {
            a
        }
        ...on ResponseTwo {
            b
        }
    }
}
"""
        )
        == {"data": {"rootQueryField": {"a": "LOOOL  2"}}}
    )
