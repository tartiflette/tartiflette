import pytest

from tartiflette import Resolver
from tartiflette.tartiflette import Tartiflette


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'sdl_type, returnval, expected', [
        (
                "String",
                "Something",
                {"data": {"obj": {"field": "Something"}}},
        ),
        (
                "String!",
                None,
                {"data": {"obj": None},
                 "errors": [
                     {
                         "locations": [{"column": 64, "line": 1}],
                         "message": "Invalid value (value: None) for field "
                                    "`field` of type `String!`",
                         "path": ["obj", "field"],
                     },
                 ]},
        ),
        (
                "[String]",
                ["Before", None, "After"],
                {"data": {"obj": {"field": ["Before", None, "After"]}}},
        ),
        (
                "[String!]",
                ["Before", None, "After"],
                {"data": {"obj": {"field": None}}, "errors": [
                    {
                        "locations": [{"column": 64, "line": 1}],
                        "message": "Invalid value (value: None) for field "
                                   "`field` of type `[String!]`",
                        "path": ["obj", "field", 1],
                    },
                ]},
        ),
        (
                "[String]!",
                None,
                {"data": {"obj": None},
                 "errors": [
                     {
                         "locations": [{"column": 64, "line": 1}],
                         "message": "Invalid value (value: None) for field "
                                    "`field` of type `[String]!`",
                         "path": ["obj", "field"],
                     },
                 ]},
        ),
        (
                "[String!]!",
                ["Before", None, "After"],
                {"data": {"obj": None},
                 "errors": [
                     {
                         "locations": [{"column": 64, "line": 1}],
                         "message": "Invalid value (value: ['Before', None, 'After']) "
                                    "for field `field` of type `[String!]!`",
                         "path": ["obj", "field"],
                     },
                 ]},
        ),
        (
                "[String!]!",
                None,
                {"data": {"obj": None},
                 "errors": [
                     {
                         "locations": [{"column": 64, "line": 1}],
                         "message": "Invalid value (value: None) "
                                    "for field `field` of type `[String!]!`",
                         "path": ["obj", "field"],
                     },
                 ]},
        ),
        (
                "[[String]]",
                [["Nobody", "Expects"], ["The", "Spanish", "Inquisition"]],
                {"data": {"obj": {"field": [["Nobody", "Expects"],
                                            ["The", "Spanish",
                                             "Inquisition"]]}}},
        ),
        # TODO: move below test to a coercion test
        # (it doesn't really test empty values)
        (
                "[[String]]",
                [42, None, ["The", "Spanish", "Inquisition"]],
                {"data": {"obj": {"field": [['42'], None,
                                            ["The", "Spanish",
                                             "Inquisition"]]}}},
        ),
        (
                "[[String!]]",
                [["Nobody", "Expects"], ["The", "Spanish"],
                 [None, "Inquisition"]],
                {"data": {
                    "obj": {"field": [['Nobody', 'Expects'], ["The", "Spanish"],
                                      None]}},
                    "errors": [
                        {
                            "locations": [{"column": 64, "line": 1}],
                            "message": "Invalid value (value: None) "
                                       "for field `field` of type `[[String!]]`",
                            "path": ["obj", "field", 2, 0],
                        },
                    ]},
        ),
        (  # Test #10
                "[[String!]!]",
                [["Nobody", "Expects"], ["The", "Spanish"],
                 [None, "Inquisition"]],
                {"data": {"obj": {"field": None}},
                 "errors": [
                     {
                         "locations": [{"column": 64, "line": 1}],
                         "message": "Invalid value "
                                    "(value: [None, 'Inquisition']) "
                                    "for field `field` of type `[[String!]!]`",
                         "path": ["obj", "field", 2],
                     },
                 ]},
        ),
        (
                "[[String!]!]!",
                [["Nobody", "Expects"], ["The", "Spanish"],
                 [None, "Inquisition"]],
                {"data": {
                    "obj": None},
                    "errors": [
                        {
                            "locations": [{"column": 64, "line": 1}],
                            "message": "Invalid value (value: "
                                       "[['Nobody', 'Expects'], "
                                       "['The', 'Spanish'], "
                                       "[None, 'Inquisition']]) "
                                       "for field `field` of type `[[String!]!]!`",
                            "path": ["obj", "field"],
                        },
                    ]},
        ),
    ])
async def test_tartiflette_execute_simple_empty_value(sdl_type, returnval,
                                                      expected):
    schema_sdl = """
    type Obj {{
        field: {sdl_type}
    }}

    type Query {{
        obj: Obj
    }}
    """.format(sdl_type=sdl_type)

    ttftt = Tartiflette(schema_sdl)

    @Resolver("Obj.field", schema=ttftt.schema)
    async def func_field_scalar_resolver(*args, **kwargs):
        return returnval

    ttftt.schema.bake()
    result = await ttftt.execute("""
    query TestExecutionEmptyValues{
        obj {
            field
        }
    }
    """)

    assert expected == result


@pytest.mark.asyncio
async def test_tartiflette_execute_bubble_up_empty_value():
    schema_sdl = """
        type SubObj {
            fieldAgain: Int!
        }
    
        type Obj {
            field: SubObj!
        }

        type Query {
            obj: Obj!
        }
        """

    ttftt = Tartiflette(schema_sdl)

    @Resolver("SubObj.fieldAgain", schema=ttftt.schema)
    async def func_field_scalar_resolver(*args, **kwargs):
        return None

    ttftt.schema.bake()
    result = await ttftt.execute("""
        query TestExecutionEmptyValues{
            obj {
                field {
                    fieldAgain
                }
            }
        }
        """)

    assert result == {
        "data": None,
        "errors": [
            {
                "locations": [{"column": 104, "line": 1}],
                "message": "Invalid value (value: None) "
                           "for field `fieldAgain` of type `Int!`",
                "path": ["obj", "field", "fieldAgain"],
            },
        ]}
