import pytest

from tartiflette.engine import Engine

_TTFTT_ENGINE = Engine(
    """
    interface Sentient {
      name: String!
    }

    interface Pet {
      name: String!
    }

    type Human implements Sentient {
      name: String!
    }

    type Dog implements Pet {
      name: String!
      owner: Human
    }

    type MutateDogPayload {
      id: String
    }

    type Query {
      dog: Dog
      sentient: Mixed
    }

    type Mutation {
      mutateDog: MutateDogPayload
    }

    enum Test {
        Value1
        Value2 @deprecated(reason: "Unused anymore")
        Value3
    }

    union Mixed = Dog | Human

    input EatSomething {
        quantity: String
    }

    """,
    schema_name="test_issue92",
)


_INTROSPECTION_QUERY = """
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


@pytest.mark.asyncio
async def test_issue92_fragment_inordered():
    results = await _TTFTT_ENGINE.execute(_INTROSPECTION_QUERY)
    print(results)
    assert results == {
        "data": {
            "__schema": {
                "subscriptionType": None,
                "directives": [
                    {
                        "locations": ["FIELD_DEFINITION", "ENUM_VALUE"],
                        "name": "deprecated",
                        "args": [
                            {
                                "type": {
                                    "name": "String",
                                    "kind": None,
                                    "ofType": None,
                                },
                                "defaultValue": "No longer supported",
                                "name": "reason",
                            }
                        ],
                    },
                    {
                        "name": "non_introspectable",
                        "args": [],
                        "locations": ["FIELD_DEFINITION"],
                    },
                ],
                "queryType": {"name": "Query"},
                "mutationType": {"name": "Mutation"},
                "types": [
                    {
                        "interfaces": None,
                        "inputFields": None,
                        "name": "Sentient",
                        "fields": [
                            {
                                "name": "name",
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
                                "isDeprecated": False,
                                "deprecationReason": None,
                            }
                        ],
                        "enumValues": None,
                        "possibleTypes": [
                            {"ofType": None, "name": "Human", "kind": "OBJECT"}
                        ],
                        "kind": "INTERFACE",
                    },
                    {
                        "inputFields": None,
                        "possibleTypes": [
                            {"name": "Dog", "kind": "OBJECT", "ofType": None}
                        ],
                        "name": "Pet",
                        "fields": [
                            {
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
                                "name": "name",
                                "args": [],
                            }
                        ],
                        "kind": "INTERFACE",
                        "enumValues": None,
                        "interfaces": None,
                    },
                    {
                        "enumValues": None,
                        "possibleTypes": None,
                        "interfaces": [
                            {
                                "name": "Sentient",
                                "kind": "INTERFACE",
                                "ofType": None,
                            }
                        ],
                        "inputFields": None,
                        "name": "Human",
                        "fields": [
                            {
                                "name": "name",
                                "args": [],
                                "type": {
                                    "ofType": {
                                        "ofType": None,
                                        "kind": "SCALAR",
                                        "name": "String",
                                    },
                                    "name": None,
                                    "kind": "NON_NULL",
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
                                        "kind": "SCALAR",
                                        "ofType": None,
                                        "name": "String",
                                    },
                                    "name": None,
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                        ],
                        "kind": "OBJECT",
                    },
                    {
                        "enumValues": None,
                        "possibleTypes": None,
                        "inputFields": None,
                        "interfaces": [
                            {
                                "name": "Pet",
                                "kind": "INTERFACE",
                                "ofType": None,
                            }
                        ],
                        "name": "Dog",
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
                                "args": [],
                                "type": {
                                    "kind": "OBJECT",
                                    "ofType": None,
                                    "name": "Human",
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                                "name": "owner",
                            },
                            {
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
                                "name": "__typename",
                            },
                        ],
                        "kind": "OBJECT",
                    },
                    {
                        "possibleTypes": None,
                        "kind": "OBJECT",
                        "fields": [
                            {
                                "name": "id",
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
                                        "name": "String",
                                        "ofType": None,
                                    },
                                    "name": None,
                                    "kind": "NON_NULL",
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                        ],
                        "interfaces": [],
                        "enumValues": None,
                        "name": "MutateDogPayload",
                        "inputFields": None,
                    },
                    {
                        "interfaces": [],
                        "possibleTypes": None,
                        "enumValues": None,
                        "fields": [
                            {
                                "isDeprecated": False,
                                "deprecationReason": None,
                                "name": "dog",
                                "args": [],
                                "type": {
                                    "kind": "OBJECT",
                                    "ofType": None,
                                    "name": "Dog",
                                },
                            },
                            {
                                "name": "sentient",
                                "args": [],
                                "type": {
                                    "name": "Mixed",
                                    "kind": "UNION",
                                    "ofType": None,
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "__schema",
                                "args": [],
                                "type": {
                                    "ofType": {
                                        "ofType": None,
                                        "name": "__Schema",
                                        "kind": "OBJECT",
                                    },
                                    "name": None,
                                    "kind": "NON_NULL",
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "__type",
                                "args": [
                                    {
                                        "type": {
                                            "kind": "NON_NULL",
                                            "ofType": None,
                                            "name": "String!",
                                        },
                                        "name": "name",
                                        "defaultValue": None,
                                    }
                                ],
                                "type": {
                                    "ofType": None,
                                    "name": "__Type",
                                    "kind": "OBJECT",
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
                                        "kind": "SCALAR",
                                        "ofType": None,
                                        "name": "String",
                                    },
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                        ],
                        "inputFields": None,
                        "kind": "OBJECT",
                        "name": "Query",
                    },
                    {
                        "possibleTypes": None,
                        "name": "Mutation",
                        "enumValues": None,
                        "fields": [
                            {
                                "type": {
                                    "name": "MutateDogPayload",
                                    "kind": "OBJECT",
                                    "ofType": None,
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                                "name": "mutateDog",
                                "args": [],
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
                        "interfaces": [],
                        "inputFields": None,
                        "kind": "OBJECT",
                    },
                    {
                        "enumValues": [
                            {
                                "deprecationReason": None,
                                "name": "Value1",
                                "isDeprecated": False,
                            },
                            {
                                "name": "Value2",
                                "isDeprecated": True,
                                "deprecationReason": "Unused anymore",
                            },
                            {
                                "deprecationReason": None,
                                "name": "Value3",
                                "isDeprecated": False,
                            },
                        ],
                        "possibleTypes": None,
                        "fields": None,
                        "inputFields": None,
                        "interfaces": None,
                        "name": "Test",
                        "kind": "ENUM",
                    },
                    {
                        "kind": "UNION",
                        "name": "Mixed",
                        "fields": None,
                        "inputFields": None,
                        "interfaces": None,
                        "enumValues": None,
                        "possibleTypes": [
                            {"name": "Dog", "ofType": None, "kind": "OBJECT"},
                            {
                                "kind": "OBJECT",
                                "name": "Human",
                                "ofType": None,
                            },
                        ],
                    },
                    {
                        "kind": "INPUT_OBJECT",
                        "name": "EatSomething",
                        "fields": None,
                        "inputFields": [
                            {
                                "type": {
                                    "kind": "SCALAR",
                                    "ofType": None,
                                    "name": "String",
                                },
                                "name": "quantity",
                                "defaultValue": None,
                            }
                        ],
                        "interfaces": None,
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
                        "name": "Date",
                        "fields": None,
                        "inputFields": None,
                        "interfaces": None,
                        "enumValues": None,
                        "possibleTypes": None,
                    },
                    {
                        "kind": "SCALAR",
                        "name": "DateTime",
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
                        "fields": None,
                        "inputFields": None,
                        "interfaces": None,
                        "enumValues": None,
                        "possibleTypes": None,
                        "kind": "SCALAR",
                        "name": "ID",
                    },
                    {
                        "kind": "SCALAR",
                        "name": "Int",
                        "fields": None,
                        "inputFields": None,
                        "interfaces": None,
                        "enumValues": None,
                        "possibleTypes": None,
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
                                    "name": None,
                                    "kind": "NON_NULL",
                                    "ofType": {
                                        "name": None,
                                        "ofType": {
                                            "kind": "NON_NULL",
                                            "ofType": {
                                                "kind": "OBJECT",
                                                "ofType": None,
                                                "name": "__Type",
                                            },
                                            "name": None,
                                        },
                                        "kind": "LIST",
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
                                        "kind": "OBJECT",
                                        "ofType": None,
                                        "name": "__Type",
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
                                "args": [],
                                "type": {
                                    "kind": "OBJECT",
                                    "ofType": None,
                                    "name": "__Type",
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                                "name": "subscriptionType",
                            },
                            {
                                "name": "directives",
                                "args": [],
                                "type": {
                                    "ofType": {
                                        "name": None,
                                        "kind": "LIST",
                                        "ofType": {
                                            "ofType": {
                                                "name": "__Directive",
                                                "kind": "OBJECT",
                                                "ofType": None,
                                            },
                                            "name": None,
                                            "kind": "NON_NULL",
                                        },
                                    },
                                    "kind": "NON_NULL",
                                    "name": None,
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
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
                                    "name": "String",
                                    "ofType": None,
                                    "kind": "SCALAR",
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
                                "name": "fields",
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
                                            "kind": "OBJECT",
                                            "ofType": None,
                                            "name": "__Field",
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
                                "type": {
                                    "kind": "LIST",
                                    "ofType": {
                                        "ofType": {
                                            "kind": "OBJECT",
                                            "ofType": None,
                                            "name": "__Type",
                                        },
                                        "name": None,
                                        "kind": "NON_NULL",
                                    },
                                    "name": None,
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                                "name": "interfaces",
                                "args": [],
                            },
                            {
                                "name": "possibleTypes",
                                "args": [],
                                "type": {
                                    "name": None,
                                    "kind": "LIST",
                                    "ofType": {
                                        "name": None,
                                        "kind": "NON_NULL",
                                        "ofType": {
                                            "ofType": None,
                                            "kind": "OBJECT",
                                            "name": "__Type",
                                        },
                                    },
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "enumValues",
                                "args": [
                                    {
                                        "defaultValue": "False",
                                        "type": {
                                            "name": "Boolean",
                                            "kind": "SCALAR",
                                            "ofType": None,
                                        },
                                        "name": "includeDeprecated",
                                    }
                                ],
                                "type": {
                                    "kind": "LIST",
                                    "ofType": {
                                        "kind": "NON_NULL",
                                        "ofType": {
                                            "name": "__EnumValue",
                                            "kind": "OBJECT",
                                            "ofType": None,
                                        },
                                        "name": None,
                                    },
                                    "name": None,
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
                                            "kind": "OBJECT",
                                            "ofType": None,
                                            "name": "__InputValue",
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
                        "possibleTypes": None,
                        "kind": "OBJECT",
                        "name": "__Field",
                        "fields": [
                            {
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
                                "name": "name",
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
                                "name": "args",
                                "args": [],
                                "type": {
                                    "kind": "NON_NULL",
                                    "ofType": {
                                        "name": None,
                                        "kind": "LIST",
                                        "ofType": {
                                            "ofType": {
                                                "ofType": None,
                                                "name": "__InputValue",
                                                "kind": "OBJECT",
                                            },
                                            "name": None,
                                            "kind": "NON_NULL",
                                        },
                                    },
                                    "name": None,
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "type",
                                "args": [],
                                "type": {
                                    "name": None,
                                    "kind": "NON_NULL",
                                    "ofType": {
                                        "ofType": None,
                                        "name": "__Type",
                                        "kind": "OBJECT",
                                    },
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "deprecationReason": None,
                                "name": "isDeprecated",
                                "args": [],
                                "type": {
                                    "kind": "NON_NULL",
                                    "ofType": {
                                        "kind": "SCALAR",
                                        "ofType": None,
                                        "name": "Boolean",
                                    },
                                    "name": None,
                                },
                                "isDeprecated": False,
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
                        "inputFields": None,
                        "interfaces": [],
                        "enumValues": None,
                    },
                    {
                        "kind": "OBJECT",
                        "name": "__InputValue",
                        "fields": [
                            {
                                "name": "name",
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
                            {
                                "name": "description",
                                "args": [],
                                "type": {
                                    "name": "String",
                                    "ofType": None,
                                    "kind": "SCALAR",
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "type",
                                "args": [],
                                "type": {
                                    "ofType": {
                                        "name": "__Type",
                                        "ofType": None,
                                        "kind": "OBJECT",
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
                                    "name": "String",
                                    "kind": "SCALAR",
                                    "ofType": None,
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
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
                        "name": "__EnumValue",
                        "fields": [
                            {
                                "name": "name",
                                "args": [],
                                "type": {
                                    "name": None,
                                    "kind": "NON_NULL",
                                    "ofType": {
                                        "kind": "SCALAR",
                                        "ofType": None,
                                        "name": "String",
                                    },
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
                                "name": "isDeprecated",
                                "args": [],
                                "type": {
                                    "name": None,
                                    "kind": "NON_NULL",
                                    "ofType": {
                                        "kind": "SCALAR",
                                        "ofType": None,
                                        "name": "Boolean",
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
                                    "ofType": {
                                        "kind": "SCALAR",
                                        "ofType": None,
                                        "name": "String",
                                    },
                                    "name": None,
                                    "kind": "NON_NULL",
                                },
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
                                "isDeprecated": False,
                                "deprecationReason": None,
                                "name": "INPUT_OBJECT",
                            },
                            {
                                "name": "LIST",
                                "isDeprecated": False,
                                "deprecationReason": None,
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
                                "name": "locations",
                                "args": [],
                                "type": {
                                    "name": None,
                                    "kind": "NON_NULL",
                                    "ofType": {
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
                                        "name": None,
                                    },
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "args",
                                "args": [],
                                "type": {
                                    "ofType": {
                                        "ofType": {
                                            "name": None,
                                            "kind": "NON_NULL",
                                            "ofType": {
                                                "name": "__InputValue",
                                                "kind": "OBJECT",
                                                "ofType": None,
                                            },
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
                                "isDeprecated": False,
                                "deprecationReason": None,
                                "name": "__typename",
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
                                "deprecationReason": None,
                                "name": "SUBSCRIPTION",
                                "isDeprecated": False,
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
                                "isDeprecated": False,
                                "deprecationReason": None,
                                "name": "FIELD_DEFINITION",
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
                                "isDeprecated": False,
                                "deprecationReason": None,
                                "name": "INPUT_FIELD_DEFINITION",
                            },
                        ],
                        "possibleTypes": None,
                    },
                ],
            }
        }
    }
