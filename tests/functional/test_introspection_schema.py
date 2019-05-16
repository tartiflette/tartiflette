import pytest


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(name="pets")
@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
            {
              __typename
              __schema {
                __typename
                directives {
                  __typename
                  name
                  description
                  locations
                  args {
                    __typename
                    name
                    description
                    type {
                      __typename
                      kind
                      name
                      description
                      fields {
                        __typename
                        name
                        description
                        args {
                          __typename
                          name
                          description
                          defaultValue
                        }
                        type {
                          __typename
                          kind
                          name
                          description
                        }
                        isDeprecated
                        deprecationReason
                      }
                      interfaces {
                        __typename
                        kind
                        name
                        description
                      }
                      possibleTypes {
                        __typename
                        kind
                        name
                        description
                      }
                      enumValues {
                        __typename
                        name
                        description
                        isDeprecated
                        deprecationReason
                      }
                      inputFields {
                        __typename
                        name
                        description
                        defaultValue
                      }
                    }
                    defaultValue
                  }
                }
              }
            }
            """,
            {
                "data": {
                    "__typename": "MyQuery",
                    "__schema": {
                        "__typename": "__Schema",
                        "directives": [
                            {
                                "__typename": "__Directive",
                                "name": "deprecated",
                                "description": "Marks an element of a GraphQL schema as no longer supported.",
                                "locations": [
                                    "FIELD_DEFINITION",
                                    "ENUM_VALUE",
                                ],
                                "args": [
                                    {
                                        "__typename": "__InputValue",
                                        "name": "reason",
                                        "description": "Explains why this element was deprecated, usually also including a suggestion for how to access supported similar data. Formatted using the Markdown syntax (as specified by [CommonMark](https://commonmark.org/).",
                                        "type": {
                                            "__typename": "__Type",
                                            "kind": "SCALAR",
                                            "name": "String",
                                            "description": None,
                                            "fields": None,
                                            "interfaces": None,
                                            "possibleTypes": None,
                                            "enumValues": None,
                                            "inputFields": None,
                                        },
                                        "defaultValue": "No longer supported",
                                    }
                                ],
                            },
                            {
                                "__typename": "__Directive",
                                "name": "nonIntrospectable",
                                "description": "Directs the executor to hide the element on introspection queries.",
                                "locations": ["FIELD_DEFINITION"],
                                "args": [],
                            },
                            {
                                "__typename": "__Directive",
                                "name": "skip",
                                "description": "Directs the executor to skip this field or fragment when the `if` argument is true.",
                                "locations": [
                                    "FIELD",
                                    "FRAGMENT_SPREAD",
                                    "INLINE_FRAGMENT",
                                ],
                                "args": [
                                    {
                                        "__typename": "__InputValue",
                                        "name": "if",
                                        "description": "Skipped when true.",
                                        "type": {
                                            "__typename": "__Type",
                                            "kind": "NON_NULL",
                                            "name": None,
                                            "description": None,
                                            "fields": None,
                                            "interfaces": None,
                                            "possibleTypes": None,
                                            "enumValues": None,
                                            "inputFields": None,
                                        },
                                        "defaultValue": None,
                                    }
                                ],
                            },
                            {
                                "__typename": "__Directive",
                                "name": "include",
                                "description": "Directs the executor to include this field or fragment only when the `if` argument is true.",
                                "locations": [
                                    "FIELD",
                                    "FRAGMENT_SPREAD",
                                    "INLINE_FRAGMENT",
                                ],
                                "args": [
                                    {
                                        "__typename": "__InputValue",
                                        "name": "if",
                                        "description": "Included when true.",
                                        "type": {
                                            "__typename": "__Type",
                                            "kind": "NON_NULL",
                                            "name": None,
                                            "description": None,
                                            "fields": None,
                                            "interfaces": None,
                                            "possibleTypes": None,
                                            "enumValues": None,
                                            "inputFields": None,
                                        },
                                        "defaultValue": None,
                                    }
                                ],
                            },
                        ],
                    },
                }
            },
        ),
        (
            """
            {
              __typename
              __schema {
                __typename
                queryType {
                  __typename
                  kind
                  name
                  description
                  fields {
                    __typename
                    name
                    description
                    args {
                      __typename
                      name
                      description
                      defaultValue
                    }
                    type {
                      __typename
                      kind
                      name
                      description
                    }
                    isDeprecated
                    deprecationReason
                  }
                  interfaces {
                    __typename
                    kind
                    name
                    description
                  }
                  possibleTypes {
                    __typename
                    kind
                    name
                    description
                  }
                  enumValues {
                    __typename
                    name
                    description
                    isDeprecated
                    deprecationReason
                  }
                  inputFields {
                    __typename
                    name
                    description
                    defaultValue
                  }
                  ofType {
                    __typename
                    kind
                    name
                    description
                  }
                }
              }
            }
            """,
            {
                "data": {
                    "__typename": "MyQuery",
                    "__schema": {
                        "__typename": "__Schema",
                        "queryType": {
                            "__typename": "__Type",
                            "kind": "OBJECT",
                            "name": "MyQuery",
                            "description": "Custom Query type.",
                            "fields": [
                                {
                                    "__typename": "__Field",
                                    "name": "version",
                                    "description": None,
                                    "args": [],
                                    "type": {
                                        "__typename": "__Type",
                                        "kind": "NON_NULL",
                                        "name": None,
                                        "description": None,
                                    },
                                    "isDeprecated": False,
                                    "deprecationReason": None,
                                },
                                {
                                    "__typename": "__Field",
                                    "name": "serviceStatus",
                                    "description": "Service status.",
                                    "args": [],
                                    "type": {
                                        "__typename": "__Type",
                                        "kind": "NON_NULL",
                                        "name": None,
                                        "description": None,
                                    },
                                    "isDeprecated": False,
                                    "deprecationReason": None,
                                },
                                {
                                    "__typename": "__Field",
                                    "name": "human",
                                    "description": None,
                                    "args": [
                                        {
                                            "__typename": "__InputValue",
                                            "name": "id",
                                            "description": "Human identifier to fetch.",
                                            "defaultValue": None,
                                        }
                                    ],
                                    "type": {
                                        "__typename": "__Type",
                                        "kind": "OBJECT",
                                        "name": "Human",
                                        "description": None,
                                    },
                                    "isDeprecated": False,
                                    "deprecationReason": None,
                                },
                                {
                                    "__typename": "__Field",
                                    "name": "humans",
                                    "description": None,
                                    "args": [
                                        {
                                            "__typename": "__InputValue",
                                            "name": "filters",
                                            "description": None,
                                            "defaultValue": None,
                                        },
                                        {
                                            "__typename": "__InputValue",
                                            "name": "order",
                                            "description": None,
                                            "defaultValue": None,
                                        },
                                    ],
                                    "type": {
                                        "__typename": "__Type",
                                        "kind": "LIST",
                                        "name": None,
                                        "description": None,
                                    },
                                    "isDeprecated": False,
                                    "deprecationReason": None,
                                },
                                {
                                    "__typename": "__Field",
                                    "name": "pet",
                                    "description": None,
                                    "args": [
                                        {
                                            "__typename": "__InputValue",
                                            "name": "id",
                                            "description": None,
                                            "defaultValue": None,
                                        }
                                    ],
                                    "type": {
                                        "__typename": "__Type",
                                        "kind": "UNION",
                                        "name": "Pet",
                                        "description": None,
                                    },
                                    "isDeprecated": False,
                                    "deprecationReason": None,
                                },
                                {
                                    "__typename": "__Field",
                                    "name": "pets",
                                    "description": None,
                                    "args": [
                                        {
                                            "__typename": "__InputValue",
                                            "name": "filters",
                                            "description": None,
                                            "defaultValue": None,
                                        },
                                        {
                                            "__typename": "__InputValue",
                                            "name": "order",
                                            "description": None,
                                            "defaultValue": None,
                                        },
                                    ],
                                    "type": {
                                        "__typename": "__Type",
                                        "kind": "LIST",
                                        "name": None,
                                        "description": None,
                                    },
                                    "isDeprecated": False,
                                    "deprecationReason": None,
                                },
                            ],
                            "interfaces": None,
                            "possibleTypes": None,
                            "enumValues": None,
                            "inputFields": None,
                            "ofType": None,
                        },
                    },
                }
            },
        ),
        (
            """
            {
              __typename
              __schema {
                __typename
                mutationType {
                  __typename
                  kind
                  name
                  description
                  fields {
                    __typename
                    name
                    description
                    args {
                      __typename
                      name
                      description
                      defaultValue
                    }
                    type {
                      __typename
                      kind
                      name
                      description
                    }
                    isDeprecated
                    deprecationReason
                  }
                  interfaces {
                    __typename
                    kind
                    name
                    description
                  }
                  possibleTypes {
                    __typename
                    kind
                    name
                    description
                  }
                  enumValues {
                    __typename
                    name
                    description
                    isDeprecated
                    deprecationReason
                  }
                  inputFields {
                    __typename
                    name
                    description
                    defaultValue
                  }
                  ofType {
                    __typename
                    kind
                    name
                    description
                  }
                }
              }
            }
            """,
            {
                "data": {
                    "__typename": "MyQuery",
                    "__schema": {
                        "__typename": "__Schema",
                        "mutationType": {
                            "__typename": "__Type",
                            "kind": "OBJECT",
                            "name": "MyMutation",
                            "description": "Custom Mutation type.",
                            "fields": [
                                {
                                    "__typename": "__Field",
                                    "name": "addHuman",
                                    "description": None,
                                    "args": [
                                        {
                                            "__typename": "__InputValue",
                                            "name": "input",
                                            "description": None,
                                            "defaultValue": None,
                                        }
                                    ],
                                    "type": {
                                        "__typename": "__Type",
                                        "kind": "NON_NULL",
                                        "name": None,
                                        "description": None,
                                    },
                                    "isDeprecated": False,
                                    "deprecationReason": None,
                                },
                                {
                                    "__typename": "__Field",
                                    "name": "addCat",
                                    "description": None,
                                    "args": [
                                        {
                                            "__typename": "__InputValue",
                                            "name": "input",
                                            "description": None,
                                            "defaultValue": None,
                                        }
                                    ],
                                    "type": {
                                        "__typename": "__Type",
                                        "kind": "NON_NULL",
                                        "name": None,
                                        "description": None,
                                    },
                                    "isDeprecated": False,
                                    "deprecationReason": None,
                                },
                                {
                                    "__typename": "__Field",
                                    "name": "addDog",
                                    "description": None,
                                    "args": [
                                        {
                                            "__typename": "__InputValue",
                                            "name": "input",
                                            "description": None,
                                            "defaultValue": None,
                                        }
                                    ],
                                    "type": {
                                        "__typename": "__Type",
                                        "kind": "NON_NULL",
                                        "name": None,
                                        "description": None,
                                    },
                                    "isDeprecated": False,
                                    "deprecationReason": None,
                                },
                            ],
                            "interfaces": None,
                            "possibleTypes": None,
                            "enumValues": None,
                            "inputFields": None,
                            "ofType": None,
                        },
                    },
                }
            },
        ),
        (
            """
            {
              __typename
              __schema {
                __typename
                subscriptionType {
                  __typename
                  kind
                  name
                  description
                  fields {
                    __typename
                    name
                    description
                    args {
                      __typename
                      name
                      description
                      defaultValue
                    }
                    type {
                      __typename
                      kind
                      name
                      description
                    }
                    isDeprecated
                    deprecationReason
                  }
                  interfaces {
                    __typename
                    kind
                    name
                    description
                  }
                  possibleTypes {
                    __typename
                    kind
                    name
                    description
                  }
                  enumValues {
                    __typename
                    name
                    description
                    isDeprecated
                    deprecationReason
                  }
                  inputFields {
                    __typename
                    name
                    description
                    defaultValue
                  }
                  ofType {
                    __typename
                    kind
                    name
                    description
                  }
                }
              }
            }
            """,
            {
                "data": {
                    "__typename": "MyQuery",
                    "__schema": {
                        "__typename": "__Schema",
                        "subscriptionType": {
                            "__typename": "__Type",
                            "kind": "OBJECT",
                            "name": "MySubscription",
                            "description": "Custom Subscription type.",
                            "fields": [
                                {
                                    "__typename": "__Field",
                                    "name": "humanAdded",
                                    "description": None,
                                    "args": [],
                                    "type": {
                                        "__typename": "__Type",
                                        "kind": "NON_NULL",
                                        "name": None,
                                        "description": None,
                                    },
                                    "isDeprecated": False,
                                    "deprecationReason": None,
                                },
                                {
                                    "__typename": "__Field",
                                    "name": "petAdded",
                                    "description": None,
                                    "args": [
                                        {
                                            "__typename": "__InputValue",
                                            "name": "kind",
                                            "description": None,
                                            "defaultValue": None,
                                        }
                                    ],
                                    "type": {
                                        "__typename": "__Type",
                                        "kind": "NON_NULL",
                                        "name": None,
                                        "description": None,
                                    },
                                    "isDeprecated": False,
                                    "deprecationReason": None,
                                },
                            ],
                            "interfaces": None,
                            "possibleTypes": None,
                            "enumValues": None,
                            "inputFields": None,
                            "ofType": None,
                        },
                    },
                }
            },
        ),
        (
            """
            {
              __typename
              __schema {
                __typename
                types {
                  __typename
                  kind
                  name
                  description
                  fields {
                    __typename
                    name
                    description
                    args {
                      __typename
                      name
                      description
                      defaultValue
                    }
                    type {
                      __typename
                      kind
                      name
                      description
                    }
                    isDeprecated
                    deprecationReason
                  }
                  interfaces {
                    __typename
                    kind
                    name
                    description
                  }
                  possibleTypes {
                    __typename
                    kind
                    name
                    description
                  }
                  enumValues {
                    __typename
                    name
                    description
                    isDeprecated
                    deprecationReason
                  }
                  inputFields {
                    __typename
                    name
                    description
                    defaultValue
                  }
                  ofType {
                    __typename
                    kind
                    name
                    description
                  }
                }
              }
            }
            """,
            {
                "data": {
                    "__typename": "MyQuery",
                    "__schema": {
                        "__typename": "__Schema",
                        "types": [
                            {
                                "__typename": "__Type",
                                "kind": "INTERFACE",
                                "name": "Identifiable",
                                "description": None,
                                "fields": [
                                    {
                                        "__typename": "__Field",
                                        "name": "id",
                                        "description": None,
                                        "args": [],
                                        "type": {
                                            "__typename": "__Type",
                                            "kind": "NON_NULL",
                                            "name": None,
                                            "description": None,
                                        },
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    }
                                ],
                                "interfaces": None,
                                "possibleTypes": [
                                    {
                                        "__typename": "__Type",
                                        "kind": "OBJECT",
                                        "name": "Human",
                                        "description": None,
                                    },
                                    {
                                        "__typename": "__Type",
                                        "kind": "OBJECT",
                                        "name": "Cat",
                                        "description": None,
                                    },
                                    {
                                        "__typename": "__Type",
                                        "kind": "OBJECT",
                                        "name": "Dog",
                                        "description": None,
                                    },
                                ],
                                "enumValues": None,
                                "inputFields": None,
                                "ofType": None,
                            },
                            {
                                "__typename": "__Type",
                                "kind": "INTERFACE",
                                "name": "Named",
                                "description": None,
                                "fields": [
                                    {
                                        "__typename": "__Field",
                                        "name": "name",
                                        "description": None,
                                        "args": [],
                                        "type": {
                                            "__typename": "__Type",
                                            "kind": "NON_NULL",
                                            "name": None,
                                            "description": None,
                                        },
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    }
                                ],
                                "interfaces": None,
                                "possibleTypes": [
                                    {
                                        "__typename": "__Type",
                                        "kind": "OBJECT",
                                        "name": "Human",
                                        "description": None,
                                    },
                                    {
                                        "__typename": "__Type",
                                        "kind": "OBJECT",
                                        "name": "Cat",
                                        "description": None,
                                    },
                                    {
                                        "__typename": "__Type",
                                        "kind": "OBJECT",
                                        "name": "Dog",
                                        "description": None,
                                    },
                                ],
                                "enumValues": None,
                                "inputFields": None,
                                "ofType": None,
                            },
                            {
                                "__typename": "__Type",
                                "kind": "INTERFACE",
                                "name": "Nicknamed",
                                "description": None,
                                "fields": [
                                    {
                                        "__typename": "__Field",
                                        "name": "nickname",
                                        "description": None,
                                        "args": [],
                                        "type": {
                                            "__typename": "__Type",
                                            "kind": "SCALAR",
                                            "name": "String",
                                            "description": "The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.",
                                        },
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    }
                                ],
                                "interfaces": None,
                                "possibleTypes": [
                                    {
                                        "__typename": "__Type",
                                        "kind": "OBJECT",
                                        "name": "Cat",
                                        "description": None,
                                    },
                                    {
                                        "__typename": "__Type",
                                        "kind": "OBJECT",
                                        "name": "Dog",
                                        "description": None,
                                    },
                                ],
                                "enumValues": None,
                                "inputFields": None,
                                "ofType": None,
                            },
                            {
                                "__typename": "__Type",
                                "kind": "INTERFACE",
                                "name": "Owned",
                                "description": None,
                                "fields": [
                                    {
                                        "__typename": "__Field",
                                        "name": "owner",
                                        "description": None,
                                        "args": [],
                                        "type": {
                                            "__typename": "__Type",
                                            "kind": "OBJECT",
                                            "name": "Human",
                                            "description": None,
                                        },
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    }
                                ],
                                "interfaces": None,
                                "possibleTypes": [
                                    {
                                        "__typename": "__Type",
                                        "kind": "OBJECT",
                                        "name": "Cat",
                                        "description": None,
                                    },
                                    {
                                        "__typename": "__Type",
                                        "kind": "OBJECT",
                                        "name": "Dog",
                                        "description": None,
                                    },
                                ],
                                "enumValues": None,
                                "inputFields": None,
                                "ofType": None,
                            },
                            {
                                "__typename": "__Type",
                                "kind": "INTERFACE",
                                "name": "Birthdated",
                                "description": "Interface for type with birthdate.",
                                "fields": [
                                    {
                                        "__typename": "__Field",
                                        "name": "birthdate",
                                        "description": "Date representing a birthdate.",
                                        "args": [],
                                        "type": {
                                            "__typename": "__Type",
                                            "kind": "NON_NULL",
                                            "name": None,
                                            "description": None,
                                        },
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    }
                                ],
                                "interfaces": None,
                                "possibleTypes": [
                                    {
                                        "__typename": "__Type",
                                        "kind": "OBJECT",
                                        "name": "Cat",
                                        "description": None,
                                    },
                                    {
                                        "__typename": "__Type",
                                        "kind": "OBJECT",
                                        "name": "Dog",
                                        "description": None,
                                    },
                                ],
                                "enumValues": None,
                                "inputFields": None,
                                "ofType": None,
                            },
                            {
                                "__typename": "__Type",
                                "kind": "ENUM",
                                "name": "ServiceStatus",
                                "description": "States of the service.",
                                "fields": None,
                                "interfaces": None,
                                "possibleTypes": None,
                                "enumValues": [
                                    {
                                        "__typename": "__EnumValue",
                                        "name": "UP",
                                        "description": "Everything works well.",
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                    {
                                        "__typename": "__EnumValue",
                                        "name": "IN_TROUBLE",
                                        "description": None,
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                    {
                                        "__typename": "__EnumValue",
                                        "name": "DOWN",
                                        "description": None,
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                ],
                                "inputFields": None,
                                "ofType": None,
                            },
                            {
                                "__typename": "__Type",
                                "kind": "ENUM",
                                "name": "PetKind",
                                "description": None,
                                "fields": None,
                                "interfaces": None,
                                "possibleTypes": None,
                                "enumValues": [
                                    {
                                        "__typename": "__EnumValue",
                                        "name": "CAT",
                                        "description": None,
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                    {
                                        "__typename": "__EnumValue",
                                        "name": "DOG",
                                        "description": None,
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                ],
                                "inputFields": None,
                                "ofType": None,
                            },
                            {
                                "__typename": "__Type",
                                "kind": "ENUM",
                                "name": "CatCommand",
                                "description": None,
                                "fields": None,
                                "interfaces": None,
                                "possibleTypes": None,
                                "enumValues": [
                                    {
                                        "__typename": "__EnumValue",
                                        "name": "JUMP",
                                        "description": None,
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    }
                                ],
                                "inputFields": None,
                                "ofType": None,
                            },
                            {
                                "__typename": "__Type",
                                "kind": "ENUM",
                                "name": "DogCommand",
                                "description": None,
                                "fields": None,
                                "interfaces": None,
                                "possibleTypes": None,
                                "enumValues": [
                                    {
                                        "__typename": "__EnumValue",
                                        "name": "SIT",
                                        "description": None,
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                    {
                                        "__typename": "__EnumValue",
                                        "name": "DOWN",
                                        "description": None,
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                    {
                                        "__typename": "__EnumValue",
                                        "name": "HEEL",
                                        "description": None,
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                ],
                                "inputFields": None,
                                "ofType": None,
                            },
                            {
                                "__typename": "__Type",
                                "kind": "ENUM",
                                "name": "OrderDirection",
                                "description": None,
                                "fields": None,
                                "interfaces": None,
                                "possibleTypes": None,
                                "enumValues": [
                                    {
                                        "__typename": "__EnumValue",
                                        "name": "ASC",
                                        "description": None,
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                    {
                                        "__typename": "__EnumValue",
                                        "name": "DESC",
                                        "description": None,
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                ],
                                "inputFields": None,
                                "ofType": None,
                            },
                            {
                                "__typename": "__Type",
                                "kind": "ENUM",
                                "name": "HumanOrderField",
                                "description": None,
                                "fields": None,
                                "interfaces": None,
                                "possibleTypes": None,
                                "enumValues": [
                                    {
                                        "__typename": "__EnumValue",
                                        "name": "IDENTIFIER",
                                        "description": None,
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                    {
                                        "__typename": "__EnumValue",
                                        "name": "NAME",
                                        "description": None,
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                ],
                                "inputFields": None,
                                "ofType": None,
                            },
                            {
                                "__typename": "__Type",
                                "kind": "ENUM",
                                "name": "PetOrderField",
                                "description": None,
                                "fields": None,
                                "interfaces": None,
                                "possibleTypes": None,
                                "enumValues": [
                                    {
                                        "__typename": "__EnumValue",
                                        "name": "IDENTIFIER",
                                        "description": None,
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                    {
                                        "__typename": "__EnumValue",
                                        "name": "NAME",
                                        "description": None,
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                    {
                                        "__typename": "__EnumValue",
                                        "name": "NICKNAME",
                                        "description": None,
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                ],
                                "inputFields": None,
                                "ofType": None,
                            },
                            {
                                "__typename": "__Type",
                                "kind": "UNION",
                                "name": "Pet",
                                "description": None,
                                "fields": None,
                                "interfaces": None,
                                "possibleTypes": [
                                    {
                                        "__typename": "__Type",
                                        "kind": "OBJECT",
                                        "name": "Cat",
                                        "description": None,
                                    },
                                    {
                                        "__typename": "__Type",
                                        "kind": "OBJECT",
                                        "name": "Dog",
                                        "description": None,
                                    },
                                ],
                                "enumValues": None,
                                "inputFields": None,
                                "ofType": None,
                            },
                            {
                                "__typename": "__Type",
                                "kind": "UNION",
                                "name": "PetOrHuman",
                                "description": None,
                                "fields": None,
                                "interfaces": None,
                                "possibleTypes": [
                                    {
                                        "__typename": "__Type",
                                        "kind": "OBJECT",
                                        "name": "Cat",
                                        "description": None,
                                    },
                                    {
                                        "__typename": "__Type",
                                        "kind": "OBJECT",
                                        "name": "Dog",
                                        "description": None,
                                    },
                                    {
                                        "__typename": "__Type",
                                        "kind": "OBJECT",
                                        "name": "Human",
                                        "description": None,
                                    },
                                ],
                                "enumValues": None,
                                "inputFields": None,
                                "ofType": None,
                            },
                            {
                                "__typename": "__Type",
                                "kind": "INPUT_OBJECT",
                                "name": "HumanOrder",
                                "description": None,
                                "fields": None,
                                "interfaces": None,
                                "possibleTypes": None,
                                "enumValues": None,
                                "inputFields": [
                                    {
                                        "__typename": "__InputValue",
                                        "name": "field",
                                        "description": None,
                                        "defaultValue": None,
                                    },
                                    {
                                        "__typename": "__InputValue",
                                        "name": "direction",
                                        "description": None,
                                        "defaultValue": None,
                                    },
                                ],
                                "ofType": None,
                            },
                            {
                                "__typename": "__Type",
                                "kind": "INPUT_OBJECT",
                                "name": "PetOrder",
                                "description": None,
                                "fields": None,
                                "interfaces": None,
                                "possibleTypes": None,
                                "enumValues": None,
                                "inputFields": [
                                    {
                                        "__typename": "__InputValue",
                                        "name": "field",
                                        "description": None,
                                        "defaultValue": None,
                                    },
                                    {
                                        "__typename": "__InputValue",
                                        "name": "direction",
                                        "description": None,
                                        "defaultValue": None,
                                    },
                                ],
                                "ofType": None,
                            },
                            {
                                "__typename": "__Type",
                                "kind": "INPUT_OBJECT",
                                "name": "HumanFilters",
                                "description": None,
                                "fields": None,
                                "interfaces": None,
                                "possibleTypes": None,
                                "enumValues": None,
                                "inputFields": [
                                    {
                                        "__typename": "__InputValue",
                                        "name": "ids",
                                        "description": None,
                                        "defaultValue": None,
                                    },
                                    {
                                        "__typename": "__InputValue",
                                        "name": "name",
                                        "description": None,
                                        "defaultValue": None,
                                    },
                                    {
                                        "__typename": "__InputValue",
                                        "name": "hasFriends",
                                        "description": None,
                                        "defaultValue": None,
                                    },
                                ],
                                "ofType": None,
                            },
                            {
                                "__typename": "__Type",
                                "kind": "INPUT_OBJECT",
                                "name": "PetFilters",
                                "description": None,
                                "fields": None,
                                "interfaces": None,
                                "possibleTypes": None,
                                "enumValues": None,
                                "inputFields": [
                                    {
                                        "__typename": "__InputValue",
                                        "name": "ids",
                                        "description": None,
                                        "defaultValue": None,
                                    },
                                    {
                                        "__typename": "__InputValue",
                                        "name": "kind",
                                        "description": None,
                                        "defaultValue": None,
                                    },
                                    {
                                        "__typename": "__InputValue",
                                        "name": "name",
                                        "description": None,
                                        "defaultValue": None,
                                    },
                                    {
                                        "__typename": "__InputValue",
                                        "name": "nickname",
                                        "description": None,
                                        "defaultValue": None,
                                    },
                                    {
                                        "__typename": "__InputValue",
                                        "name": "hasChildren",
                                        "description": None,
                                        "defaultValue": None,
                                    },
                                    {
                                        "__typename": "__InputValue",
                                        "name": "hasFriends",
                                        "description": None,
                                        "defaultValue": None,
                                    },
                                ],
                                "ofType": None,
                            },
                            {
                                "__typename": "__Type",
                                "kind": "OBJECT",
                                "name": "Human",
                                "description": None,
                                "fields": [
                                    {
                                        "__typename": "__Field",
                                        "name": "id",
                                        "description": None,
                                        "args": [],
                                        "type": {
                                            "__typename": "__Type",
                                            "kind": "NON_NULL",
                                            "name": None,
                                            "description": None,
                                        },
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                    {
                                        "__typename": "__Field",
                                        "name": "name",
                                        "description": None,
                                        "args": [],
                                        "type": {
                                            "__typename": "__Type",
                                            "kind": "NON_NULL",
                                            "name": None,
                                            "description": None,
                                        },
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                    {
                                        "__typename": "__Field",
                                        "name": "friends",
                                        "description": None,
                                        "args": [],
                                        "type": {
                                            "__typename": "__Type",
                                            "kind": "LIST",
                                            "name": None,
                                            "description": None,
                                        },
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                ],
                                "interfaces": [
                                    {
                                        "__typename": "__Type",
                                        "kind": "INTERFACE",
                                        "name": "Identifiable",
                                        "description": None,
                                    },
                                    {
                                        "__typename": "__Type",
                                        "kind": "INTERFACE",
                                        "name": "Named",
                                        "description": None,
                                    },
                                ],
                                "possibleTypes": None,
                                "enumValues": None,
                                "inputFields": None,
                                "ofType": None,
                            },
                            {
                                "__typename": "__Type",
                                "kind": "OBJECT",
                                "name": "Cat",
                                "description": None,
                                "fields": [
                                    {
                                        "__typename": "__Field",
                                        "name": "id",
                                        "description": None,
                                        "args": [],
                                        "type": {
                                            "__typename": "__Type",
                                            "kind": "NON_NULL",
                                            "name": None,
                                            "description": None,
                                        },
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                    {
                                        "__typename": "__Field",
                                        "name": "name",
                                        "description": None,
                                        "args": [],
                                        "type": {
                                            "__typename": "__Type",
                                            "kind": "NON_NULL",
                                            "name": None,
                                            "description": None,
                                        },
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                    {
                                        "__typename": "__Field",
                                        "name": "nickname",
                                        "description": None,
                                        "args": [],
                                        "type": {
                                            "__typename": "__Type",
                                            "kind": "SCALAR",
                                            "name": "String",
                                            "description": "The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.",
                                        },
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                    {
                                        "__typename": "__Field",
                                        "name": "owner",
                                        "description": None,
                                        "args": [],
                                        "type": {
                                            "__typename": "__Type",
                                            "kind": "OBJECT",
                                            "name": "Human",
                                            "description": None,
                                        },
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                    {
                                        "__typename": "__Field",
                                        "name": "birthdate",
                                        "description": None,
                                        "args": [],
                                        "type": {
                                            "__typename": "__Type",
                                            "kind": "NON_NULL",
                                            "name": None,
                                            "description": None,
                                        },
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                    {
                                        "__typename": "__Field",
                                        "name": "doesKnowCommand",
                                        "description": None,
                                        "args": [
                                            {
                                                "__typename": "__InputValue",
                                                "name": "command",
                                                "description": None,
                                                "defaultValue": None,
                                            }
                                        ],
                                        "type": {
                                            "__typename": "__Type",
                                            "kind": "NON_NULL",
                                            "name": None,
                                            "description": None,
                                        },
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                    {
                                        "__typename": "__Field",
                                        "name": "meowVolume",
                                        "description": None,
                                        "args": [],
                                        "type": {
                                            "__typename": "__Type",
                                            "kind": "NON_NULL",
                                            "name": None,
                                            "description": None,
                                        },
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                    {
                                        "__typename": "__Field",
                                        "name": "children",
                                        "description": None,
                                        "args": [],
                                        "type": {
                                            "__typename": "__Type",
                                            "kind": "LIST",
                                            "name": None,
                                            "description": None,
                                        },
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                    {
                                        "__typename": "__Field",
                                        "name": "friends",
                                        "description": None,
                                        "args": [],
                                        "type": {
                                            "__typename": "__Type",
                                            "kind": "LIST",
                                            "name": None,
                                            "description": None,
                                        },
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                ],
                                "interfaces": [
                                    {
                                        "__typename": "__Type",
                                        "kind": "INTERFACE",
                                        "name": "Identifiable",
                                        "description": None,
                                    },
                                    {
                                        "__typename": "__Type",
                                        "kind": "INTERFACE",
                                        "name": "Named",
                                        "description": None,
                                    },
                                    {
                                        "__typename": "__Type",
                                        "kind": "INTERFACE",
                                        "name": "Nicknamed",
                                        "description": None,
                                    },
                                    {
                                        "__typename": "__Type",
                                        "kind": "INTERFACE",
                                        "name": "Owned",
                                        "description": None,
                                    },
                                    {
                                        "__typename": "__Type",
                                        "kind": "INTERFACE",
                                        "name": "Birthdated",
                                        "description": "Interface for type with birthdate.",
                                    },
                                ],
                                "possibleTypes": None,
                                "enumValues": None,
                                "inputFields": None,
                                "ofType": None,
                            },
                            {
                                "__typename": "__Type",
                                "kind": "OBJECT",
                                "name": "Dog",
                                "description": None,
                                "fields": [
                                    {
                                        "__typename": "__Field",
                                        "name": "id",
                                        "description": None,
                                        "args": [],
                                        "type": {
                                            "__typename": "__Type",
                                            "kind": "NON_NULL",
                                            "name": None,
                                            "description": None,
                                        },
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                    {
                                        "__typename": "__Field",
                                        "name": "name",
                                        "description": None,
                                        "args": [],
                                        "type": {
                                            "__typename": "__Type",
                                            "kind": "NON_NULL",
                                            "name": None,
                                            "description": None,
                                        },
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                    {
                                        "__typename": "__Field",
                                        "name": "nickname",
                                        "description": None,
                                        "args": [],
                                        "type": {
                                            "__typename": "__Type",
                                            "kind": "SCALAR",
                                            "name": "String",
                                            "description": "The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.",
                                        },
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                    {
                                        "__typename": "__Field",
                                        "name": "owner",
                                        "description": None,
                                        "args": [],
                                        "type": {
                                            "__typename": "__Type",
                                            "kind": "OBJECT",
                                            "name": "Human",
                                            "description": None,
                                        },
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                    {
                                        "__typename": "__Field",
                                        "name": "birthdate",
                                        "description": None,
                                        "args": [],
                                        "type": {
                                            "__typename": "__Type",
                                            "kind": "NON_NULL",
                                            "name": None,
                                            "description": None,
                                        },
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                    {
                                        "__typename": "__Field",
                                        "name": "doesKnowCommand",
                                        "description": None,
                                        "args": [
                                            {
                                                "__typename": "__InputValue",
                                                "name": "command",
                                                "description": None,
                                                "defaultValue": None,
                                            }
                                        ],
                                        "type": {
                                            "__typename": "__Type",
                                            "kind": "NON_NULL",
                                            "name": None,
                                            "description": None,
                                        },
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                    {
                                        "__typename": "__Field",
                                        "name": "barkVolume",
                                        "description": None,
                                        "args": [],
                                        "type": {
                                            "__typename": "__Type",
                                            "kind": "NON_NULL",
                                            "name": None,
                                            "description": None,
                                        },
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                    {
                                        "__typename": "__Field",
                                        "name": "children",
                                        "description": None,
                                        "args": [],
                                        "type": {
                                            "__typename": "__Type",
                                            "kind": "LIST",
                                            "name": None,
                                            "description": None,
                                        },
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                    {
                                        "__typename": "__Field",
                                        "name": "friends",
                                        "description": None,
                                        "args": [],
                                        "type": {
                                            "__typename": "__Type",
                                            "kind": "LIST",
                                            "name": None,
                                            "description": None,
                                        },
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                ],
                                "interfaces": [
                                    {
                                        "__typename": "__Type",
                                        "kind": "INTERFACE",
                                        "name": "Identifiable",
                                        "description": None,
                                    },
                                    {
                                        "__typename": "__Type",
                                        "kind": "INTERFACE",
                                        "name": "Named",
                                        "description": None,
                                    },
                                    {
                                        "__typename": "__Type",
                                        "kind": "INTERFACE",
                                        "name": "Nicknamed",
                                        "description": None,
                                    },
                                    {
                                        "__typename": "__Type",
                                        "kind": "INTERFACE",
                                        "name": "Owned",
                                        "description": None,
                                    },
                                    {
                                        "__typename": "__Type",
                                        "kind": "INTERFACE",
                                        "name": "Birthdated",
                                        "description": "Interface for type with birthdate.",
                                    },
                                ],
                                "possibleTypes": None,
                                "enumValues": None,
                                "inputFields": None,
                                "ofType": None,
                            },
                            {
                                "__typename": "__Type",
                                "kind": "INPUT_OBJECT",
                                "name": "AddHumanInput",
                                "description": None,
                                "fields": None,
                                "interfaces": None,
                                "possibleTypes": None,
                                "enumValues": None,
                                "inputFields": [
                                    {
                                        "__typename": "__InputValue",
                                        "name": "clientMutationId",
                                        "description": None,
                                        "defaultValue": None,
                                    },
                                    {
                                        "__typename": "__InputValue",
                                        "name": "name",
                                        "description": None,
                                        "defaultValue": None,
                                    },
                                ],
                                "ofType": None,
                            },
                            {
                                "__typename": "__Type",
                                "kind": "OBJECT",
                                "name": "AddHumanPayload",
                                "description": None,
                                "fields": [
                                    {
                                        "__typename": "__Field",
                                        "name": "clientMutationId",
                                        "description": None,
                                        "args": [],
                                        "type": {
                                            "__typename": "__Type",
                                            "kind": "SCALAR",
                                            "name": "String",
                                            "description": "The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.",
                                        },
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                    {
                                        "__typename": "__Field",
                                        "name": "human",
                                        "description": None,
                                        "args": [],
                                        "type": {
                                            "__typename": "__Type",
                                            "kind": "NON_NULL",
                                            "name": None,
                                            "description": None,
                                        },
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                ],
                                "interfaces": None,
                                "possibleTypes": None,
                                "enumValues": None,
                                "inputFields": None,
                                "ofType": None,
                            },
                            {
                                "__typename": "__Type",
                                "kind": "INPUT_OBJECT",
                                "name": "AddCatInput",
                                "description": None,
                                "fields": None,
                                "interfaces": None,
                                "possibleTypes": None,
                                "enumValues": None,
                                "inputFields": [
                                    {
                                        "__typename": "__InputValue",
                                        "name": "clientMutationId",
                                        "description": None,
                                        "defaultValue": None,
                                    },
                                    {
                                        "__typename": "__InputValue",
                                        "name": "name",
                                        "description": None,
                                        "defaultValue": None,
                                    },
                                    {
                                        "__typename": "__InputValue",
                                        "name": "nickname",
                                        "description": None,
                                        "defaultValue": None,
                                    },
                                    {
                                        "__typename": "__InputValue",
                                        "name": "ownerId",
                                        "description": None,
                                        "defaultValue": None,
                                    },
                                    {
                                        "__typename": "__InputValue",
                                        "name": "birthdate",
                                        "description": None,
                                        "defaultValue": None,
                                    },
                                    {
                                        "__typename": "__InputValue",
                                        "name": "knownCommands",
                                        "description": None,
                                        "defaultValue": None,
                                    },
                                    {
                                        "__typename": "__InputValue",
                                        "name": "meowVolume",
                                        "description": None,
                                        "defaultValue": None,
                                    },
                                ],
                                "ofType": None,
                            },
                            {
                                "__typename": "__Type",
                                "kind": "OBJECT",
                                "name": "AddCatPayload",
                                "description": None,
                                "fields": [
                                    {
                                        "__typename": "__Field",
                                        "name": "clientMutationId",
                                        "description": None,
                                        "args": [],
                                        "type": {
                                            "__typename": "__Type",
                                            "kind": "SCALAR",
                                            "name": "String",
                                            "description": "The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.",
                                        },
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                    {
                                        "__typename": "__Field",
                                        "name": "cat",
                                        "description": None,
                                        "args": [],
                                        "type": {
                                            "__typename": "__Type",
                                            "kind": "NON_NULL",
                                            "name": None,
                                            "description": None,
                                        },
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                ],
                                "interfaces": None,
                                "possibleTypes": None,
                                "enumValues": None,
                                "inputFields": None,
                                "ofType": None,
                            },
                            {
                                "__typename": "__Type",
                                "kind": "INPUT_OBJECT",
                                "name": "AddDogInput",
                                "description": "Input definition of the add dog mutation.",
                                "fields": None,
                                "interfaces": None,
                                "possibleTypes": None,
                                "enumValues": None,
                                "inputFields": [
                                    {
                                        "__typename": "__InputValue",
                                        "name": "clientMutationId",
                                        "description": "Identifier of the mutation.",
                                        "defaultValue": None,
                                    },
                                    {
                                        "__typename": "__InputValue",
                                        "name": "name",
                                        "description": None,
                                        "defaultValue": None,
                                    },
                                    {
                                        "__typename": "__InputValue",
                                        "name": "nickname",
                                        "description": None,
                                        "defaultValue": None,
                                    },
                                    {
                                        "__typename": "__InputValue",
                                        "name": "ownerId",
                                        "description": None,
                                        "defaultValue": None,
                                    },
                                    {
                                        "__typename": "__InputValue",
                                        "name": "birthdate",
                                        "description": None,
                                        "defaultValue": None,
                                    },
                                    {
                                        "__typename": "__InputValue",
                                        "name": "knownCommands",
                                        "description": None,
                                        "defaultValue": None,
                                    },
                                    {
                                        "__typename": "__InputValue",
                                        "name": "barkVolume",
                                        "description": None,
                                        "defaultValue": None,
                                    },
                                ],
                                "ofType": None,
                            },
                            {
                                "__typename": "__Type",
                                "kind": "OBJECT",
                                "name": "AddDogPayload",
                                "description": "Payload of a add dog mutation.",
                                "fields": [
                                    {
                                        "__typename": "__Field",
                                        "name": "clientMutationId",
                                        "description": None,
                                        "args": [],
                                        "type": {
                                            "__typename": "__Type",
                                            "kind": "SCALAR",
                                            "name": "String",
                                            "description": "The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.",
                                        },
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                    {
                                        "__typename": "__Field",
                                        "name": "dog",
                                        "description": None,
                                        "args": [],
                                        "type": {
                                            "__typename": "__Type",
                                            "kind": "NON_NULL",
                                            "name": None,
                                            "description": None,
                                        },
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                ],
                                "interfaces": None,
                                "possibleTypes": None,
                                "enumValues": None,
                                "inputFields": None,
                                "ofType": None,
                            },
                            {
                                "__typename": "__Type",
                                "kind": "OBJECT",
                                "name": "MyQuery",
                                "description": "Custom Query type.",
                                "fields": [
                                    {
                                        "__typename": "__Field",
                                        "name": "version",
                                        "description": None,
                                        "args": [],
                                        "type": {
                                            "__typename": "__Type",
                                            "kind": "NON_NULL",
                                            "name": None,
                                            "description": None,
                                        },
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                    {
                                        "__typename": "__Field",
                                        "name": "serviceStatus",
                                        "description": "Service status.",
                                        "args": [],
                                        "type": {
                                            "__typename": "__Type",
                                            "kind": "NON_NULL",
                                            "name": None,
                                            "description": None,
                                        },
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                    {
                                        "__typename": "__Field",
                                        "name": "human",
                                        "description": None,
                                        "args": [
                                            {
                                                "__typename": "__InputValue",
                                                "name": "id",
                                                "description": "Human identifier to fetch.",
                                                "defaultValue": None,
                                            }
                                        ],
                                        "type": {
                                            "__typename": "__Type",
                                            "kind": "OBJECT",
                                            "name": "Human",
                                            "description": None,
                                        },
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                    {
                                        "__typename": "__Field",
                                        "name": "humans",
                                        "description": None,
                                        "args": [
                                            {
                                                "__typename": "__InputValue",
                                                "name": "filters",
                                                "description": None,
                                                "defaultValue": None,
                                            },
                                            {
                                                "__typename": "__InputValue",
                                                "name": "order",
                                                "description": None,
                                                "defaultValue": None,
                                            },
                                        ],
                                        "type": {
                                            "__typename": "__Type",
                                            "kind": "LIST",
                                            "name": None,
                                            "description": None,
                                        },
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                    {
                                        "__typename": "__Field",
                                        "name": "pet",
                                        "description": None,
                                        "args": [
                                            {
                                                "__typename": "__InputValue",
                                                "name": "id",
                                                "description": None,
                                                "defaultValue": None,
                                            }
                                        ],
                                        "type": {
                                            "__typename": "__Type",
                                            "kind": "UNION",
                                            "name": "Pet",
                                            "description": None,
                                        },
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                    {
                                        "__typename": "__Field",
                                        "name": "pets",
                                        "description": None,
                                        "args": [
                                            {
                                                "__typename": "__InputValue",
                                                "name": "filters",
                                                "description": None,
                                                "defaultValue": None,
                                            },
                                            {
                                                "__typename": "__InputValue",
                                                "name": "order",
                                                "description": None,
                                                "defaultValue": None,
                                            },
                                        ],
                                        "type": {
                                            "__typename": "__Type",
                                            "kind": "LIST",
                                            "name": None,
                                            "description": None,
                                        },
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                ],
                                "interfaces": None,
                                "possibleTypes": None,
                                "enumValues": None,
                                "inputFields": None,
                                "ofType": None,
                            },
                            {
                                "__typename": "__Type",
                                "kind": "OBJECT",
                                "name": "MyMutation",
                                "description": "Custom Mutation type.",
                                "fields": [
                                    {
                                        "__typename": "__Field",
                                        "name": "addHuman",
                                        "description": None,
                                        "args": [
                                            {
                                                "__typename": "__InputValue",
                                                "name": "input",
                                                "description": None,
                                                "defaultValue": None,
                                            }
                                        ],
                                        "type": {
                                            "__typename": "__Type",
                                            "kind": "NON_NULL",
                                            "name": None,
                                            "description": None,
                                        },
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                    {
                                        "__typename": "__Field",
                                        "name": "addCat",
                                        "description": None,
                                        "args": [
                                            {
                                                "__typename": "__InputValue",
                                                "name": "input",
                                                "description": None,
                                                "defaultValue": None,
                                            }
                                        ],
                                        "type": {
                                            "__typename": "__Type",
                                            "kind": "NON_NULL",
                                            "name": None,
                                            "description": None,
                                        },
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                    {
                                        "__typename": "__Field",
                                        "name": "addDog",
                                        "description": None,
                                        "args": [
                                            {
                                                "__typename": "__InputValue",
                                                "name": "input",
                                                "description": None,
                                                "defaultValue": None,
                                            }
                                        ],
                                        "type": {
                                            "__typename": "__Type",
                                            "kind": "NON_NULL",
                                            "name": None,
                                            "description": None,
                                        },
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                ],
                                "interfaces": None,
                                "possibleTypes": None,
                                "enumValues": None,
                                "inputFields": None,
                                "ofType": None,
                            },
                            {
                                "__typename": "__Type",
                                "kind": "OBJECT",
                                "name": "MySubscription",
                                "description": "Custom Subscription type.",
                                "fields": [
                                    {
                                        "__typename": "__Field",
                                        "name": "humanAdded",
                                        "description": None,
                                        "args": [],
                                        "type": {
                                            "__typename": "__Type",
                                            "kind": "NON_NULL",
                                            "name": None,
                                            "description": None,
                                        },
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                    {
                                        "__typename": "__Field",
                                        "name": "petAdded",
                                        "description": None,
                                        "args": [
                                            {
                                                "__typename": "__InputValue",
                                                "name": "kind",
                                                "description": None,
                                                "defaultValue": None,
                                            }
                                        ],
                                        "type": {
                                            "__typename": "__Type",
                                            "kind": "NON_NULL",
                                            "name": None,
                                            "description": None,
                                        },
                                        "isDeprecated": False,
                                        "deprecationReason": None,
                                    },
                                ],
                                "interfaces": None,
                                "possibleTypes": None,
                                "enumValues": None,
                                "inputFields": None,
                                "ofType": None,
                            },
                            {
                                "__typename": "__Type",
                                "kind": "SCALAR",
                                "name": "Boolean",
                                "description": "The `Boolean` scalar type represents `true` or `false`.",
                                "fields": None,
                                "interfaces": None,
                                "possibleTypes": None,
                                "enumValues": None,
                                "inputFields": None,
                                "ofType": None,
                            },
                            {
                                "__typename": "__Type",
                                "kind": "SCALAR",
                                "name": "Date",
                                "description": "The `Date` scalar type represents a date object",
                                "fields": None,
                                "interfaces": None,
                                "possibleTypes": None,
                                "enumValues": None,
                                "inputFields": None,
                                "ofType": None,
                            },
                            {
                                "__typename": "__Type",
                                "kind": "SCALAR",
                                "name": "DateTime",
                                "description": "The `DateTime` scalar type represents a date time object",
                                "fields": None,
                                "interfaces": None,
                                "possibleTypes": None,
                                "enumValues": None,
                                "inputFields": None,
                                "ofType": None,
                            },
                            {
                                "__typename": "__Type",
                                "kind": "SCALAR",
                                "name": "Float",
                                "description": "The `Float` scalar type represents signed double-precision fractional values as specified by [IEEE 754](https://en.wikipedia.org/wiki/IEEE_floating_point).",
                                "fields": None,
                                "interfaces": None,
                                "possibleTypes": None,
                                "enumValues": None,
                                "inputFields": None,
                                "ofType": None,
                            },
                            {
                                "__typename": "__Type",
                                "kind": "SCALAR",
                                "name": "ID",
                                "description": 'The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID.',
                                "fields": None,
                                "interfaces": None,
                                "possibleTypes": None,
                                "enumValues": None,
                                "inputFields": None,
                                "ofType": None,
                            },
                            {
                                "__typename": "__Type",
                                "kind": "SCALAR",
                                "name": "Int",
                                "description": "The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1.",
                                "fields": None,
                                "interfaces": None,
                                "possibleTypes": None,
                                "enumValues": None,
                                "inputFields": None,
                                "ofType": None,
                            },
                            {
                                "__typename": "__Type",
                                "kind": "SCALAR",
                                "name": "String",
                                "description": "The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.",
                                "fields": None,
                                "interfaces": None,
                                "possibleTypes": None,
                                "enumValues": None,
                                "inputFields": None,
                                "ofType": None,
                            },
                            {
                                "__typename": "__Type",
                                "kind": "SCALAR",
                                "name": "Time",
                                "description": "The `Time` scalar type represents a time object",
                                "fields": None,
                                "interfaces": None,
                                "possibleTypes": None,
                                "enumValues": None,
                                "inputFields": None,
                                "ofType": None,
                            },
                        ],
                    },
                }
            },
        ),
    ],
)
async def test_introspection_full(engine, query, expected):
    assert await engine.execute(query) == expected
