import pytest

from tartiflette import Resolver
from tartiflette.engine import Engine


@pytest.mark.asyncio
async def test_tartiflette_execute_basic_type_introspection_output(
    clean_registry
):
    schema_sdl = """
    \"\"\"This is the description\"\"\"
    type Test {
        field1: String
        field2(arg1: Int = 42): Int
        field3: [EnumStatus!]
    }

    enum EnumStatus {
        Active
        Inactive
    }

    type Query {
        objectTest: Test
    }
    """

    ttftt = Engine(schema_sdl)

    result = await ttftt.execute(
        """
    query Test{
        __type(name: "Test") {
            name
            kind
            description
            fields {
                name
                args {
                    name
                    description
                    type {
                        kind
                        name
                        ofType {
                            kind
                            name
                            ofType {
                                kind
                                name
                                ofType {
                                    kind
                                    name
                                    ofType {
                                        kind
                                        name
                                        ofType {
                                            kind
                                            name
                                        }
                                    }
                                }
                            }
                        }
                    }
                    defaultValue
                }
                type {
                    kind
                    name
                    ofType {
                        kind
                        name
                        ofType {
                            kind
                            name
                            ofType {
                                kind
                                name
                                ofType {
                                    kind
                                    name
                                    ofType {
                                        kind
                                        name
                                        ofType {
                                            kind
                                            name
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    """
    )

    assert {
        "data": {
            "__type": {
                "name": "Test",
                "kind": "OBJECT",
                "description": "This is the description",
                "fields": [
                    {
                        "name": "field1",
                        "args": [],
                        "type": {
                            "kind": "SCALAR",
                            "name": "String",
                            "ofType": None,
                        },
                    },
                    {
                        "name": "field2",
                        "args": [
                            {
                                "name": "arg1",
                                "description": None,
                                "type": {
                                    "kind": "SCALAR",
                                    "name": "Int",
                                    "ofType": None,
                                },
                                "defaultValue": "42",
                            }
                        ],
                        "type": {
                            "kind": "SCALAR",
                            "name": "Int",
                            "ofType": None,
                        },
                    },
                    {
                        "name": "field3",
                        "args": [],
                        "type": {
                            "kind": "LIST",
                            "name": None,
                            "ofType": {
                                "kind": "NON_NULL",
                                "name": None,
                                "ofType": {
                                    "kind": "ENUM",
                                    "name": "EnumStatus",
                                    "ofType": None,
                                },
                            },
                        },
                    },
                    {
                        "name": "__typename",
                        "args": [],
                        "type": {
                            "kind": "NON_NULL",
                            "name": None,
                            "ofType": {
                                "kind": "SCALAR",
                                "name": "String",
                                "ofType": None,
                            },
                        },
                    },
                ],
            }
        }
    } == result


@pytest.mark.asyncio
async def test_tartiflette_execute_schema_introspection_output(clean_registry):
    schema_sdl = """
    schema {
        query: CustomRootQuery
        mutation: CustomRootMutation
        subscription: CustomRootSubscription
    }

    type CustomRootQuery {
        test: String
    }

    type CustomRootMutation {
        test: Int
    }

    type CustomRootSubscription {
        test: String
    }
    """

    ttftt = Engine(schema_sdl)

    result = await ttftt.execute(
        """
    query Test{
        __schema {
            queryType { name }
            mutationType { name }
            subscriptionType { name }
            types {
                kind
                name
            }
            directives {
                name
                description
                locations
                args {
                    name
                    description
                    type {
                        kind
                        name
                    }
                    defaultValue
                }
            }
        }
    }
    """
    )

    assert {
        "data": {
            "__schema": {
                "subscriptionType": {"name": "CustomRootSubscription"},
                "directives": [
                    {
                        "name": "deprecated",
                        "args": [
                            {
                                "description": None,
                                "name": "reason",
                                "defaultValue": "No longer supported",
                                "type": {"kind": None, "name": "String"},
                            }
                        ],
                        "locations": ["FIELD_DEFINITION", "ENUM_VALUE"],
                        "description": None,
                    },
                    {
                        "description": None,
                        "locations": ["FIELD_DEFINITION"],
                        "name": "non_introspectable",
                        "args": [],
                    },
                ],
                "types": [
                    {"kind": "OBJECT", "name": "CustomRootQuery"},
                    {"name": "CustomRootMutation", "kind": "OBJECT"},
                    {"kind": "OBJECT", "name": "CustomRootSubscription"},
                    {"name": "Boolean", "kind": "SCALAR"},
                    {"name": "Date", "kind": "SCALAR"},
                    {"name": "DateTime", "kind": "SCALAR"},
                    {"kind": "SCALAR", "name": "Float"},
                    {"kind": "SCALAR", "name": "ID"},
                    {"kind": "SCALAR", "name": "Int"},
                    {"name": "String", "kind": "SCALAR"},
                    {"kind": "SCALAR", "name": "Time"},
                    {"kind": "OBJECT", "name": "__Schema"},
                    {"name": "__Type", "kind": "OBJECT"},
                    {"name": "__Field", "kind": "OBJECT"},
                    {"name": "__InputValue", "kind": "OBJECT"},
                    {"name": "__EnumValue", "kind": "OBJECT"},
                    {"name": "__TypeKind", "kind": "ENUM"},
                    {"kind": "OBJECT", "name": "__Directive"},
                    {"name": "__DirectiveLocation", "kind": "ENUM"},
                ],
                "mutationType": {"name": "CustomRootMutation"},
                "queryType": {"name": "CustomRootQuery"},
            }
        }
    } == result


@pytest.mark.asyncio
async def test_tartiflette_execute_schema_introspection_output_exclude_scalars(
    clean_registry
):
    schema_sdl = """
    schema {
        query: CustomRootQuery
        mutation: CustomRootMutation
        subscription: CustomRootSubscription
    }

    type CustomRootQuery {
        test: String
    }

    type CustomRootMutation {
        test: Int
    }

    type CustomRootSubscription {
        test: String
    }
    """

    ttftt = Engine(schema_sdl, exclude_builtins_scalars=["Date", "DateTime"])
    result = await ttftt.execute(
        """
    query Test{
        __schema {
            queryType { name }
            mutationType { name }
            subscriptionType { name }
            types {
                kind
                name
            }
            directives {
                name
                description
                locations
                args {
                    name
                    description
                    type {
                        kind
                        name
                    }
                    defaultValue
                }
            }
        }
    }
    """
    )

    assert {
        "data": {
            "__schema": {
                "types": [
                    {"name": "CustomRootQuery", "kind": "OBJECT"},
                    {"kind": "OBJECT", "name": "CustomRootMutation"},
                    {"kind": "OBJECT", "name": "CustomRootSubscription"},
                    {"kind": "SCALAR", "name": "Boolean"},
                    {"kind": "SCALAR", "name": "Float"},
                    {"name": "ID", "kind": "SCALAR"},
                    {"kind": "SCALAR", "name": "Int"},
                    {"kind": "SCALAR", "name": "String"},
                    {"kind": "SCALAR", "name": "Time"},
                    {"name": "__Schema", "kind": "OBJECT"},
                    {"name": "__Type", "kind": "OBJECT"},
                    {"kind": "OBJECT", "name": "__Field"},
                    {"name": "__InputValue", "kind": "OBJECT"},
                    {"kind": "OBJECT", "name": "__EnumValue"},
                    {"name": "__TypeKind", "kind": "ENUM"},
                    {"name": "__Directive", "kind": "OBJECT"},
                    {"name": "__DirectiveLocation", "kind": "ENUM"},
                ],
                "directives": [
                    {
                        "name": "deprecated",
                        "description": None,
                        "args": [
                            {
                                "type": {"kind": None, "name": "String"},
                                "name": "reason",
                                "description": None,
                                "defaultValue": "No longer supported",
                            }
                        ],
                        "locations": ["FIELD_DEFINITION", "ENUM_VALUE"],
                    },
                    {
                        "description": None,
                        "name": "non_introspectable",
                        "locations": ["FIELD_DEFINITION"],
                        "args": [],
                    },
                ],
                "subscriptionType": {"name": "CustomRootSubscription"},
                "queryType": {"name": "CustomRootQuery"},
                "mutationType": {"name": "CustomRootMutation"},
            }
        }
    } == result
