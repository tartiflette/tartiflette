import pytest

from tartiflette import create_engine

_SDL = """
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
"""


@pytest.fixture(scope="module")
async def ttftt_engine():
    return await create_engine(sdl=_SDL, schema_name="test_issue92")


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
async def test_issue92_fragment_inordered(ttftt_engine):
    results = await ttftt_engine.execute(
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
                        "fields": [
                            {
                                "name": "name",
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
                                "isDeprecated": False,
                                "deprecationReason": None,
                            }
                        ],
                        "inputFields": None,
                        "interfaces": None,
                        "enumValues": None,
                        "possibleTypes": [
                            {"kind": "OBJECT", "name": "Human", "ofType": None}
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
                                    "name": None,
                                    "ofType": {
                                        "kind": "SCALAR",
                                        "name": "String",
                                        "ofType": None,
                                    },
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            }
                        ],
                        "inputFields": None,
                        "interfaces": None,
                        "enumValues": None,
                        "possibleTypes": [
                            {"kind": "OBJECT", "name": "Dog", "ofType": None}
                        ],
                    },
                    {
                        "kind": "OBJECT",
                        "name": "Human",
                        "fields": [
                            {
                                "name": "name",
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
                                "isDeprecated": False,
                                "deprecationReason": None,
                            }
                        ],
                        "inputFields": None,
                        "interfaces": [
                            {
                                "kind": "INTERFACE",
                                "name": "Sentient",
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
                                "name": "name",
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
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "owner",
                                "args": [],
                                "type": {
                                    "kind": "OBJECT",
                                    "name": "Human",
                                    "ofType": None,
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                        ],
                        "inputFields": None,
                        "interfaces": [
                            {
                                "kind": "INTERFACE",
                                "name": "Pet",
                                "ofType": None,
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
                                "name": "id",
                                "args": [],
                                "type": {
                                    "kind": "SCALAR",
                                    "name": "String",
                                    "ofType": None,
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            }
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
                                "name": "dog",
                                "args": [],
                                "type": {
                                    "kind": "OBJECT",
                                    "name": "Dog",
                                    "ofType": None,
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "sentient",
                                "args": [],
                                "type": {
                                    "kind": "UNION",
                                    "name": "Mixed",
                                    "ofType": None,
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
                        "name": "Mutation",
                        "fields": [
                            {
                                "name": "mutateDog",
                                "args": [],
                                "type": {
                                    "kind": "OBJECT",
                                    "name": "MutateDogPayload",
                                    "ofType": None,
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            }
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
                                "name": "quantity",
                                "type": {
                                    "kind": "SCALAR",
                                    "name": "String",
                                    "ofType": None,
                                },
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
                ],
                "directives": [
                    {
                        "name": "deprecated",
                        "locations": ["FIELD_DEFINITION", "ENUM_VALUE"],
                        "args": [
                            {
                                "name": "reason",
                                "type": {
                                    "kind": "SCALAR",
                                    "name": "String",
                                    "ofType": None,
                                },
                                "defaultValue": '"No longer supported"',
                            }
                        ],
                    },
                    {
                        "name": "nonIntrospectable",
                        "locations": ["FIELD_DEFINITION", "SCHEMA"],
                        "args": [],
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
                                "name": "if",
                                "type": {
                                    "kind": "NON_NULL",
                                    "name": None,
                                    "ofType": {
                                        "kind": "SCALAR",
                                        "name": "Boolean",
                                        "ofType": None,
                                    },
                                },
                                "defaultValue": None,
                            }
                        ],
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
                                "name": "if",
                                "type": {
                                    "kind": "NON_NULL",
                                    "name": None,
                                    "ofType": {
                                        "kind": "SCALAR",
                                        "name": "Boolean",
                                        "ofType": None,
                                    },
                                },
                                "defaultValue": None,
                            }
                        ],
                    },
                ],
            }
        }
    }
