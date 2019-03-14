import pytest

from tartiflette.directive import CommonDirective, Directive
from tartiflette.engine import Engine
from tartiflette.types.exceptions.tartiflette import GraphQLSchemaError


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "sdl,should_exp, adddir",
    [
        (
            """type aType { a(lol: Int!): String } type Query { aa: aType }""",
            False,
            False,
        ),
        (
            """type aType { a(lol: Int!): String } type Query { aa(bb: aType): aType }""",
            True,
            False,
        ),
        (
            """enum AnEnum { ALOL } type aType { a(lol: Int!): String } input AnInputType { a: String } type Mutation { aa(a: String, b:AnEnum, c:AnInputType!): aType } type Query { aa: aType }""",
            False,
            False,
        ),
        (
            """enum AnEnum { ALOL } type aType { a(lol: Int!): String } type AnInputType { a: String } type Mutation { aa(a: String, b:AnEnum, c:AnInputType!): aType } type Query { aa: aType }""",
            True,
            False,
        ),
        (
            """enum AnEnum { ALOL } type aType { a(lol: Int!): String } type AnInputType { a: String } type Mutation { aa(a: String, b:AnEnum, c:String!): aType } type Query { aa: aType } directive @adirective(a: String, b:AnEnum, c:AnInputType!) on FIELD_DEFINITION""",
            True,
            True,
        ),
        (
            """enum AnEnum { ALOL } type aType { a(lol: Int!): String } input AnInputType { a: String } type Mutation { aa(a: String, b:AnEnum, c:AnInputType!): aType } type Query { aa: aType } directive @adirective(a: String, b:AnEnum, c:AnInputType!) on FIELD_DEFINITION""",
            False,
            True,
        ),
    ],
)
async def test_issue154(sdl, should_exp, adddir):
    class aDirective(CommonDirective):
        pass

    if adddir:
        Directive("adirective", schema_name=f"issue154_{sdl}")(aDirective)

    if should_exp:
        with pytest.raises(GraphQLSchemaError):
            Engine(sdl=sdl, schema_name=f"issue154_{sdl}")
    else:
        e = Engine(sdl=sdl, schema_name=f"issue154_{sdl}")
        assert e._schema is not None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "sdl,should_exp",
    [
        (
            """type aType { a(lol: Int!): String } type Query { aa: aType } input AnotherInput { a:String } input anInType { a:String b:Int g:AnotherInput } """,
            False,
        ),
        (
            """type aType { a(lol: Int!): String } type Query { aa: aType } input anInType { a:String b:Int g:aType }""",
            True,
        ),
    ],
)
async def test_issue154_input_type(sdl, should_exp):
    if should_exp:
        with pytest.raises(GraphQLSchemaError):
            Engine(sdl=sdl, schema_name=f"issue154_{sdl}")
    else:
        e = Engine(sdl=sdl, schema_name=f"issue154_{sdl}")
        assert e._schema is not None
