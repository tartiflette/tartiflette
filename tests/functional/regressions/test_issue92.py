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
                            {"ofType": None, "name": "Human", "kind": "OBJECT"}
                        ],
                        "fields": [],
                        "enumValues": None,
                    },
                    {
                        "kind": "INTERFACE",
                        "name": "Pet",
                        "inputFields": None,
                        "interfaces": None,
                        "possibleTypes": [
                            {"name": "Dog", "kind": "OBJECT", "ofType": None}
                        ],
                        "fields": [],
                        "enumValues": None,
                    },
                    {
                        "kind": "OBJECT",
                        "name": "Human",
                        "inputFields": None,
                        "interfaces": [
                            {
                                "kind": "INTERFACE",
                                "ofType": None,
                                "name": "Sentient",
                            }
                        ],
                        "possibleTypes": None,
                        "fields": [
                            {
                                "args": [],
                                "deprecationReason": None,
                                "name": "name",
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
                            }
                        ],
                        "enumValues": None,
                    },
                    {
                        "possibleTypes": None,
                        "kind": "OBJECT",
                        "name": "Dog",
                        "inputFields": None,
                        "interfaces": [
                            {
                                "kind": "INTERFACE",
                                "ofType": None,
                                "name": "Pet",
                            }
                        ],
                        "enumValues": None,
                        "fields": [
                            {
                                "deprecationReason": None,
                                "name": "name",
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
                                "args": [],
                            },
                            {
                                "args": [],
                                "isDeprecated": False,
                                "deprecationReason": None,
                                "type": {
                                    "name": "Human",
                                    "kind": "OBJECT",
                                    "ofType": None,
                                },
                                "name": "owner",
                            },
                        ],
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
                                    "kind": "SCALAR",
                                    "ofType": None,
                                },
                                "isDeprecated": False,
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
                                "args": [],
                                "deprecationReason": None,
                                "name": "dog",
                                "type": {
                                    "name": "Dog",
                                    "kind": "OBJECT",
                                    "ofType": None,
                                },
                                "isDeprecated": False,
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
                                "type": {
                                    "name": "MutateDogPayload",
                                    "kind": "OBJECT",
                                    "ofType": None,
                                },
                                "isDeprecated": False,
                                "args": [],
                                "deprecationReason": None,
                                "name": "mutateDog",
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
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "isDeprecated": True,
                                "deprecationReason": "Unused anymore",
                                "name": "Value2",
                            },
                            {
                                "deprecationReason": None,
                                "name": "Value3",
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
                            {"kind": "OBJECT", "name": "Dog", "ofType": None},
                            {
                                "name": "Human",
                                "ofType": None,
                                "kind": "OBJECT",
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
                        "possibleTypes": None,
                        "fields": None,
                        "enumValues": None,
                    },
                    {
                        "inputFields": None,
                        "interfaces": None,
                        "possibleTypes": None,
                        "kind": "SCALAR",
                        "name": "Boolean",
                        "enumValues": None,
                        "fields": None,
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
                ],
            }
        }
    }
