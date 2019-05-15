import pytest

from tartiflette import Engine

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
                        "name": "nonIntrospectable",
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
                "queryType": {"name": "Query"},
                "mutationType": {"name": "Mutation"},
                "subscriptionType": None,
                "types": [
                    {
                        "kind": "INTERFACE",
                        "name": "Sentient",
                        "inputFields": None,
                        "interfaces": None,
                        "possibleTypes": [
                            {"name": "Human", "kind": "OBJECT", "ofType": None}
                        ],
                        "fields": [
                            {
                                "name": "name",
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
                                "args": [],
                                "deprecationReason": None,
                            }
                        ],
                        "enumValues": None,
                    },
                    {
                        "kind": "INTERFACE",
                        "name": "Pet",
                        "inputFields": None,
                        "interfaces": None,
                        "possibleTypes": [
                            {"ofType": None, "name": "Dog", "kind": "OBJECT"}
                        ],
                        "fields": [
                            {
                                "isDeprecated": False,
                                "args": [],
                                "deprecationReason": None,
                                "name": "name",
                                "type": {
                                    "ofType": {
                                        "kind": "SCALAR",
                                        "name": "String",
                                        "ofType": None,
                                    },
                                    "name": None,
                                    "kind": "NON_NULL",
                                },
                            }
                        ],
                        "enumValues": None,
                    },
                    {
                        "kind": "OBJECT",
                        "name": "Human",
                        "inputFields": None,
                        "interfaces": [
                            {
                                "ofType": None,
                                "name": "Sentient",
                                "kind": "INTERFACE",
                            }
                        ],
                        "possibleTypes": None,
                        "fields": [
                            {
                                "name": "name",
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
                                "args": [],
                                "deprecationReason": None,
                            }
                        ],
                        "enumValues": None,
                    },
                    {
                        "kind": "OBJECT",
                        "name": "Dog",
                        "inputFields": None,
                        "interfaces": [
                            {
                                "name": "Pet",
                                "kind": "INTERFACE",
                                "ofType": None,
                            }
                        ],
                        "possibleTypes": None,
                        "fields": [
                            {
                                "name": "name",
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
                                "args": [],
                                "deprecationReason": None,
                            },
                            {
                                "type": {
                                    "kind": "OBJECT",
                                    "ofType": None,
                                    "name": "Human",
                                },
                                "name": "owner",
                                "args": [],
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                        ],
                        "enumValues": None,
                    },
                    {
                        "kind": "OBJECT",
                        "name": "MutateDogPayload",
                        "inputFields": None,
                        "interfaces": [],
                        "possibleTypes": None,
                        "fields": [
                            {
                                "args": [],
                                "deprecationReason": None,
                                "name": "id",
                                "type": {
                                    "name": "String",
                                    "ofType": None,
                                    "kind": "SCALAR",
                                },
                                "isDeprecated": False,
                            }
                        ],
                        "enumValues": None,
                    },
                    {
                        "possibleTypes": None,
                        "kind": "OBJECT",
                        "name": "Query",
                        "inputFields": None,
                        "interfaces": [],
                        "enumValues": None,
                        "fields": [
                            {
                                "isDeprecated": False,
                                "args": [],
                                "deprecationReason": None,
                                "name": "dog",
                                "type": {
                                    "ofType": None,
                                    "kind": "OBJECT",
                                    "name": "Dog",
                                },
                            },
                            {
                                "isDeprecated": False,
                                "name": "sentient",
                                "deprecationReason": None,
                                "args": [],
                                "type": {
                                    "ofType": None,
                                    "name": "Mixed",
                                    "kind": "UNION",
                                },
                            },
                        ],
                    },
                    {
                        "kind": "OBJECT",
                        "name": "Mutation",
                        "inputFields": None,
                        "interfaces": [],
                        "possibleTypes": None,
                        "fields": [
                            {
                                "args": [],
                                "name": "mutateDog",
                                "type": {
                                    "kind": "OBJECT",
                                    "ofType": None,
                                    "name": "MutateDogPayload",
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            }
                        ],
                        "enumValues": None,
                    },
                    {
                        "kind": "ENUM",
                        "name": "Test",
                        "inputFields": None,
                        "interfaces": None,
                        "possibleTypes": None,
                        "fields": None,
                        "enumValues": [
                            {
                                "isDeprecated": False,
                                "name": "Value1",
                                "deprecationReason": None,
                            },
                            {
                                "deprecationReason": "Unused anymore",
                                "isDeprecated": True,
                                "name": "Value2",
                            },
                            {
                                "name": "Value3",
                                "deprecationReason": None,
                                "isDeprecated": False,
                            },
                        ],
                    },
                    {
                        "kind": "UNION",
                        "name": "Mixed",
                        "inputFields": None,
                        "interfaces": None,
                        "possibleTypes": [
                            {"name": "Dog", "ofType": None, "kind": "OBJECT"},
                            {
                                "kind": "OBJECT",
                                "name": "Human",
                                "ofType": None,
                            },
                        ],
                        "fields": None,
                        "enumValues": None,
                    },
                    {
                        "kind": "INPUT_OBJECT",
                        "name": "EatSomething",
                        "inputFields": [
                            {
                                "type": {
                                    "name": "String",
                                    "kind": "SCALAR",
                                    "ofType": None,
                                },
                                "name": "quantity",
                                "defaultValue": None,
                            }
                        ],
                        "interfaces": None,
                        "possibleTypes": None,
                        "fields": None,
                        "enumValues": None,
                    },
                    {
                        "kind": "SCALAR",
                        "name": "Boolean",
                        "inputFields": None,
                        "interfaces": None,
                        "possibleTypes": None,
                        "fields": None,
                        "enumValues": None,
                    },
                    {
                        "kind": "SCALAR",
                        "name": "Date",
                        "inputFields": None,
                        "interfaces": None,
                        "possibleTypes": None,
                        "fields": None,
                        "enumValues": None,
                    },
                    {
                        "kind": "SCALAR",
                        "name": "DateTime",
                        "inputFields": None,
                        "interfaces": None,
                        "possibleTypes": None,
                        "fields": None,
                        "enumValues": None,
                    },
                    {
                        "kind": "SCALAR",
                        "name": "Float",
                        "inputFields": None,
                        "interfaces": None,
                        "possibleTypes": None,
                        "fields": None,
                        "enumValues": None,
                    },
                    {
                        "kind": "SCALAR",
                        "name": "ID",
                        "inputFields": None,
                        "interfaces": None,
                        "possibleTypes": None,
                        "fields": None,
                        "enumValues": None,
                    },
                    {
                        "kind": "SCALAR",
                        "name": "Int",
                        "inputFields": None,
                        "interfaces": None,
                        "possibleTypes": None,
                        "fields": None,
                        "enumValues": None,
                    },
                    {
                        "kind": "SCALAR",
                        "name": "String",
                        "inputFields": None,
                        "interfaces": None,
                        "possibleTypes": None,
                        "fields": None,
                        "enumValues": None,
                    },
                    {
                        "kind": "SCALAR",
                        "name": "Time",
                        "inputFields": None,
                        "interfaces": None,
                        "possibleTypes": None,
                        "fields": None,
                        "enumValues": None,
                    },
                ],
            }
        }
    }
