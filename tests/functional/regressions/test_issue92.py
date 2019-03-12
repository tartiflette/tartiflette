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
                "directives": [
                    {
                        "args": [
                            {
                                "name": "reason",
                                "defaultValue": "Deprecated",
                                "type": {
                                    "ofType": None,
                                    "name": "String",
                                    "kind": "SCALAR",
                                },
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
                                "isDeprecated": False,
                                "args": [],
                                "deprecationReason": None,
                                "name": "name",
                                "type": {
                                    "ofType": {
                                        "name": "String",
                                        "kind": "SCALAR",
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
                        "kind": "INTERFACE",
                        "name": "Pet",
                        "inputFields": None,
                        "interfaces": None,
                        "possibleTypes": [
                            {"ofType": None, "name": "Dog", "kind": "OBJECT"}
                        ],
                        "fields": [
                            {
                                "name": "name",
                                "args": [],
                                "type": {
                                    "name": None,
                                    "ofType": {
                                        "ofType": None,
                                        "kind": "SCALAR",
                                        "name": "String",
                                    },
                                    "kind": "NON_NULL",
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
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
                                "ofType": None,
                                "name": "Pet",
                                "kind": "INTERFACE",
                            }
                        ],
                        "possibleTypes": None,
                        "fields": [
                            {
                                "args": [],
                                "deprecationReason": None,
                                "name": "name",
                                "type": {
                                    "kind": "NON_NULL",
                                    "ofType": {
                                        "ofType": None,
                                        "kind": "SCALAR",
                                        "name": "String",
                                    },
                                    "name": None,
                                },
                                "isDeprecated": False,
                            },
                            {
                                "name": "owner",
                                "isDeprecated": False,
                                "args": [],
                                "deprecationReason": None,
                                "type": {
                                    "ofType": None,
                                    "name": "Human",
                                    "kind": "OBJECT",
                                },
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
                                "name": "id",
                                "type": {
                                    "ofType": None,
                                    "name": "String",
                                    "kind": "SCALAR",
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
                        "name": "Query",
                        "inputFields": None,
                        "interfaces": [],
                        "possibleTypes": None,
                        "fields": [
                            {
                                "name": "dog",
                                "type": {
                                    "ofType": None,
                                    "name": "Dog",
                                    "kind": "OBJECT",
                                },
                                "isDeprecated": False,
                                "args": [],
                                "deprecationReason": None,
                            },
                            {
                                "type": {
                                    "ofType": None,
                                    "name": "Mixed",
                                    "kind": "UNION",
                                },
                                "name": "sentient",
                                "args": [],
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                        ],
                        "enumValues": None,
                    },
                    {
                        "kind": "OBJECT",
                        "name": "Mutation",
                        "inputFields": None,
                        "interfaces": [],
                        "possibleTypes": None,
                        "fields": [
                            {
                                "isDeprecated": False,
                                "args": [],
                                "deprecationReason": None,
                                "name": "mutateDog",
                                "type": {
                                    "ofType": None,
                                    "name": "MutateDogPayload",
                                    "kind": "OBJECT",
                                },
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
                                "name": "Value1",
                                "deprecationReason": None,
                                "isDeprecated": False,
                            },
                            {
                                "isDeprecated": True,
                                "name": "Value2",
                                "deprecationReason": "Unused anymore",
                            },
                            {
                                "isDeprecated": False,
                                "name": "Value3",
                                "deprecationReason": None,
                            },
                        ],
                    },
                    {
                        "kind": "UNION",
                        "name": "Mixed",
                        "inputFields": None,
                        "interfaces": None,
                        "possibleTypes": [
                            {"kind": "OBJECT", "name": "Dog", "ofType": None},
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
                        "name": "Boolean",
                        "inputFields": None,
                        "interfaces": None,
                        "possibleTypes": None,
                        "kind": "SCALAR",
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
                        "possibleTypes": None,
                        "interfaces": None,
                        "kind": "SCALAR",
                        "name": "String",
                        "inputFields": None,
                        "enumValues": None,
                        "fields": None,
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
