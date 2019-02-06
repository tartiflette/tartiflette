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
    results = await _TTFTT_ENGINE.execute(
        _INTROSPECTION_QUERY, operation_name="IntrospectionQuery"
    )
    assert results == {
        "data": {
            "__schema": {
                "subscriptionType": None,
                "mutationType": {"name": "Mutation"},
                "directives": [
                    {
                        "args": [
                            {
                                "defaultValue": "Deprecated",
                                "type": {
                                    "name": "String",
                                    "kind": "SCALAR",
                                    "ofType": None,
                                },
                                "name": "reason",
                            }
                        ],
                        "locations": ["FIELD_DEFINITION", "ENUM_VALUE"],
                        "name": "deprecated",
                    },
                    {
                        "locations": ["FIELD_DEFINITION"],
                        "name": "non_introspectable",
                        "args": [],
                    },
                ],
                "queryType": {"name": "Query"},
                "types": [
                    {
                        "possibleTypes": [
                            {"name": "Human", "kind": "OBJECT", "ofType": None}
                        ],
                        "enumValues": None,
                        "inputFields": None,
                        "interfaces": None,
                        "name": "Sentient",
                        "fields": [
                            {
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
                                "args": [],
                            }
                        ],
                        "kind": "INTERFACE",
                    },
                    {
                        "possibleTypes": [
                            {"name": "Dog", "kind": "OBJECT", "ofType": None}
                        ],
                        "enumValues": None,
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
                                "name": "name",
                                "args": [],
                                "deprecationReason": None,
                                "isDeprecated": False,
                            }
                        ],
                        "name": "Pet",
                        "kind": "INTERFACE",
                        "interfaces": None,
                        "inputFields": None,
                    },
                    {
                        "interfaces": [
                            {
                                "ofType": None,
                                "kind": "INTERFACE",
                                "name": "Sentient",
                            }
                        ],
                        "name": "Human",
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
                            },
                        ],
                        "kind": "OBJECT",
                        "possibleTypes": None,
                        "inputFields": None,
                        "enumValues": None,
                    },
                    {
                        "fields": [
                            {
                                "args": [],
                                "name": "name",
                                "isDeprecated": False,
                                "type": {
                                    "ofType": {
                                        "ofType": None,
                                        "kind": "SCALAR",
                                        "name": "String",
                                    },
                                    "name": None,
                                    "kind": "NON_NULL",
                                },
                                "deprecationReason": None,
                            },
                            {
                                "isDeprecated": False,
                                "deprecationReason": None,
                                "args": [],
                                "type": {
                                    "name": "Human",
                                    "ofType": None,
                                    "kind": "OBJECT",
                                },
                                "name": "owner",
                            },
                            {
                                "type": {
                                    "kind": "NON_NULL",
                                    "ofType": {
                                        "ofType": None,
                                        "name": "String",
                                        "kind": "SCALAR",
                                    },
                                    "name": None,
                                },
                                "name": "__typename",
                                "isDeprecated": False,
                                "args": [],
                                "deprecationReason": None,
                            },
                        ],
                        "kind": "OBJECT",
                        "interfaces": [
                            {
                                "kind": "INTERFACE",
                                "ofType": None,
                                "name": "Pet",
                            }
                        ],
                        "possibleTypes": None,
                        "inputFields": None,
                        "name": "Dog",
                        "enumValues": None,
                    },
                    {
                        "fields": [
                            {
                                "args": [],
                                "deprecationReason": None,
                                "name": "id",
                                "type": {
                                    "kind": "SCALAR",
                                    "ofType": None,
                                    "name": "String",
                                },
                                "isDeprecated": False,
                            },
                            {
                                "deprecationReason": None,
                                "isDeprecated": False,
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
                                "name": "__typename",
                            },
                        ],
                        "inputFields": None,
                        "enumValues": None,
                        "interfaces": [],
                        "kind": "OBJECT",
                        "name": "MutateDogPayload",
                        "possibleTypes": None,
                    },
                    {
                        "name": "Query",
                        "kind": "OBJECT",
                        "fields": [
                            {
                                "name": "dog",
                                "args": [],
                                "type": {
                                    "name": "Dog",
                                    "kind": "OBJECT",
                                    "ofType": None,
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "sentient",
                                "type": {
                                    "kind": "UNION",
                                    "ofType": None,
                                    "name": "Mixed",
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                                "args": [],
                            },
                            {
                                "args": [],
                                "type": {
                                    "kind": "NON_NULL",
                                    "ofType": {
                                        "ofType": None,
                                        "name": "__Schema",
                                        "kind": "OBJECT",
                                    },
                                    "name": None,
                                },
                                "isDeprecated": False,
                                "name": "__schema",
                                "deprecationReason": None,
                            },
                            {
                                "name": "__type",
                                "isDeprecated": False,
                                "deprecationReason": None,
                                "args": [
                                    {
                                        "defaultValue": None,
                                        "type": {
                                            "ofType": {
                                                "name": "String",
                                                "ofType": None,
                                                "kind": "SCALAR",
                                            },
                                            "name": None,
                                            "kind": "NON_NULL",
                                        },
                                        "name": "name",
                                    }
                                ],
                                "type": {
                                    "kind": "OBJECT",
                                    "ofType": None,
                                    "name": "__Type",
                                },
                            },
                            {
                                "type": {
                                    "name": None,
                                    "kind": "NON_NULL",
                                    "ofType": {
                                        "name": "String",
                                        "kind": "SCALAR",
                                        "ofType": None,
                                    },
                                },
                                "name": "__typename",
                                "deprecationReason": None,
                                "isDeprecated": False,
                                "args": [],
                            },
                        ],
                        "enumValues": None,
                        "possibleTypes": None,
                        "interfaces": [],
                        "inputFields": None,
                    },
                    {
                        "kind": "OBJECT",
                        "fields": [
                            {
                                "type": {
                                    "ofType": None,
                                    "name": "MutateDogPayload",
                                    "kind": "OBJECT",
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
                                        "kind": "SCALAR",
                                        "ofType": None,
                                        "name": "String",
                                    },
                                    "name": None,
                                },
                            },
                        ],
                        "enumValues": None,
                        "possibleTypes": None,
                        "name": "Mutation",
                        "inputFields": None,
                        "interfaces": [],
                    },
                    {
                        "interfaces": None,
                        "fields": None,
                        "possibleTypes": None,
                        "kind": "ENUM",
                        "name": "Test",
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
                                "isDeprecated": False,
                                "deprecationReason": None,
                                "name": "Value3",
                            },
                        ],
                        "inputFields": None,
                    },
                    {
                        "possibleTypes": [
                            {"kind": "OBJECT", "name": "Dog", "ofType": None},
                            {
                                "ofType": None,
                                "kind": "OBJECT",
                                "name": "Human",
                            },
                        ],
                        "enumValues": None,
                        "interfaces": None,
                        "inputFields": None,
                        "fields": None,
                        "kind": "UNION",
                        "name": "Mixed",
                    },
                    {
                        "name": "EatSomething",
                        "kind": "INPUT_OBJECT",
                        "possibleTypes": None,
                        "enumValues": None,
                        "fields": None,
                        "interfaces": None,
                        "inputFields": [
                            {
                                "type": {
                                    "ofType": None,
                                    "name": "String",
                                    "kind": "SCALAR",
                                },
                                "name": "quantity",
                                "defaultValue": None,
                            }
                        ],
                    },
                    {
                        "fields": None,
                        "possibleTypes": None,
                        "name": "Boolean",
                        "enumValues": None,
                        "interfaces": None,
                        "kind": "SCALAR",
                        "inputFields": None,
                    },
                    {
                        "possibleTypes": None,
                        "name": "Date",
                        "enumValues": None,
                        "interfaces": None,
                        "inputFields": None,
                        "fields": None,
                        "kind": "SCALAR",
                    },
                    {
                        "enumValues": None,
                        "interfaces": None,
                        "possibleTypes": None,
                        "kind": "SCALAR",
                        "fields": None,
                        "inputFields": None,
                        "name": "DateTime",
                    },
                    {
                        "enumValues": None,
                        "possibleTypes": None,
                        "interfaces": None,
                        "name": "Float",
                        "kind": "SCALAR",
                        "inputFields": None,
                        "fields": None,
                    },
                    {
                        "inputFields": None,
                        "fields": None,
                        "interfaces": None,
                        "name": "ID",
                        "possibleTypes": None,
                        "enumValues": None,
                        "kind": "SCALAR",
                    },
                    {
                        "inputFields": None,
                        "interfaces": None,
                        "fields": None,
                        "kind": "SCALAR",
                        "possibleTypes": None,
                        "enumValues": None,
                        "name": "Int",
                    },
                    {
                        "kind": "SCALAR",
                        "fields": None,
                        "inputFields": None,
                        "enumValues": None,
                        "name": "String",
                        "possibleTypes": None,
                        "interfaces": None,
                    },
                    {
                        "kind": "SCALAR",
                        "enumValues": None,
                        "interfaces": None,
                        "possibleTypes": None,
                        "name": "Time",
                        "fields": None,
                        "inputFields": None,
                    },
                    {
                        "possibleTypes": None,
                        "kind": "OBJECT",
                        "name": "__Schema",
                        "inputFields": None,
                        "enumValues": None,
                        "interfaces": [],
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
                                    "ofType": {
                                        "name": "__Type",
                                        "kind": "OBJECT",
                                        "ofType": None,
                                    },
                                    "name": None,
                                    "kind": "NON_NULL",
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
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
                                    "name": "__Type",
                                    "kind": "OBJECT",
                                    "ofType": None,
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "type": {
                                    "ofType": {
                                        "ofType": {
                                            "ofType": {
                                                "name": "__Directive",
                                                "kind": "OBJECT",
                                                "ofType": None,
                                            },
                                            "name": None,
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
                                "name": "directives",
                                "args": [],
                            },
                            {
                                "name": "__typename",
                                "args": [],
                                "type": {
                                    "name": None,
                                    "ofType": {
                                        "ofType": None,
                                        "name": "String",
                                        "kind": "SCALAR",
                                    },
                                    "kind": "NON_NULL",
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                        ],
                    },
                    {
                        "inputFields": None,
                        "name": "__Type",
                        "fields": [
                            {
                                "isDeprecated": False,
                                "deprecationReason": None,
                                "name": "kind",
                                "args": [],
                                "type": {
                                    "name": "__TypeKind",
                                    "kind": "ENUM",
                                    "ofType": None,
                                },
                            },
                            {
                                "name": "name",
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
                                "name": "description",
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
                                "name": "fields",
                                "args": [
                                    {
                                        "defaultValue": "False",
                                        "type": {
                                            "ofType": None,
                                            "name": "Boolean",
                                            "kind": "SCALAR",
                                        },
                                        "name": "includeDeprecated",
                                    }
                                ],
                                "type": {
                                    "kind": "LIST",
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
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "interfaces",
                                "args": [],
                                "type": {
                                    "kind": "LIST",
                                    "ofType": {
                                        "kind": "NON_NULL",
                                        "ofType": {
                                            "kind": "OBJECT",
                                            "ofType": None,
                                            "name": "__Type",
                                        },
                                        "name": None,
                                    },
                                    "name": None,
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "args": [],
                                "type": {
                                    "name": None,
                                    "kind": "LIST",
                                    "ofType": {
                                        "kind": "NON_NULL",
                                        "ofType": {
                                            "kind": "OBJECT",
                                            "ofType": None,
                                            "name": "__Type",
                                        },
                                        "name": None,
                                    },
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                                "name": "possibleTypes",
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
                                            "kind": "OBJECT",
                                            "ofType": None,
                                            "name": "__EnumValue",
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
                                    "name": None,
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
                                "deprecationReason": None,
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
                                "name": "__typename",
                                "args": [],
                            },
                        ],
                        "kind": "OBJECT",
                        "possibleTypes": None,
                        "interfaces": [],
                        "enumValues": None,
                    },
                    {
                        "possibleTypes": None,
                        "enumValues": None,
                        "fields": [
                            {
                                "isDeprecated": False,
                                "deprecationReason": None,
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
                            },
                            {
                                "type": {
                                    "kind": "SCALAR",
                                    "ofType": None,
                                    "name": "String",
                                },
                                "name": "description",
                                "isDeprecated": False,
                                "deprecationReason": None,
                                "args": [],
                            },
                            {
                                "args": [],
                                "isDeprecated": False,
                                "name": "args",
                                "deprecationReason": None,
                                "type": {
                                    "name": None,
                                    "kind": "NON_NULL",
                                    "ofType": {
                                        "kind": "LIST",
                                        "ofType": {
                                            "kind": "NON_NULL",
                                            "ofType": {
                                                "name": "__InputValue",
                                                "ofType": None,
                                                "kind": "OBJECT",
                                            },
                                            "name": None,
                                        },
                                        "name": None,
                                    },
                                },
                            },
                            {
                                "name": "type",
                                "type": {
                                    "name": None,
                                    "kind": "NON_NULL",
                                    "ofType": {
                                        "kind": "OBJECT",
                                        "ofType": None,
                                        "name": "__Type",
                                    },
                                },
                                "args": [],
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "deprecationReason": None,
                                "name": "isDeprecated",
                                "type": {
                                    "name": None,
                                    "kind": "NON_NULL",
                                    "ofType": {
                                        "name": "Boolean",
                                        "kind": "SCALAR",
                                        "ofType": None,
                                    },
                                },
                                "isDeprecated": False,
                                "args": [],
                            },
                            {
                                "deprecationReason": None,
                                "args": [],
                                "name": "deprecationReason",
                                "type": {
                                    "ofType": None,
                                    "name": "String",
                                    "kind": "SCALAR",
                                },
                                "isDeprecated": False,
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
                        "kind": "OBJECT",
                        "name": "__Field",
                        "interfaces": [],
                        "inputFields": None,
                    },
                    {
                        "inputFields": None,
                        "name": "__InputValue",
                        "interfaces": [],
                        "kind": "OBJECT",
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
                                "isDeprecated": False,
                                "deprecationReason": None,
                                "name": "description",
                                "args": [],
                                "type": {
                                    "kind": "SCALAR",
                                    "ofType": None,
                                    "name": "String",
                                },
                            },
                            {
                                "name": "type",
                                "args": [],
                                "type": {
                                    "name": None,
                                    "kind": "NON_NULL",
                                    "ofType": {
                                        "name": "__Type",
                                        "kind": "OBJECT",
                                        "ofType": None,
                                    },
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
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
                        "enumValues": None,
                        "possibleTypes": None,
                    },
                    {
                        "possibleTypes": None,
                        "interfaces": [],
                        "kind": "OBJECT",
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
                                "isDeprecated": False,
                                "deprecationReason": None,
                                "name": "description",
                                "args": [],
                                "type": {
                                    "name": "String",
                                    "kind": "SCALAR",
                                    "ofType": None,
                                },
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
                        "enumValues": None,
                        "name": "__EnumValue",
                    },
                    {
                        "inputFields": None,
                        "name": "__TypeKind",
                        "possibleTypes": None,
                        "kind": "ENUM",
                        "fields": None,
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
                        "interfaces": None,
                    },
                    {
                        "inputFields": None,
                        "name": "__Directive",
                        "interfaces": [],
                        "fields": [
                            {
                                "deprecationReason": None,
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
                                        "ofType": {
                                            "name": None,
                                            "ofType": {
                                                "kind": "ENUM",
                                                "name": "__DirectiveLocation",
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
                                "name": "args",
                                "args": [],
                                "type": {
                                    "kind": "NON_NULL",
                                    "ofType": {
                                        "kind": "LIST",
                                        "ofType": {
                                            "kind": "NON_NULL",
                                            "ofType": {
                                                "name": "__InputValue",
                                                "kind": "OBJECT",
                                                "ofType": None,
                                            },
                                            "name": None,
                                        },
                                        "name": None,
                                    },
                                    "name": None,
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
                        "possibleTypes": None,
                        "kind": "OBJECT",
                        "enumValues": None,
                    },
                    {
                        "inputFields": None,
                        "fields": None,
                        "possibleTypes": None,
                        "kind": "ENUM",
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
                                "deprecationReason": None,
                                "name": "SCHEMA",
                                "isDeprecated": False,
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
                                "isDeprecated": False,
                                "deprecationReason": None,
                                "name": "ENUM_VALUE",
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
                        "name": "__DirectiveLocation",
                        "interfaces": None,
                    },
                ],
            }
        }
    }
