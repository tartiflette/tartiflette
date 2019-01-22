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
                    {"kind": "OBJECT", "name": "__Schema"},
                    {"kind": "OBJECT", "name": "__Type"},
                    {"kind": "OBJECT", "name": "__Field"},
                    {"name": "__InputValue", "kind": "OBJECT"},
                    {"name": "__EnumValue", "kind": "OBJECT"},
                    {"name": "__TypeKind", "kind": "ENUM"},
                    {"name": "__Directive", "kind": "OBJECT"},
                    {"kind": "ENUM", "name": "__DirectiveLocation"},
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
    """
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
                    {"name": "__Schema", "kind": "OBJECT"},
                    {"name": "__Type", "kind": "OBJECT"},
                    {"name": "__Field", "kind": "OBJECT"},
                    {"kind": "OBJECT", "name": "__InputValue"},
                    {"kind": "OBJECT", "name": "__EnumValue"},
                    {"kind": "ENUM", "name": "__TypeKind"},
                    {"name": "__Directive", "kind": "OBJECT"},
                    {"name": "__DirectiveLocation", "kind": "ENUM"},
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
    """
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
                            },
                            {
                                "type": {
                                    "name": None,
                                    "kind": "NON_NULL",
                                    "ofType": {
                                        "ofType": None,
                                        "name": "__Schema",
                                        "kind": "OBJECT",
                                    },
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                                "name": "__schema",
                                "args": [],
                            },
                            {
                                "isDeprecated": False,
                                "deprecationReason": None,
                                "name": "__type",
                                "args": [
                                    {
                                        "defaultValue": None,
                                        "type": {
                                            "name": None,
                                            "kind": "NON_NULL",
                                            "ofType": {
                                                "ofType": None,
                                                "name": "String",
                                                "kind": "SCALAR",
                                            },
                                        },
                                        "name": "name",
                                    }
                                ],
                                "type": {
                                    "name": "__Type",
                                    "kind": "OBJECT",
                                    "ofType": None,
                                },
                            },
                            {
                                "deprecationReason": None,
                                "isDeprecated": False,
                                "name": "__typename",
                                "type": {
                                    "name": None,
                                    "kind": "NON_NULL",
                                    "ofType": {
                                        "kind": "SCALAR",
                                        "ofType": None,
                                        "name": "String",
                                    },
                                },
                                "args": [],
                            },
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
                    {
                        "fields": [
                            {
                                "name": "types",
                                "args": [],
                                "type": {
                                    "name": None,
                                    "kind": "NON_NULL",
                                    "ofType": {
                                        "name": None,
                                        "kind": "LIST",
                                        "ofType": {
                                            "name": None,
                                            "kind": "NON_NULL",
                                            "ofType": {
                                                "ofType": None,
                                                "name": "__Type",
                                                "kind": "OBJECT",
                                            },
                                        },
                                    },
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "queryType",
                                "args": [],
                                "type": {
                                    "kind": "NON_NULL",
                                    "ofType": {
                                        "name": "__Type",
                                        "kind": "OBJECT",
                                        "ofType": None,
                                    },
                                    "name": None,
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "mutationType",
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
                                "isDeprecated": False,
                                "deprecationReason": None,
                                "name": "directives",
                                "args": [],
                                "type": {
                                    "name": None,
                                    "kind": "NON_NULL",
                                    "ofType": {
                                        "kind": "LIST",
                                        "ofType": {
                                            "name": None,
                                            "kind": "NON_NULL",
                                            "ofType": {
                                                "name": "__Directive",
                                                "ofType": None,
                                                "kind": "OBJECT",
                                            },
                                        },
                                        "name": None,
                                    },
                                },
                            },
                            {
                                "name": "__typename",
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
                        ],
                        "interfaces": [],
                        "inputFields": None,
                        "possibleTypes": None,
                        "name": "__Schema",
                        "kind": "OBJECT",
                        "enumValues": None,
                    },
                    {
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
                                "type": {
                                    "ofType": None,
                                    "name": "String",
                                    "kind": "SCALAR",
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                                "name": "name",
                                "args": [],
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
                                "name": "interfaces",
                                "args": [],
                                "type": {
                                    "name": None,
                                    "kind": "LIST",
                                    "ofType": {
                                        "kind": "NON_NULL",
                                        "ofType": {
                                            "ofType": None,
                                            "kind": "OBJECT",
                                            "name": "__Type",
                                        },
                                        "name": None,
                                    },
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "possibleTypes",
                                "args": [],
                                "type": {
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
                                        "kind": "NON_NULL",
                                        "ofType": {
                                            "ofType": None,
                                            "name": "__EnumValue",
                                            "kind": "OBJECT",
                                        },
                                        "name": None,
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
                                        "kind": "NON_NULL",
                                        "ofType": {
                                            "ofType": None,
                                            "name": "__InputValue",
                                            "kind": "OBJECT",
                                        },
                                        "name": None,
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
                                    "kind": "OBJECT",
                                    "ofType": None,
                                    "name": "__Type",
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
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
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                        ],
                        "inputFields": None,
                        "possibleTypes": None,
                        "interfaces": [],
                        "kind": "OBJECT",
                        "enumValues": None,
                        "name": "__Type",
                    },
                    {
                        "fields": [
                            {
                                "name": "name",
                                "args": [],
                                "type": {
                                    "ofType": {
                                        "name": "String",
                                        "kind": "SCALAR",
                                        "ofType": None,
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
                                    "name": None,
                                    "kind": "NON_NULL",
                                    "ofType": {
                                        "ofType": {
                                            "name": None,
                                            "kind": "NON_NULL",
                                            "ofType": {
                                                "name": "__InputValue",
                                                "ofType": None,
                                                "kind": "OBJECT",
                                            },
                                        },
                                        "name": None,
                                        "kind": "LIST",
                                    },
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
                                "name": "isDeprecated",
                                "args": [],
                                "type": {
                                    "name": None,
                                    "kind": "NON_NULL",
                                    "ofType": {
                                        "ofType": None,
                                        "name": "Boolean",
                                        "kind": "SCALAR",
                                    },
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "deprecationReason",
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
                                "isDeprecated": False,
                                "deprecationReason": None,
                                "name": "__typename",
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
                            },
                        ],
                        "kind": "OBJECT",
                        "possibleTypes": None,
                        "interfaces": [],
                        "name": "__Field",
                        "enumValues": None,
                        "inputFields": None,
                    },
                    {
                        "fields": [
                            {
                                "name": "name",
                                "args": [],
                                "type": {
                                    "name": None,
                                    "ofType": {
                                        "name": "String",
                                        "kind": "SCALAR",
                                        "ofType": None,
                                    },
                                    "kind": "NON_NULL",
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
                                "deprecationReason": None,
                                "name": "type",
                                "args": [],
                                "type": {
                                    "kind": "NON_NULL",
                                    "ofType": {
                                        "kind": "OBJECT",
                                        "ofType": None,
                                        "name": "__Type",
                                    },
                                    "name": None,
                                },
                                "isDeprecated": False,
                            },
                            {
                                "name": "defaultValue",
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
                        "possibleTypes": None,
                        "name": "__InputValue",
                        "kind": "OBJECT",
                        "interfaces": [],
                        "inputFields": None,
                        "enumValues": None,
                    },
                    {
                        "fields": [
                            {
                                "deprecationReason": None,
                                "name": "name",
                                "args": [],
                                "type": {
                                    "ofType": {
                                        "kind": "SCALAR",
                                        "ofType": None,
                                        "name": "String",
                                    },
                                    "kind": "NON_NULL",
                                    "name": None,
                                },
                                "isDeprecated": False,
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
                                    "ofType": None,
                                    "name": "String",
                                    "kind": "SCALAR",
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "__typename",
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
                            },
                        ],
                        "inputFields": None,
                        "interfaces": [],
                        "enumValues": None,
                        "possibleTypes": None,
                        "kind": "OBJECT",
                        "name": "__EnumValue",
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
                                        "name": "String",
                                        "kind": "SCALAR",
                                        "ofType": None,
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
                                    "kind": "SCALAR",
                                    "ofType": None,
                                    "name": "String",
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "locations",
                                "args": [],
                                "type": {
                                    "ofType": {
                                        "name": None,
                                        "kind": "LIST",
                                        "ofType": {
                                            "kind": "NON_NULL",
                                            "ofType": {
                                                "kind": "ENUM",
                                                "name": "__DirectiveLocation",
                                                "ofType": None,
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
                                "args": [],
                                "type": {
                                    "ofType": {
                                        "kind": "LIST",
                                        "ofType": {
                                            "kind": "NON_NULL",
                                            "ofType": {
                                                "kind": "OBJECT",
                                                "ofType": None,
                                                "name": "__InputValue",
                                            },
                                            "name": None,
                                        },
                                        "name": None,
                                    },
                                    "name": None,
                                    "kind": "NON_NULL",
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
                                "name": "FRAGMENT_DEFINITION",
                                "isDeprecated": False,
                                "deprecationReason": None,
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
                                "deprecationReason": None,
                                "name": "ARGUMENT_DEFINITION",
                                "isDeprecated": False,
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
                "subscriptionType": None,
            }
        }
    } == result
