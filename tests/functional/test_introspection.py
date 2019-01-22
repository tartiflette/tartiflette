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
    """
    )

    assert {
        "data": {
            "__schema": {
                "queryType": {"name": "Query"},
                "subscriptionType": None,
                "directives": [
                    {
                        "name": "deprecated",
                        "locations": ["FIELD_DEFINITION", "ENUM_VALUE"],
                        "args": [
                            {
                                "defaultValue": "No longer supported",
                                "name": "reason",
                                "type": {
                                    "kind": None,
                                    "name": None,
                                    "ofType": None,
                                },
                            }
                        ],
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
                        "fields": [
                            {
                                "args": [],
                                "type": {
                                    "kind": "SCALAR",
                                    "ofType": None,
                                    "name": "String",
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                                "name": "GGG",
                            },
                            {
                                "type": {
                                    "name": "String",
                                    "kind": "SCALAR",
                                    "ofType": None,
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                                "name": "GG",
                                "args": [
                                    {
                                        "type": {
                                            "ofType": {
                                                "kind": "SCALAR",
                                                "ofType": None,
                                                "name": "String",
                                            },
                                            "name": None,
                                            "kind": "NON_NULL",
                                        },
                                        "name": "a",
                                        "defaultValue": None,
                                    }
                                ],
                            },
                            {
                                "type": {
                                    "kind": "NON_NULL",
                                    "ofType": {
                                        "name": "String",
                                        "kind": "SCALAR",
                                        "ofType": None,
                                    },
                                    "name": None,
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                                "name": "G",
                                "args": [
                                    {
                                        "defaultValue": None,
                                        "type": {
                                            "ofType": {
                                                "kind": "LIST",
                                                "ofType": {
                                                    "name": None,
                                                    "kind": "NON_NULL",
                                                    "ofType": {
                                                        "kind": "SCALAR",
                                                        "ofType": None,
                                                        "name": "String",
                                                    },
                                                },
                                                "name": None,
                                            },
                                            "name": None,
                                            "kind": "NON_NULL",
                                        },
                                        "name": "a",
                                    }
                                ],
                            },
                            {
                                "isDeprecated": False,
                                "deprecationReason": None,
                                "name": "__typename",
                                "args": [],
                                "type": {
                                    "kind": "NON_NULL",
                                    "ofType": {
                                        "name": "String",
                                        "kind": "SCALAR",
                                        "ofType": None,
                                    },
                                    "name": None,
                                },
                            },
                        ],
                        "inputFields": None,
                        "interfaces": [],
                        "enumValues": None,
                        "possibleTypes": None,
                    },
                    {
                        "kind": "OBJECT",
                        "name": "Query",
                        "fields": [
                            {
                                "name": "a",
                                "args": [],
                                "type": {
                                    "name": "lol",
                                    "kind": "OBJECT",
                                    "ofType": None,
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "args": [],
                                "type": {
                                    "kind": "NON_NULL",
                                    "ofType": {
                                        "name": "__Schema",
                                        "kind": "OBJECT",
                                        "ofType": None,
                                    },
                                    "name": None,
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                                "name": "__schema",
                            },
                            {
                                "type": {
                                    "name": "__Type",
                                    "kind": "OBJECT",
                                    "ofType": None,
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                                "name": "__type",
                                "args": [
                                    {
                                        "defaultValue": None,
                                        "type": {
                                            "name": None,
                                            "kind": "NON_NULL",
                                            "ofType": None,
                                        },
                                        "name": "name",
                                    }
                                ],
                            },
                            {
                                "isDeprecated": False,
                                "deprecationReason": None,
                                "name": "__typename",
                                "args": [],
                                "type": {
                                    "name": None,
                                    "kind": "NON_NULL",
                                    "ofType": {
                                        "name": "String",
                                        "ofType": None,
                                        "kind": "SCALAR",
                                    },
                                },
                            },
                        ],
                        "inputFields": None,
                        "interfaces": [],
                        "enumValues": None,
                        "possibleTypes": None,
                    },
                    {
                        "kind": "SCALAR",
                        "name": "Boolean",
                        "fields": None,
                        "inputFields": None,
                        "interfaces": None,
                        "enumValues": None,
                        "possibleTypes": None,
                    },
                    {
                        "kind": "SCALAR",
                        "name": "Float",
                        "fields": None,
                        "inputFields": None,
                        "interfaces": None,
                        "enumValues": None,
                        "possibleTypes": None,
                    },
                    {
                        "kind": "SCALAR",
                        "name": "ID",
                        "fields": None,
                        "inputFields": None,
                        "interfaces": None,
                        "enumValues": None,
                        "possibleTypes": None,
                    },
                    {
                        "interfaces": None,
                        "enumValues": None,
                        "possibleTypes": None,
                        "kind": "SCALAR",
                        "name": "Int",
                        "fields": None,
                        "inputFields": None,
                    },
                    {
                        "kind": "SCALAR",
                        "name": "String",
                        "fields": None,
                        "inputFields": None,
                        "interfaces": None,
                        "enumValues": None,
                        "possibleTypes": None,
                    },
                    {
                        "kind": "SCALAR",
                        "name": "Time",
                        "fields": None,
                        "inputFields": None,
                        "interfaces": None,
                        "enumValues": None,
                        "possibleTypes": None,
                    },
                    {
                        "kind": "OBJECT",
                        "name": "__Schema",
                        "fields": [
                            {
                                "name": "types",
                                "args": [],
                                "type": {
                                    "ofType": {
                                        "kind": "LIST",
                                        "ofType": {
                                            "name": None,
                                            "kind": "NON_NULL",
                                            "ofType": {
                                                "kind": "OBJECT",
                                                "ofType": None,
                                                "name": "__Type",
                                            },
                                        },
                                        "name": None,
                                    },
                                    "name": None,
                                    "kind": "NON_NULL",
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "deprecationReason": None,
                                "name": "queryType",
                                "args": [],
                                "type": {
                                    "ofType": {
                                        "name": "__Type",
                                        "kind": "OBJECT",
                                        "ofType": None,
                                    },
                                    "name": None,
                                    "kind": "NON_NULL",
                                },
                                "isDeprecated": False,
                            },
                            {
                                "name": "mutationType",
                                "args": [],
                                "type": {
                                    "kind": "OBJECT",
                                    "ofType": None,
                                    "name": "__Type",
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "subscriptionType",
                                "args": [],
                                "type": {
                                    "kind": "OBJECT",
                                    "ofType": None,
                                    "name": "__Type",
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "directives",
                                "args": [],
                                "type": {
                                    "name": None,
                                    "kind": "NON_NULL",
                                    "ofType": {
                                        "ofType": {
                                            "name": None,
                                            "ofType": {
                                                "name": "__Directive",
                                                "kind": "OBJECT",
                                                "ofType": None,
                                            },
                                            "kind": "NON_NULL",
                                        },
                                        "name": None,
                                        "kind": "LIST",
                                    },
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "__typename",
                                "args": [],
                                "type": {
                                    "name": None,
                                    "kind": "NON_NULL",
                                    "ofType": {
                                        "ofType": None,
                                        "kind": "SCALAR",
                                        "name": "String",
                                    },
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                        ],
                        "inputFields": None,
                        "interfaces": [],
                        "enumValues": None,
                        "possibleTypes": None,
                    },
                    {
                        "kind": "OBJECT",
                        "name": "__Type",
                        "fields": [
                            {
                                "name": "kind",
                                "args": [],
                                "type": {
                                    "ofType": None,
                                    "name": "__TypeKind",
                                    "kind": "ENUM",
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "name",
                                "args": [],
                                "type": {
                                    "ofType": None,
                                    "kind": "SCALAR",
                                    "name": "String",
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "description",
                                "args": [],
                                "type": {
                                    "kind": "SCALAR",
                                    "ofType": None,
                                    "name": "String",
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "fields",
                                "args": [
                                    {
                                        "name": "includeDeprecated",
                                        "defaultValue": "False",
                                        "type": {
                                            "ofType": None,
                                            "name": "Boolean",
                                            "kind": "SCALAR",
                                        },
                                    }
                                ],
                                "type": {
                                    "name": None,
                                    "kind": "LIST",
                                    "ofType": {
                                        "kind": "NON_NULL",
                                        "ofType": {
                                            "ofType": None,
                                            "name": "__Field",
                                            "kind": "OBJECT",
                                        },
                                        "name": None,
                                    },
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "isDeprecated": False,
                                "deprecationReason": None,
                                "name": "interfaces",
                                "args": [],
                                "type": {
                                    "name": None,
                                    "kind": "LIST",
                                    "ofType": {
                                        "ofType": {
                                            "name": "__Type",
                                            "ofType": None,
                                            "kind": "OBJECT",
                                        },
                                        "name": None,
                                        "kind": "NON_NULL",
                                    },
                                },
                            },
                            {
                                "name": "possibleTypes",
                                "args": [],
                                "type": {
                                    "kind": "LIST",
                                    "ofType": {
                                        "ofType": {
                                            "name": "__Type",
                                            "kind": "OBJECT",
                                            "ofType": None,
                                        },
                                        "name": None,
                                        "kind": "NON_NULL",
                                    },
                                    "name": None,
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "enumValues",
                                "args": [
                                    {
                                        "type": {
                                            "name": "Boolean",
                                            "kind": "SCALAR",
                                            "ofType": None,
                                        },
                                        "name": "includeDeprecated",
                                        "defaultValue": "False",
                                    }
                                ],
                                "type": {
                                    "ofType": {
                                        "ofType": {
                                            "kind": "OBJECT",
                                            "ofType": None,
                                            "name": "__EnumValue",
                                        },
                                        "name": None,
                                        "kind": "NON_NULL",
                                    },
                                    "name": None,
                                    "kind": "LIST",
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "inputFields",
                                "args": [],
                                "type": {
                                    "ofType": {
                                        "name": None,
                                        "ofType": {
                                            "kind": "OBJECT",
                                            "ofType": None,
                                            "name": "__InputValue",
                                        },
                                        "kind": "NON_NULL",
                                    },
                                    "name": None,
                                    "kind": "LIST",
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "ofType",
                                "args": [],
                                "type": {
                                    "ofType": None,
                                    "name": "__Type",
                                    "kind": "OBJECT",
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "args": [],
                                "type": {
                                    "kind": "NON_NULL",
                                    "ofType": {
                                        "ofType": None,
                                        "name": "String",
                                        "kind": "SCALAR",
                                    },
                                    "name": None,
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                                "name": "__typename",
                            },
                        ],
                        "inputFields": None,
                        "interfaces": [],
                        "enumValues": None,
                        "possibleTypes": None,
                    },
                    {
                        "kind": "OBJECT",
                        "name": "__Field",
                        "fields": [
                            {
                                "name": "name",
                                "args": [],
                                "type": {
                                    "kind": "NON_NULL",
                                    "ofType": {
                                        "kind": "SCALAR",
                                        "ofType": None,
                                        "name": "String",
                                    },
                                    "name": None,
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "description",
                                "args": [],
                                "type": {
                                    "ofType": None,
                                    "name": "String",
                                    "kind": "SCALAR",
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "args",
                                "args": [],
                                "type": {
                                    "ofType": {
                                        "name": None,
                                        "kind": "LIST",
                                        "ofType": {
                                            "kind": "NON_NULL",
                                            "ofType": {
                                                "ofType": None,
                                                "kind": "OBJECT",
                                                "name": "__InputValue",
                                            },
                                            "name": None,
                                        },
                                    },
                                    "name": None,
                                    "kind": "NON_NULL",
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "type": {
                                    "name": None,
                                    "ofType": {
                                        "name": "__Type",
                                        "kind": "OBJECT",
                                        "ofType": None,
                                    },
                                    "kind": "NON_NULL",
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                                "name": "type",
                                "args": [],
                            },
                            {
                                "name": "isDeprecated",
                                "args": [],
                                "type": {
                                    "ofType": {
                                        "ofType": None,
                                        "name": "Boolean",
                                        "kind": "SCALAR",
                                    },
                                    "name": None,
                                    "kind": "NON_NULL",
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "deprecationReason",
                                "args": [],
                                "type": {
                                    "name": "String",
                                    "kind": "SCALAR",
                                    "ofType": None,
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "__typename",
                                "args": [],
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
                        "interfaces": [],
                        "enumValues": None,
                        "possibleTypes": None,
                    },
                    {
                        "kind": "OBJECT",
                        "name": "__InputValue",
                        "fields": [
                            {
                                "isDeprecated": False,
                                "deprecationReason": None,
                                "name": "name",
                                "args": [],
                                "type": {
                                    "name": None,
                                    "kind": "NON_NULL",
                                    "ofType": {
                                        "name": "String",
                                        "kind": "SCALAR",
                                        "ofType": None,
                                    },
                                },
                            },
                            {
                                "name": "description",
                                "args": [],
                                "type": {
                                    "kind": "SCALAR",
                                    "ofType": None,
                                    "name": "String",
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "type",
                                "args": [],
                                "type": {
                                    "ofType": {
                                        "kind": "OBJECT",
                                        "ofType": None,
                                        "name": "__Type",
                                    },
                                    "name": None,
                                    "kind": "NON_NULL",
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "defaultValue",
                                "args": [],
                                "type": {
                                    "kind": "SCALAR",
                                    "ofType": None,
                                    "name": "String",
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "__typename",
                                "args": [],
                                "type": {
                                    "ofType": {
                                        "kind": "SCALAR",
                                        "ofType": None,
                                        "name": "String",
                                    },
                                    "name": None,
                                    "kind": "NON_NULL",
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                        ],
                        "inputFields": None,
                        "interfaces": [],
                        "enumValues": None,
                        "possibleTypes": None,
                    },
                    {
                        "kind": "OBJECT",
                        "name": "__EnumValue",
                        "fields": [
                            {
                                "name": "name",
                                "args": [],
                                "type": {
                                    "kind": "NON_NULL",
                                    "ofType": {
                                        "name": "String",
                                        "kind": "SCALAR",
                                        "ofType": None,
                                    },
                                    "name": None,
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "description",
                                "args": [],
                                "type": {
                                    "ofType": None,
                                    "name": "String",
                                    "kind": "SCALAR",
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "isDeprecated",
                                "args": [],
                                "type": {
                                    "kind": "NON_NULL",
                                    "ofType": {
                                        "ofType": None,
                                        "name": "Boolean",
                                        "kind": "SCALAR",
                                    },
                                    "name": None,
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "deprecationReason",
                                "args": [],
                                "type": {
                                    "name": "String",
                                    "kind": "SCALAR",
                                    "ofType": None,
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "type": {
                                    "ofType": {
                                        "kind": "SCALAR",
                                        "ofType": None,
                                        "name": "String",
                                    },
                                    "name": None,
                                    "kind": "NON_NULL",
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                                "name": "__typename",
                                "args": [],
                            },
                        ],
                        "inputFields": None,
                        "interfaces": [],
                        "enumValues": None,
                        "possibleTypes": None,
                    },
                    {
                        "kind": "ENUM",
                        "name": "__TypeKind",
                        "fields": None,
                        "inputFields": None,
                        "interfaces": None,
                        "enumValues": [
                            {
                                "name": "SCALAR",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "OBJECT",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "INTERFACE",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "UNION",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "ENUM",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "INPUT_OBJECT",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "isDeprecated": False,
                                "deprecationReason": None,
                                "name": "LIST",
                            },
                            {
                                "name": "NON_NULL",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                        ],
                        "possibleTypes": None,
                    },
                    {
                        "kind": "OBJECT",
                        "name": "__Directive",
                        "fields": [
                            {
                                "name": "name",
                                "args": [],
                                "type": {
                                    "ofType": {
                                        "ofType": None,
                                        "name": "String",
                                        "kind": "SCALAR",
                                    },
                                    "name": None,
                                    "kind": "NON_NULL",
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "description",
                                "args": [],
                                "type": {
                                    "name": "String",
                                    "kind": "SCALAR",
                                    "ofType": None,
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "locations",
                                "args": [],
                                "type": {
                                    "ofType": {
                                        "ofType": {
                                            "name": None,
                                            "ofType": {
                                                "name": "__DirectiveLocation",
                                                "kind": "ENUM",
                                                "ofType": None,
                                            },
                                            "kind": "NON_NULL",
                                        },
                                        "name": None,
                                        "kind": "LIST",
                                    },
                                    "name": None,
                                    "kind": "NON_NULL",
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "args": [],
                                "type": {
                                    "kind": "NON_NULL",
                                    "ofType": {
                                        "name": None,
                                        "kind": "LIST",
                                        "ofType": {
                                            "kind": "NON_NULL",
                                            "ofType": {
                                                "ofType": None,
                                                "name": "__InputValue",
                                                "kind": "OBJECT",
                                            },
                                            "name": None,
                                        },
                                    },
                                    "name": None,
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                                "name": "args",
                            },
                            {
                                "name": "__typename",
                                "args": [],
                                "type": {
                                    "name": None,
                                    "kind": "NON_NULL",
                                    "ofType": {
                                        "name": "String",
                                        "kind": "SCALAR",
                                        "ofType": None,
                                    },
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                        ],
                        "inputFields": None,
                        "interfaces": [],
                        "enumValues": None,
                        "possibleTypes": None,
                    },
                    {
                        "kind": "ENUM",
                        "name": "__DirectiveLocation",
                        "fields": None,
                        "inputFields": None,
                        "interfaces": None,
                        "enumValues": [
                            {
                                "name": "QUERY",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "MUTATION",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "SUBSCRIPTION",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "FIELD",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "isDeprecated": False,
                                "deprecationReason": None,
                                "name": "FRAGMENT_DEFINITION",
                            },
                            {
                                "name": "FRAGMENT_SPREAD",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "INLINE_FRAGMENT",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "SCHEMA",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "SCALAR",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "OBJECT",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "FIELD_DEFINITION",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "ARGUMENT_DEFINITION",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "INTERFACE",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "UNION",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "ENUM",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "ENUM_VALUE",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "INPUT_OBJECT",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "INPUT_FIELD_DEFINITION",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                        ],
                        "possibleTypes": None,
                    },
                ],
                "mutationType": None,
            }
        }
    } == result
