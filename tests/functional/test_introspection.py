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
                    {"kind": "OBJECT", "name": "CustomRootQuery"},
                    {"name": "CustomRootMutation", "kind": "OBJECT"},
                    {"kind": "OBJECT", "name": "CustomRootSubscription"},
                    {"kind": "SCALAR", "name": "Boolean"},
                    {"kind": "SCALAR", "name": "Date"},
                    {"name": "DateTime", "kind": "SCALAR"},
                    {"kind": "SCALAR", "name": "Float"},
                    {"name": "ID", "kind": "SCALAR"},
                    {"kind": "SCALAR", "name": "Int"},
                    {"kind": "SCALAR", "name": "String"},
                    {"kind": "SCALAR", "name": "Time"},
                ],
                "queryType": {"name": "CustomRootQuery"},
                "mutationType": {"name": "CustomRootMutation"},
                "directives": [
                    {
                        "args": [
                            {
                                "defaultValue": "Deprecated",
                                "name": "reason",
                                "type": {"name": "String", "kind": "SCALAR"},
                                "description": None,
                            }
                        ],
                        "locations": ["FIELD_DEFINITION", "ENUM_VALUE"],
                        "description": None,
                        "name": "deprecated",
                    },
                    {
                        "locations": ["FIELD_DEFINITION"],
                        "args": [],
                        "description": None,
                        "name": "non_introspectable",
                    },
                ],
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
                "subscriptionType": {"name": "CustomRootSubscription"},
                "mutationType": {"name": "CustomRootMutation"},
                "types": [
                    {"name": "CustomRootQuery", "kind": "OBJECT"},
                    {"name": "CustomRootMutation", "kind": "OBJECT"},
                    {"name": "CustomRootSubscription", "kind": "OBJECT"},
                    {"name": "Boolean", "kind": "SCALAR"},
                    {"name": "Float", "kind": "SCALAR"},
                    {"name": "ID", "kind": "SCALAR"},
                    {"name": "Int", "kind": "SCALAR"},
                    {"name": "String", "kind": "SCALAR"},
                    {"name": "Time", "kind": "SCALAR"},
                ],
                "directives": [
                    {
                        "name": "deprecated",
                        "args": [
                            {
                                "description": None,
                                "name": "reason",
                                "defaultValue": "Deprecated",
                                "type": {"kind": "SCALAR", "name": "String"},
                            }
                        ],
                        "description": None,
                        "locations": ["FIELD_DEFINITION", "ENUM_VALUE"],
                    },
                    {
                        "locations": ["FIELD_DEFINITION"],
                        "description": None,
                        "args": [],
                        "name": "non_introspectable",
                    },
                ],
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
                                "defaultValue": "Deprecated",
                                "type": {
                                    "name": "String",
                                    "ofType": None,
                                    "kind": "SCALAR",
                                },
                                "name": "reason",
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
