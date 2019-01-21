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
                "types": [
                    {
                        "kind": "INTERFACE",
                        "name": "Sentient",
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
                            }
                        ],
                        "inputFields": None,
                        "interfaces": None,
                        "enumValues": None,
                        "possibleTypes": [
                            {"name": "Human", "kind": "OBJECT", "ofType": None}
                        ],
                    },
                    {
                        "kind": "INTERFACE",
                        "name": "Pet",
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
                            }
                        ],
                        "inputFields": None,
                        "interfaces": None,
                        "enumValues": None,
                        "possibleTypes": [
                            {"kind": "OBJECT", "ofType": None, "name": "Dog"}
                        ],
                    },
                    {
                        "kind": "OBJECT",
                        "name": "Human",
                        "fields": [
                            {
                                "deprecationReason": None,
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
                            },
                            {
                                "deprecationReason": None,
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
                            },
                        ],
                        "inputFields": None,
                        "interfaces": [
                            {
                                "name": "Sentient",
                                "kind": "INTERFACE",
                                "ofType": None,
                            }
                        ],
                        "enumValues": None,
                        "possibleTypes": None,
                    },
                    {
                        "kind": "OBJECT",
                        "name": "Dog",
                        "fields": [
                            {
                                "isDeprecated": False,
                                "deprecationReason": None,
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
                            },
                            {
                                "deprecationReason": None,
                                "name": "owner",
                                "args": [],
                                "type": {
                                    "name": "Human",
                                    "kind": "OBJECT",
                                    "ofType": None,
                                },
                                "isDeprecated": False,
                            },
                            {
                                "name": "__typename",
                                "args": [],
                                "type": {
                                    "ofType": {
                                        "ofType": None,
                                        "kind": "SCALAR",
                                        "name": "String",
                                    },
                                    "kind": "NON_NULL",
                                    "name": None,
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                        ],
                        "inputFields": None,
                        "interfaces": [
                            {
                                "ofType": None,
                                "name": "Pet",
                                "kind": "INTERFACE",
                            }
                        ],
                        "enumValues": None,
                        "possibleTypes": None,
                    },
                    {
                        "kind": "OBJECT",
                        "name": "MutateDogPayload",
                        "fields": [
                            {
                                "deprecationReason": None,
                                "name": "id",
                                "args": [],
                                "type": {
                                    "kind": "SCALAR",
                                    "ofType": None,
                                    "name": "String",
                                },
                                "isDeprecated": False,
                            },
                            {
                                "name": "__typename",
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
                        ],
                        "inputFields": None,
                        "interfaces": [],
                        "enumValues": None,
                        "possibleTypes": None,
                    },
                    {
                        "inputFields": None,
                        "interfaces": [],
                        "enumValues": None,
                        "possibleTypes": None,
                        "kind": "OBJECT",
                        "name": "Query",
                        "fields": [
                            {
                                "name": "dog",
                                "args": [],
                                "type": {
                                    "kind": "OBJECT",
                                    "ofType": None,
                                    "name": "Dog",
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "sentient",
                                "args": [],
                                "type": {
                                    "ofType": None,
                                    "name": "Mixed",
                                    "kind": "UNION",
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "type": {
                                    "name": None,
                                    "kind": "NON_NULL",
                                    "ofType": {
                                        "name": "__Schema",
                                        "kind": "OBJECT",
                                        "ofType": None,
                                    },
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                                "name": "__schema",
                                "args": [],
                            },
                            {
                                "name": "__type",
                                "args": [
                                    {
                                        "defaultValue": None,
                                        "type": {
                                            "ofType": None,
                                            "name": None,
                                            "kind": "NON_NULL",
                                        },
                                        "name": "name",
                                    }
                                ],
                                "type": {
                                    "name": "__Type",
                                    "kind": "OBJECT",
                                    "ofType": None,
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
                    },
                    {
                        "kind": "OBJECT",
                        "name": "Mutation",
                        "fields": [
                            {
                                "name": "mutateDog",
                                "args": [],
                                "type": {
                                    "name": "MutateDogPayload",
                                    "kind": "OBJECT",
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
                                        "kind": "SCALAR",
                                        "ofType": None,
                                        "name": "String",
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
                        "kind": "ENUM",
                        "name": "Test",
                        "fields": None,
                        "inputFields": None,
                        "interfaces": None,
                        "enumValues": [
                            {
                                "name": "Value1",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "Value2",
                                "isDeprecated": True,
                                "deprecationReason": "Unused anymore",
                            },
                            {
                                "name": "Value3",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                        ],
                        "possibleTypes": None,
                    },
                    {
                        "kind": "UNION",
                        "name": "Mixed",
                        "fields": None,
                        "inputFields": None,
                        "interfaces": None,
                        "enumValues": None,
                        "possibleTypes": [
                            {"kind": "OBJECT", "name": "Dog", "ofType": None},
                            {
                                "name": "Human",
                                "ofType": None,
                                "kind": "OBJECT",
                            },
                        ],
                    },
                    {
                        "kind": "INPUT_OBJECT",
                        "name": "EatSomething",
                        "fields": None,
                        "inputFields": [
                            {
                                "defaultValue": None,
                                "type": {
                                    "kind": "SCALAR",
                                    "ofType": None,
                                    "name": "String",
                                },
                                "name": "quantity",
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
                        "kind": "SCALAR",
                        "name": "ID",
                        "fields": None,
                        "inputFields": None,
                        "interfaces": None,
                        "enumValues": None,
                        "possibleTypes": None,
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
                                    "ofType": {
                                        "ofType": {
                                            "name": None,
                                            "kind": "NON_NULL",
                                            "ofType": {
                                                "ofType": None,
                                                "name": "__Type",
                                                "kind": "OBJECT",
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
                                "name": "queryType",
                                "args": [],
                                "type": {
                                    "name": None,
                                    "ofType": {
                                        "ofType": None,
                                        "name": "__Type",
                                        "kind": "OBJECT",
                                    },
                                    "kind": "NON_NULL",
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
                                "args": [],
                                "type": {
                                    "name": None,
                                    "kind": "NON_NULL",
                                    "ofType": {
                                        "name": None,
                                        "kind": "LIST",
                                        "ofType": {
                                            "kind": "NON_NULL",
                                            "name": None,
                                            "ofType": {
                                                "name": "__Directive",
                                                "kind": "OBJECT",
                                                "ofType": None,
                                            },
                                        },
                                    },
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                                "name": "directives",
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
                        "kind": "OBJECT",
                        "name": "__Type",
                        "fields": [
                            {
                                "name": "kind",
                                "args": [],
                                "type": {
                                    "name": "__TypeKind",
                                    "kind": "ENUM",
                                    "ofType": None,
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "isDeprecated": False,
                                "deprecationReason": None,
                                "name": "name",
                                "args": [],
                                "type": {
                                    "ofType": None,
                                    "name": "String",
                                    "kind": "SCALAR",
                                },
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
                                        "name": "includeDeprecated",
                                        "defaultValue": "False",
                                        "type": {
                                            "kind": "SCALAR",
                                            "ofType": None,
                                            "name": "Boolean",
                                        },
                                    }
                                ],
                                "type": {
                                    "ofType": {
                                        "ofType": {
                                            "name": "__Field",
                                            "ofType": None,
                                            "kind": "OBJECT",
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
                                "name": "interfaces",
                                "args": [],
                                "type": {
                                    "name": None,
                                    "kind": "LIST",
                                    "ofType": {
                                        "name": None,
                                        "kind": "NON_NULL",
                                        "ofType": {
                                            "kind": "OBJECT",
                                            "name": "__Type",
                                            "ofType": None,
                                        },
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
                                        "ofType": {
                                            "name": "__Type",
                                            "kind": "OBJECT",
                                            "ofType": None,
                                        },
                                        "kind": "NON_NULL",
                                    },
                                    "name": None,
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "args": [
                                    {
                                        "name": "includeDeprecated",
                                        "defaultValue": "False",
                                        "type": {
                                            "kind": "SCALAR",
                                            "ofType": None,
                                            "name": "Boolean",
                                        },
                                    }
                                ],
                                "type": {
                                    "ofType": {
                                        "ofType": {
                                            "kind": "OBJECT",
                                            "name": "__EnumValue",
                                            "ofType": None,
                                        },
                                        "kind": "NON_NULL",
                                        "name": None,
                                    },
                                    "name": None,
                                    "kind": "LIST",
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                                "name": "enumValues",
                            },
                            {
                                "name": "inputFields",
                                "args": [],
                                "type": {
                                    "ofType": {
                                        "ofType": {
                                            "ofType": None,
                                            "name": "__InputValue",
                                            "kind": "OBJECT",
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
                    },
                    {
                        "kind": "OBJECT",
                        "name": "__Field",
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
                                    "ofType": {
                                        "ofType": {
                                            "name": None,
                                            "kind": "NON_NULL",
                                            "ofType": {
                                                "ofType": None,
                                                "name": "__InputValue",
                                                "kind": "OBJECT",
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
                                "name": "type",
                                "args": [],
                                "type": {
                                    "name": None,
                                    "kind": "NON_NULL",
                                    "ofType": {
                                        "kind": "OBJECT",
                                        "ofType": None,
                                        "name": "__Type",
                                    },
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
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
                        "kind": "OBJECT",
                        "name": "__InputValue",
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
                                "args": [],
                                "type": {
                                    "name": None,
                                    "kind": "NON_NULL",
                                    "ofType": {
                                        "kind": "OBJECT",
                                        "ofType": None,
                                        "name": "__Type",
                                    },
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                                "name": "type",
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
                        "kind": "OBJECT",
                        "name": "__EnumValue",
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
                                    "kind": "NON_NULL",
                                    "name": None,
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
                                "name": "description",
                                "args": [],
                            },
                            {
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
                                    "kind": "NON_NULL",
                                    "ofType": {
                                        "name": None,
                                        "kind": "LIST",
                                        "ofType": {
                                            "name": None,
                                            "ofType": {
                                                "kind": "ENUM",
                                                "ofType": None,
                                                "name": "__DirectiveLocation",
                                            },
                                            "kind": "NON_NULL",
                                        },
                                    },
                                    "name": None,
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
                                                "ofType": None,
                                                "name": "__InputValue",
                                                "kind": "OBJECT",
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
                        "name": "__DirectiveLocation",
                        "fields": None,
                        "inputFields": None,
                        "interfaces": None,
                        "enumValues": [
                            {
                                "name": "QUERY",
                                "deprecationReason": None,
                                "isDeprecated": False,
                            },
                            {
                                "isDeprecated": False,
                                "deprecationReason": None,
                                "name": "MUTATION",
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
                                "deprecationReason": None,
                                "name": "INPUT_OBJECT",
                                "isDeprecated": False,
                            },
                            {
                                "name": "INPUT_FIELD_DEFINITION",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                        ],
                        "possibleTypes": None,
                        "kind": "ENUM",
                    },
                ],
                "mutationType": {"name": "Mutation"},
                "directives": [
                    {
                        "name": "deprecated",
                        "locations": ["FIELD_DEFINITION", "ENUM_VALUE"],
                        "args": [
                            {
                                "name": "reason",
                                "defaultValue": "No longer supported",
                                "type": {
                                    "name": "String",
                                    "kind": "SCALAR",
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
                "queryType": {"name": "Query"},
            }
        }
    }
