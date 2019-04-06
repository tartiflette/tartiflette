import pytest

from tartiflette import Engine, Resolver


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
    """,
        operation_name="Test",
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
    """,
        operation_name="Test",
    )
    assert {
        "data": {
            "__schema": {
                "subscriptionType": {"name": "CustomRootSubscription"},
                "types": [
                    {"name": "CustomRootQuery", "kind": "OBJECT"},
                    {"kind": "OBJECT", "name": "CustomRootMutation"},
                    {"name": "CustomRootSubscription", "kind": "OBJECT"},
                    {"name": "Boolean", "kind": "SCALAR"},
                    {"name": "Date", "kind": "SCALAR"},
                    {"name": "DateTime", "kind": "SCALAR"},
                    {"kind": "SCALAR", "name": "Float"},
                    {"kind": "SCALAR", "name": "ID"},
                    {"kind": "SCALAR", "name": "Int"},
                    {"kind": "SCALAR", "name": "String"},
                    {"name": "Time", "kind": "SCALAR"},
                ],
                "directives": [
                    {
                        "description": None,
                        "locations": ["FIELD_DEFINITION", "ENUM_VALUE"],
                        "name": "deprecated",
                        "args": [
                            {
                                "name": "reason",
                                "defaultValue": "Deprecated",
                                "type": {"name": "String", "kind": "SCALAR"},
                                "description": None,
                            }
                        ],
                    },
                    {
                        "locations": ["FIELD_DEFINITION"],
                        "args": [],
                        "name": "non_introspectable",
                        "description": None,
                    },
                    {
                        "name": "skip",
                        "locations": [
                            "FIELD",
                            "FRAGMENT_SPREAD",
                            "INLINE_FRAGMENT",
                        ],
                        "args": [
                            {
                                "defaultValue": None,
                                "type": {"name": None, "kind": "NON_NULL"},
                                "name": "if",
                                "description": None,
                            }
                        ],
                        "description": None,
                    },
                    {
                        "name": "include",
                        "locations": [
                            "FIELD",
                            "FRAGMENT_SPREAD",
                            "INLINE_FRAGMENT",
                        ],
                        "description": None,
                        "args": [
                            {
                                "name": "if",
                                "type": {"name": None, "kind": "NON_NULL"},
                                "description": None,
                                "defaultValue": None,
                            }
                        ],
                    },
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
    """,
        operation_name="Test",
    )
    assert {
        "data": {
            "__schema": {
                "mutationType": {"name": "CustomRootMutation"},
                "directives": [
                    {
                        "locations": ["FIELD_DEFINITION", "ENUM_VALUE"],
                        "args": [
                            {
                                "name": "reason",
                                "defaultValue": "Deprecated",
                                "description": None,
                                "type": {"kind": "SCALAR", "name": "String"},
                            }
                        ],
                        "name": "deprecated",
                        "description": None,
                    },
                    {
                        "name": "non_introspectable",
                        "description": None,
                        "args": [],
                        "locations": ["FIELD_DEFINITION"],
                    },
                    {
                        "locations": [
                            "FIELD",
                            "FRAGMENT_SPREAD",
                            "INLINE_FRAGMENT",
                        ],
                        "description": None,
                        "name": "skip",
                        "args": [
                            {
                                "description": None,
                                "type": {"kind": "NON_NULL", "name": None},
                                "defaultValue": None,
                                "name": "if",
                            }
                        ],
                    },
                    {
                        "args": [
                            {
                                "type": {"kind": "NON_NULL", "name": None},
                                "defaultValue": None,
                                "description": None,
                                "name": "if",
                            }
                        ],
                        "locations": [
                            "FIELD",
                            "FRAGMENT_SPREAD",
                            "INLINE_FRAGMENT",
                        ],
                        "name": "include",
                        "description": None,
                    },
                ],
                "types": [
                    {"kind": "OBJECT", "name": "CustomRootQuery"},
                    {"name": "CustomRootMutation", "kind": "OBJECT"},
                    {"kind": "OBJECT", "name": "CustomRootSubscription"},
                    {"kind": "SCALAR", "name": "Boolean"},
                    {"name": "Float", "kind": "SCALAR"},
                    {"kind": "SCALAR", "name": "ID"},
                    {"kind": "SCALAR", "name": "Int"},
                    {"name": "String", "kind": "SCALAR"},
                    {"name": "Time", "kind": "SCALAR"},
                ],
                "subscriptionType": {"name": "CustomRootSubscription"},
                "queryType": {"name": "CustomRootQuery"},
            }
        }
    } == result


@pytest.mark.asyncio
async def test_tartiflette_execute_schema_introspection_output_introspecting_args(
    clean_registry
):
    schema_sdl = """
    type lol {
        GGG: String
        GG(a: String!): String
        G(a: [String!]!): String!
    }

    type Query {
        a: lol
    }
    """

    ttftt = Engine(schema_sdl, exclude_builtins_scalars=["Date", "DateTime"])
    result = await ttftt.execute(
        """
    query IntrospectionQuery {
  __schema {
    queryType {
      name
    }
    mutationType {
      name
    }
    subscriptionType {
      name
    }
    types {
      ...FullType
    }
    directives {
      name
      locations
      args {
        ...InputValue
      }
    }
  }
}

fragment FullType on __Type {
  kind
  name
  fields(includeDeprecated: true) {
    name
    args {
      ...InputValue
    }
    type {
      ...TypeRef
    }
    isDeprecated
    deprecationReason
  }
  inputFields {
    ...InputValue
  }
  interfaces {
    ...TypeRef
  }
  enumValues(includeDeprecated: true) {
    name
    isDeprecated
    deprecationReason
  }
  possibleTypes {
    ...TypeRef
  }
}

fragment InputValue on __InputValue {
  name
  type {
    ...TypeRef
  }
  defaultValue
}

fragment TypeRef on __Type {
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
    """,
        operation_name="IntrospectionQuery",
    )

    assert {
        "data": {
            "__schema": {
                "queryType": {"name": "Query"},
                "directives": [
                    {
                        "args": [
                            {
                                "type": {
                                    "ofType": None,
                                    "name": "String",
                                    "kind": "SCALAR",
                                },
                                "name": "reason",
                                "defaultValue": "Deprecated",
                            }
                        ],
                        "name": "deprecated",
                        "locations": ["FIELD_DEFINITION", "ENUM_VALUE"],
                    },
                    {
                        "name": "non_introspectable",
                        "locations": ["FIELD_DEFINITION"],
                        "args": [],
                    },
                    {
                        "locations": [
                            "FIELD",
                            "FRAGMENT_SPREAD",
                            "INLINE_FRAGMENT",
                        ],
                        "args": [
                            {
                                "name": "if",
                                "defaultValue": None,
                                "type": {
                                    "name": None,
                                    "kind": "NON_NULL",
                                    "ofType": {
                                        "ofType": None,
                                        "kind": "SCALAR",
                                        "name": "Boolean",
                                    },
                                },
                            }
                        ],
                        "name": "skip",
                    },
                    {
                        "name": "include",
                        "locations": [
                            "FIELD",
                            "FRAGMENT_SPREAD",
                            "INLINE_FRAGMENT",
                        ],
                        "args": [
                            {
                                "defaultValue": None,
                                "type": {
                                    "ofType": {
                                        "ofType": None,
                                        "name": "Boolean",
                                        "kind": "SCALAR",
                                    },
                                    "name": None,
                                    "kind": "NON_NULL",
                                },
                                "name": "if",
                            }
                        ],
                    },
                ],
                "types": [
                    {
                        "kind": "OBJECT",
                        "name": "lol",
                        "enumValues": None,
                        "possibleTypes": None,
                        "interfaces": [],
                        "fields": [
                            {
                                "isDeprecated": False,
                                "deprecationReason": None,
                                "name": "GGG",
                                "args": [],
                                "type": {
                                    "name": "String",
                                    "kind": "SCALAR",
                                    "ofType": None,
                                },
                            },
                            {
                                "deprecationReason": None,
                                "name": "GG",
                                "args": [
                                    {
                                        "name": "a",
                                        "defaultValue": None,
                                        "type": {
                                            "kind": "NON_NULL",
                                            "ofType": {
                                                "kind": "SCALAR",
                                                "ofType": None,
                                                "name": "String",
                                            },
                                            "name": None,
                                        },
                                    }
                                ],
                                "type": {
                                    "ofType": None,
                                    "name": "String",
                                    "kind": "SCALAR",
                                },
                                "isDeprecated": False,
                            },
                            {
                                "name": "G",
                                "args": [
                                    {
                                        "defaultValue": None,
                                        "type": {
                                            "name": None,
                                            "kind": "NON_NULL",
                                            "ofType": {
                                                "name": None,
                                                "ofType": {
                                                    "kind": "NON_NULL",
                                                    "ofType": {
                                                        "kind": "SCALAR",
                                                        "name": "String",
                                                        "ofType": None,
                                                    },
                                                    "name": None,
                                                },
                                                "kind": "LIST",
                                            },
                                        },
                                        "name": "a",
                                    }
                                ],
                                "type": {
                                    "name": None,
                                    "kind": "NON_NULL",
                                    "ofType": {
                                        "ofType": None,
                                        "name": "String",
                                        "kind": "SCALAR",
                                    },
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                        ],
                        "inputFields": None,
                    },
                    {
                        "kind": "OBJECT",
                        "fields": [
                            {
                                "type": {
                                    "kind": "OBJECT",
                                    "ofType": None,
                                    "name": "lol",
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                                "args": [],
                                "name": "a",
                            }
                        ],
                        "name": "Query",
                        "possibleTypes": None,
                        "enumValues": None,
                        "interfaces": [],
                        "inputFields": None,
                    },
                    {
                        "kind": "SCALAR",
                        "interfaces": None,
                        "fields": None,
                        "inputFields": None,
                        "possibleTypes": None,
                        "enumValues": None,
                        "name": "Boolean",
                    },
                    {
                        "name": "Float",
                        "possibleTypes": None,
                        "inputFields": None,
                        "kind": "SCALAR",
                        "enumValues": None,
                        "interfaces": None,
                        "fields": None,
                    },
                    {
                        "enumValues": None,
                        "name": "ID",
                        "inputFields": None,
                        "interfaces": None,
                        "possibleTypes": None,
                        "fields": None,
                        "kind": "SCALAR",
                    },
                    {
                        "inputFields": None,
                        "kind": "SCALAR",
                        "possibleTypes": None,
                        "name": "Int",
                        "interfaces": None,
                        "enumValues": None,
                        "fields": None,
                    },
                    {
                        "name": "String",
                        "possibleTypes": None,
                        "fields": None,
                        "interfaces": None,
                        "kind": "SCALAR",
                        "enumValues": None,
                        "inputFields": None,
                    },
                    {
                        "inputFields": None,
                        "name": "Time",
                        "kind": "SCALAR",
                        "enumValues": None,
                        "interfaces": None,
                        "fields": None,
                        "possibleTypes": None,
                    },
                ],
                "mutationType": None,
                "subscriptionType": None,
            }
        }
    } == result
