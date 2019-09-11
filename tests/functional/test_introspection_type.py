import pytest

_TYPE_INTROSPECTION_QUERY = """
{{
  __typename
  __type(name: "{}") {{
    __typename
    kind
    name
    description
    fields {{
      __typename
      name
      description
      args {{
        __typename
        name
        description
        type {{
          __typename
          kind
          name
          description
          ofType {{
            __typename
            kind
            name
            description
            ofType {{
              __typename
              kind
              name
              description
              ofType {{
                __typename
                kind
                name
                description
              }}
            }}
          }}
        }}
        defaultValue
      }}
      type {{
        __typename
        kind
        name
        description
        ofType {{
          __typename
          kind
          name
          description
          ofType {{
            __typename
            kind
            name
            description
            ofType {{
              __typename
              kind
              name
              description
            }}
          }}
        }}
      }}
      isDeprecated
      deprecationReason
    }}
    interfaces {{
      __typename
      kind
      name
      description
      ofType {{
        __typename
        kind
        name
        description
        ofType {{
          __typename
          kind
          name
          description
          ofType {{
            __typename
            kind
            name
            description
            ofType {{
              __typename
              kind
              name
              description
            }}
          }}
        }}
      }}
    }}
    possibleTypes {{
      __typename
      kind
      name
      description
      ofType {{
        __typename
        kind
        name
        description
        ofType {{
          __typename
          kind
          name
          description
          ofType {{
            __typename
            kind
            name
            description
            ofType {{
              __typename
              kind
              name
              description
            }}
          }}
        }}
      }}
    }}
    enumValues {{
      __typename
      name
      description
      isDeprecated
      deprecationReason
    }}
    inputFields {{
      __typename
      name
      description
      type {{
        __typename
        kind
        name
        description
        ofType {{
          __typename
          kind
          name
          description
          ofType {{
            __typename
            kind
            name
            description
            ofType {{
              __typename
              kind
              name
              description
            }}
          }}
        }}
      }}
      defaultValue
    }}
    ofType {{
      __typename
      kind
      name
      description
      ofType {{
        __typename
        kind
        name
        description
        ofType {{
          __typename
          kind
          name
          description
          ofType {{
            __typename
            kind
            name
            description
          }}
        }}
      }}
    }}
  }}
}}
"""


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(name="pets")
@pytest.mark.parametrize(
    "type_name,expected",
    [
        ("UNKNOWN_TYPE", {"data": {"__typename": "MyQuery", "__type": None}}),
        (
            "Int",
            {
                "data": {
                    "__typename": "MyQuery",
                    "__type": {
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
                }
            },
        ),
        (
            "Human",
            {
                "data": {
                    "__typename": "MyQuery",
                    "__type": {
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
                                    "ofType": {
                                        "__typename": "__Type",
                                        "kind": "SCALAR",
                                        "name": "Int",
                                        "description": "The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1.",
                                        "ofType": None,
                                    },
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
                                    "ofType": {
                                        "__typename": "__Type",
                                        "kind": "SCALAR",
                                        "name": "String",
                                        "description": "The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.",
                                        "ofType": None,
                                    },
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
                                    "ofType": {
                                        "__typename": "__Type",
                                        "kind": "NON_NULL",
                                        "name": None,
                                        "description": None,
                                        "ofType": {
                                            "__typename": "__Type",
                                            "kind": "UNION",
                                            "name": "PetOrHuman",
                                            "description": None,
                                            "ofType": None,
                                        },
                                    },
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
                                "ofType": None,
                            },
                            {
                                "__typename": "__Type",
                                "kind": "INTERFACE",
                                "name": "Named",
                                "description": None,
                                "ofType": None,
                            },
                        ],
                        "possibleTypes": None,
                        "enumValues": None,
                        "inputFields": None,
                        "ofType": None,
                    },
                }
            },
        ),
        (
            "Owned",
            {
                "data": {
                    "__typename": "MyQuery",
                    "__type": {
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
                                    "ofType": None,
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
                                "ofType": None,
                            },
                            {
                                "__typename": "__Type",
                                "kind": "OBJECT",
                                "name": "Dog",
                                "description": None,
                                "ofType": None,
                            },
                        ],
                        "enumValues": None,
                        "inputFields": None,
                        "ofType": None,
                    },
                }
            },
        ),
        (
            "PetOrHuman",
            {
                "data": {
                    "__typename": "MyQuery",
                    "__type": {
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
                                "ofType": None,
                            },
                            {
                                "__typename": "__Type",
                                "kind": "OBJECT",
                                "name": "Dog",
                                "description": None,
                                "ofType": None,
                            },
                            {
                                "__typename": "__Type",
                                "kind": "OBJECT",
                                "name": "Human",
                                "description": None,
                                "ofType": None,
                            },
                        ],
                        "enumValues": None,
                        "inputFields": None,
                        "ofType": None,
                    },
                }
            },
        ),
        (
            "ServiceStatus",
            {
                "data": {
                    "__typename": "MyQuery",
                    "__type": {
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
                }
            },
        ),
        (
            "HumanFilters",
            {
                "data": {
                    "__typename": "MyQuery",
                    "__type": {
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
                                "type": {
                                    "__typename": "__Type",
                                    "kind": "LIST",
                                    "name": None,
                                    "description": None,
                                    "ofType": {
                                        "__typename": "__Type",
                                        "kind": "NON_NULL",
                                        "name": None,
                                        "description": None,
                                        "ofType": {
                                            "__typename": "__Type",
                                            "kind": "SCALAR",
                                            "name": "Int",
                                            "description": "The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1.",
                                            "ofType": None,
                                        },
                                    },
                                },
                                "defaultValue": None,
                            },
                            {
                                "__typename": "__InputValue",
                                "name": "name",
                                "description": None,
                                "type": {
                                    "__typename": "__Type",
                                    "kind": "SCALAR",
                                    "name": "String",
                                    "description": None,
                                    "ofType": None,
                                },
                                "defaultValue": None,
                            },
                            {
                                "__typename": "__InputValue",
                                "name": "hasFriends",
                                "description": None,
                                "type": {
                                    "__typename": "__Type",
                                    "kind": "SCALAR",
                                    "name": "Boolean",
                                    "description": None,
                                    "ofType": None,
                                },
                                "defaultValue": None,
                            },
                        ],
                        "ofType": None,
                    },
                }
            },
        ),
        (
            "__Schema",
            {
                "data": {
                    "__typename": "MyQuery",
                    "__type": {
                        "__typename": "__Type",
                        "kind": "OBJECT",
                        "name": "__Schema",
                        "description": "A GraphQL Schema defines the capabilities of a GraphQL server. It exposes all available types and directives on the server, as well as the entry points for query, mutation, and subscription operations.",
                        "fields": [
                            {
                                "__typename": "__Field",
                                "name": "types",
                                "description": "A list of all types supported by this server.",
                                "args": [],
                                "type": {
                                    "__typename": "__Type",
                                    "kind": "NON_NULL",
                                    "name": None,
                                    "description": None,
                                    "ofType": {
                                        "__typename": "__Type",
                                        "kind": "LIST",
                                        "name": None,
                                        "description": None,
                                        "ofType": {
                                            "__typename": "__Type",
                                            "kind": "NON_NULL",
                                            "name": None,
                                            "description": None,
                                            "ofType": {
                                                "__typename": "__Type",
                                                "kind": "OBJECT",
                                                "name": "__Type",
                                                "description": "The fundamental unit of any GraphQL Schema is the type. There are many kinds of types in GraphQL as represented by the `__TypeKind` enum.\n\nDepending on the kind of a type, certain fields describe information about that type. Scalar types provide no information beyond a name and description, while Enum types provide their values. Object and Interface types provide the fields they describe. Abstract types, Union and Interface, provide the Object types possible at runtime. List and NonNull types compose other types.",
                                            },
                                        },
                                    },
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "__typename": "__Field",
                                "name": "queryType",
                                "description": "The type that query operations will be rooted at.",
                                "args": [],
                                "type": {
                                    "__typename": "__Type",
                                    "kind": "NON_NULL",
                                    "name": None,
                                    "description": None,
                                    "ofType": {
                                        "__typename": "__Type",
                                        "kind": "OBJECT",
                                        "name": "__Type",
                                        "description": "The fundamental unit of any GraphQL Schema is the type. There are many kinds of types in GraphQL as represented by the `__TypeKind` enum.\n\nDepending on the kind of a type, certain fields describe information about that type. Scalar types provide no information beyond a name and description, while Enum types provide their values. Object and Interface types provide the fields they describe. Abstract types, Union and Interface, provide the Object types possible at runtime. List and NonNull types compose other types.",
                                        "ofType": None,
                                    },
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "__typename": "__Field",
                                "name": "mutationType",
                                "description": "If this server supports mutation, the type that mutation operations will be rooted at.",
                                "args": [],
                                "type": {
                                    "__typename": "__Type",
                                    "kind": "OBJECT",
                                    "name": "__Type",
                                    "description": "The fundamental unit of any GraphQL Schema is the type. There are many kinds of types in GraphQL as represented by the `__TypeKind` enum.\n\nDepending on the kind of a type, certain fields describe information about that type. Scalar types provide no information beyond a name and description, while Enum types provide their values. Object and Interface types provide the fields they describe. Abstract types, Union and Interface, provide the Object types possible at runtime. List and NonNull types compose other types.",
                                    "ofType": None,
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "__typename": "__Field",
                                "name": "subscriptionType",
                                "description": "If this server support subscription, the type that subscription operations will be rooted at.",
                                "args": [],
                                "type": {
                                    "__typename": "__Type",
                                    "kind": "OBJECT",
                                    "name": "__Type",
                                    "description": "The fundamental unit of any GraphQL Schema is the type. There are many kinds of types in GraphQL as represented by the `__TypeKind` enum.\n\nDepending on the kind of a type, certain fields describe information about that type. Scalar types provide no information beyond a name and description, while Enum types provide their values. Object and Interface types provide the fields they describe. Abstract types, Union and Interface, provide the Object types possible at runtime. List and NonNull types compose other types.",
                                    "ofType": None,
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "__typename": "__Field",
                                "name": "directives",
                                "description": "A list of all directives supported by this server.",
                                "args": [],
                                "type": {
                                    "__typename": "__Type",
                                    "kind": "NON_NULL",
                                    "name": None,
                                    "description": None,
                                    "ofType": {
                                        "__typename": "__Type",
                                        "kind": "LIST",
                                        "name": None,
                                        "description": None,
                                        "ofType": {
                                            "__typename": "__Type",
                                            "kind": "NON_NULL",
                                            "name": None,
                                            "description": None,
                                            "ofType": {
                                                "__typename": "__Type",
                                                "kind": "OBJECT",
                                                "name": "__Directive",
                                                "description": "A Directive provides a way to describe alternate runtime execution and type validation behavior in a GraphQL document.\n\nIn some cases, you need to provide options to alter GraphQL's execution behavior in ways field arguments will not suffice, such as conditionally including or skipping a field. Directives provide this by describing additional information to the executor.",
                                            },
                                        },
                                    },
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                        ],
                        "interfaces": [],
                        "possibleTypes": None,
                        "enumValues": None,
                        "inputFields": None,
                        "ofType": None,
                    },
                }
            },
        ),
        (
            "__Type",
            {
                "data": {
                    "__typename": "MyQuery",
                    "__type": {
                        "__typename": "__Type",
                        "kind": "OBJECT",
                        "name": "__Type",
                        "description": "The fundamental unit of any GraphQL Schema is the type. There are many kinds of types in GraphQL as represented by the `__TypeKind` enum.\n\nDepending on the kind of a type, certain fields describe information about that type. Scalar types provide no information beyond a name and description, while Enum types provide their values. Object and Interface types provide the fields they describe. Abstract types, Union and Interface, provide the Object types possible at runtime. List and NonNull types compose other types.",
                        "fields": [
                            {
                                "__typename": "__Field",
                                "name": "kind",
                                "description": None,
                                "args": [],
                                "type": {
                                    "__typename": "__Type",
                                    "kind": "NON_NULL",
                                    "name": None,
                                    "description": None,
                                    "ofType": {
                                        "__typename": "__Type",
                                        "kind": "ENUM",
                                        "name": "__TypeKind",
                                        "description": "An enum describing what kind of type a given `__Type` is.",
                                        "ofType": None,
                                    },
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
                                    "kind": "SCALAR",
                                    "name": "String",
                                    "description": "The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.",
                                    "ofType": None,
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "__typename": "__Field",
                                "name": "description",
                                "description": None,
                                "args": [],
                                "type": {
                                    "__typename": "__Type",
                                    "kind": "SCALAR",
                                    "name": "String",
                                    "description": "The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.",
                                    "ofType": None,
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "__typename": "__Field",
                                "name": "fields",
                                "description": None,
                                "args": [
                                    {
                                        "__typename": "__InputValue",
                                        "name": "includeDeprecated",
                                        "description": None,
                                        "type": {
                                            "__typename": "__Type",
                                            "kind": "SCALAR",
                                            "name": "Boolean",
                                            "description": None,
                                            "ofType": None,
                                        },
                                        "defaultValue": "false",
                                    }
                                ],
                                "type": {
                                    "__typename": "__Type",
                                    "kind": "LIST",
                                    "name": None,
                                    "description": None,
                                    "ofType": {
                                        "__typename": "__Type",
                                        "kind": "NON_NULL",
                                        "name": None,
                                        "description": None,
                                        "ofType": {
                                            "__typename": "__Type",
                                            "kind": "OBJECT",
                                            "name": "__Field",
                                            "description": "Object and Interface types are described by a list of Fields, each of which has a name, potentially a list of arguments, and a return type.",
                                            "ofType": None,
                                        },
                                    },
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "__typename": "__Field",
                                "name": "interfaces",
                                "description": None,
                                "args": [],
                                "type": {
                                    "__typename": "__Type",
                                    "kind": "LIST",
                                    "name": None,
                                    "description": None,
                                    "ofType": {
                                        "__typename": "__Type",
                                        "kind": "NON_NULL",
                                        "name": None,
                                        "description": None,
                                        "ofType": {
                                            "__typename": "__Type",
                                            "kind": "OBJECT",
                                            "name": "__Type",
                                            "description": "The fundamental unit of any GraphQL Schema is the type. There are many kinds of types in GraphQL as represented by the `__TypeKind` enum.\n\nDepending on the kind of a type, certain fields describe information about that type. Scalar types provide no information beyond a name and description, while Enum types provide their values. Object and Interface types provide the fields they describe. Abstract types, Union and Interface, provide the Object types possible at runtime. List and NonNull types compose other types.",
                                            "ofType": None,
                                        },
                                    },
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "__typename": "__Field",
                                "name": "possibleTypes",
                                "description": None,
                                "args": [],
                                "type": {
                                    "__typename": "__Type",
                                    "kind": "LIST",
                                    "name": None,
                                    "description": None,
                                    "ofType": {
                                        "__typename": "__Type",
                                        "kind": "NON_NULL",
                                        "name": None,
                                        "description": None,
                                        "ofType": {
                                            "__typename": "__Type",
                                            "kind": "OBJECT",
                                            "name": "__Type",
                                            "description": "The fundamental unit of any GraphQL Schema is the type. There are many kinds of types in GraphQL as represented by the `__TypeKind` enum.\n\nDepending on the kind of a type, certain fields describe information about that type. Scalar types provide no information beyond a name and description, while Enum types provide their values. Object and Interface types provide the fields they describe. Abstract types, Union and Interface, provide the Object types possible at runtime. List and NonNull types compose other types.",
                                            "ofType": None,
                                        },
                                    },
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "__typename": "__Field",
                                "name": "enumValues",
                                "description": None,
                                "args": [
                                    {
                                        "__typename": "__InputValue",
                                        "name": "includeDeprecated",
                                        "description": None,
                                        "type": {
                                            "__typename": "__Type",
                                            "kind": "SCALAR",
                                            "name": "Boolean",
                                            "description": None,
                                            "ofType": None,
                                        },
                                        "defaultValue": "false",
                                    }
                                ],
                                "type": {
                                    "__typename": "__Type",
                                    "kind": "LIST",
                                    "name": None,
                                    "description": None,
                                    "ofType": {
                                        "__typename": "__Type",
                                        "kind": "NON_NULL",
                                        "name": None,
                                        "description": None,
                                        "ofType": {
                                            "__typename": "__Type",
                                            "kind": "OBJECT",
                                            "name": "__EnumValue",
                                            "description": "One possible value for a given Enum. Enum values are unique values, not a placeholder for a string or numeric value. However an Enum value is returned in a JSON response as a string.",
                                            "ofType": None,
                                        },
                                    },
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "__typename": "__Field",
                                "name": "inputFields",
                                "description": None,
                                "args": [],
                                "type": {
                                    "__typename": "__Type",
                                    "kind": "LIST",
                                    "name": None,
                                    "description": None,
                                    "ofType": {
                                        "__typename": "__Type",
                                        "kind": "NON_NULL",
                                        "name": None,
                                        "description": None,
                                        "ofType": {
                                            "__typename": "__Type",
                                            "kind": "OBJECT",
                                            "name": "__InputValue",
                                            "description": "Arguments provided to Fields or Directives and the input fields of an InputObject are represented as Input Values which describe their type and optionally a default value.",
                                            "ofType": None,
                                        },
                                    },
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "__typename": "__Field",
                                "name": "ofType",
                                "description": None,
                                "args": [],
                                "type": {
                                    "__typename": "__Type",
                                    "kind": "OBJECT",
                                    "name": "__Type",
                                    "description": "The fundamental unit of any GraphQL Schema is the type. There are many kinds of types in GraphQL as represented by the `__TypeKind` enum.\n\nDepending on the kind of a type, certain fields describe information about that type. Scalar types provide no information beyond a name and description, while Enum types provide their values. Object and Interface types provide the fields they describe. Abstract types, Union and Interface, provide the Object types possible at runtime. List and NonNull types compose other types.",
                                    "ofType": None,
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                        ],
                        "interfaces": [],
                        "possibleTypes": None,
                        "enumValues": None,
                        "inputFields": None,
                        "ofType": None,
                    },
                }
            },
        ),
        (
            "__Field",
            {
                "data": {
                    "__typename": "MyQuery",
                    "__type": {
                        "__typename": "__Type",
                        "kind": "OBJECT",
                        "name": "__Field",
                        "description": "Object and Interface types are described by a list of Fields, each of which has a name, potentially a list of arguments, and a return type.",
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
                                    "ofType": {
                                        "__typename": "__Type",
                                        "kind": "SCALAR",
                                        "name": "String",
                                        "description": "The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.",
                                        "ofType": None,
                                    },
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "__typename": "__Field",
                                "name": "description",
                                "description": None,
                                "args": [],
                                "type": {
                                    "__typename": "__Type",
                                    "kind": "SCALAR",
                                    "name": "String",
                                    "description": "The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.",
                                    "ofType": None,
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "__typename": "__Field",
                                "name": "args",
                                "description": None,
                                "args": [],
                                "type": {
                                    "__typename": "__Type",
                                    "kind": "NON_NULL",
                                    "name": None,
                                    "description": None,
                                    "ofType": {
                                        "__typename": "__Type",
                                        "kind": "LIST",
                                        "name": None,
                                        "description": None,
                                        "ofType": {
                                            "__typename": "__Type",
                                            "kind": "NON_NULL",
                                            "name": None,
                                            "description": None,
                                            "ofType": {
                                                "__typename": "__Type",
                                                "kind": "OBJECT",
                                                "name": "__InputValue",
                                                "description": "Arguments provided to Fields or Directives and the input fields of an InputObject are represented as Input Values which describe their type and optionally a default value.",
                                            },
                                        },
                                    },
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "__typename": "__Field",
                                "name": "type",
                                "description": None,
                                "args": [],
                                "type": {
                                    "__typename": "__Type",
                                    "kind": "NON_NULL",
                                    "name": None,
                                    "description": None,
                                    "ofType": {
                                        "__typename": "__Type",
                                        "kind": "OBJECT",
                                        "name": "__Type",
                                        "description": "The fundamental unit of any GraphQL Schema is the type. There are many kinds of types in GraphQL as represented by the `__TypeKind` enum.\n\nDepending on the kind of a type, certain fields describe information about that type. Scalar types provide no information beyond a name and description, while Enum types provide their values. Object and Interface types provide the fields they describe. Abstract types, Union and Interface, provide the Object types possible at runtime. List and NonNull types compose other types.",
                                        "ofType": None,
                                    },
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "__typename": "__Field",
                                "name": "isDeprecated",
                                "description": None,
                                "args": [],
                                "type": {
                                    "__typename": "__Type",
                                    "kind": "NON_NULL",
                                    "name": None,
                                    "description": None,
                                    "ofType": {
                                        "__typename": "__Type",
                                        "kind": "SCALAR",
                                        "name": "Boolean",
                                        "description": "The `Boolean` scalar type represents `true` or `false`.",
                                        "ofType": None,
                                    },
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "__typename": "__Field",
                                "name": "deprecationReason",
                                "description": None,
                                "args": [],
                                "type": {
                                    "__typename": "__Type",
                                    "kind": "SCALAR",
                                    "name": "String",
                                    "description": "The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.",
                                    "ofType": None,
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                        ],
                        "interfaces": [],
                        "possibleTypes": None,
                        "enumValues": None,
                        "inputFields": None,
                        "ofType": None,
                    },
                }
            },
        ),
        (
            "__InputValue",
            {
                "data": {
                    "__typename": "MyQuery",
                    "__type": {
                        "__typename": "__Type",
                        "kind": "OBJECT",
                        "name": "__InputValue",
                        "description": "Arguments provided to Fields or Directives and the input fields of an InputObject are represented as Input Values which describe their type and optionally a default value.",
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
                                    "ofType": {
                                        "__typename": "__Type",
                                        "kind": "SCALAR",
                                        "name": "String",
                                        "description": "The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.",
                                        "ofType": None,
                                    },
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "__typename": "__Field",
                                "name": "description",
                                "description": None,
                                "args": [],
                                "type": {
                                    "__typename": "__Type",
                                    "kind": "SCALAR",
                                    "name": "String",
                                    "description": "The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.",
                                    "ofType": None,
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "__typename": "__Field",
                                "name": "type",
                                "description": None,
                                "args": [],
                                "type": {
                                    "__typename": "__Type",
                                    "kind": "NON_NULL",
                                    "name": None,
                                    "description": None,
                                    "ofType": {
                                        "__typename": "__Type",
                                        "kind": "OBJECT",
                                        "name": "__Type",
                                        "description": "The fundamental unit of any GraphQL Schema is the type. There are many kinds of types in GraphQL as represented by the `__TypeKind` enum.\n\nDepending on the kind of a type, certain fields describe information about that type. Scalar types provide no information beyond a name and description, while Enum types provide their values. Object and Interface types provide the fields they describe. Abstract types, Union and Interface, provide the Object types possible at runtime. List and NonNull types compose other types.",
                                        "ofType": None,
                                    },
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "__typename": "__Field",
                                "name": "defaultValue",
                                "description": "A GraphQL-formatted string representing the default value for this input value.",
                                "args": [],
                                "type": {
                                    "__typename": "__Type",
                                    "kind": "SCALAR",
                                    "name": "String",
                                    "description": "The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.",
                                    "ofType": None,
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                        ],
                        "interfaces": [],
                        "possibleTypes": None,
                        "enumValues": None,
                        "inputFields": None,
                        "ofType": None,
                    },
                }
            },
        ),
        (
            "__EnumValue",
            {
                "data": {
                    "__typename": "MyQuery",
                    "__type": {
                        "__typename": "__Type",
                        "kind": "OBJECT",
                        "name": "__EnumValue",
                        "description": "One possible value for a given Enum. Enum values are unique values, not a placeholder for a string or numeric value. However an Enum value is returned in a JSON response as a string.",
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
                                    "ofType": {
                                        "__typename": "__Type",
                                        "kind": "SCALAR",
                                        "name": "String",
                                        "description": "The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.",
                                        "ofType": None,
                                    },
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "__typename": "__Field",
                                "name": "description",
                                "description": None,
                                "args": [],
                                "type": {
                                    "__typename": "__Type",
                                    "kind": "SCALAR",
                                    "name": "String",
                                    "description": "The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.",
                                    "ofType": None,
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "__typename": "__Field",
                                "name": "isDeprecated",
                                "description": None,
                                "args": [],
                                "type": {
                                    "__typename": "__Type",
                                    "kind": "NON_NULL",
                                    "name": None,
                                    "description": None,
                                    "ofType": {
                                        "__typename": "__Type",
                                        "kind": "SCALAR",
                                        "name": "Boolean",
                                        "description": "The `Boolean` scalar type represents `true` or `false`.",
                                        "ofType": None,
                                    },
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "__typename": "__Field",
                                "name": "deprecationReason",
                                "description": None,
                                "args": [],
                                "type": {
                                    "__typename": "__Type",
                                    "kind": "SCALAR",
                                    "name": "String",
                                    "description": "The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.",
                                    "ofType": None,
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                        ],
                        "interfaces": [],
                        "possibleTypes": None,
                        "enumValues": None,
                        "inputFields": None,
                        "ofType": None,
                    },
                }
            },
        ),
        (
            "__TypeKind",
            {
                "data": {
                    "__typename": "MyQuery",
                    "__type": {
                        "__typename": "__Type",
                        "kind": "ENUM",
                        "name": "__TypeKind",
                        "description": "An enum describing what kind of type a given `__Type` is.",
                        "fields": None,
                        "interfaces": None,
                        "possibleTypes": None,
                        "enumValues": [
                            {
                                "__typename": "__EnumValue",
                                "name": "SCALAR",
                                "description": "Indicates this type is a scalar.",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "__typename": "__EnumValue",
                                "name": "OBJECT",
                                "description": "Indicates this type is an object. `fields` and `interfaces` are valid fields.",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "__typename": "__EnumValue",
                                "name": "INTERFACE",
                                "description": "Indicates this type is an interface. `fields` and `possibleTypes` are valid fields.",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "__typename": "__EnumValue",
                                "name": "UNION",
                                "description": "Indicates this type is a union. `possibleTypes` is a valid field.",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "__typename": "__EnumValue",
                                "name": "ENUM",
                                "description": "Indicates this type is an enum. `enumValues` is a valid field.",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "__typename": "__EnumValue",
                                "name": "INPUT_OBJECT",
                                "description": "Indicates this type is an input object. `inputFields` is a valid field.",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "__typename": "__EnumValue",
                                "name": "LIST",
                                "description": "Indicates this type is a list. `ofType` is a valid field.",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "__typename": "__EnumValue",
                                "name": "NON_NULL",
                                "description": "Indicates this type is a non-null. `ofType` is a valid field.",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                        ],
                        "inputFields": None,
                        "ofType": None,
                    },
                }
            },
        ),
        (
            "__Directive",
            {
                "data": {
                    "__typename": "MyQuery",
                    "__type": {
                        "__typename": "__Type",
                        "kind": "OBJECT",
                        "name": "__Directive",
                        "description": "A Directive provides a way to describe alternate runtime execution and type validation behavior in a GraphQL document.\n\nIn some cases, you need to provide options to alter GraphQL's execution behavior in ways field arguments will not suffice, such as conditionally including or skipping a field. Directives provide this by describing additional information to the executor.",
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
                                    "ofType": {
                                        "__typename": "__Type",
                                        "kind": "SCALAR",
                                        "name": "String",
                                        "description": "The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.",
                                        "ofType": None,
                                    },
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "__typename": "__Field",
                                "name": "description",
                                "description": None,
                                "args": [],
                                "type": {
                                    "__typename": "__Type",
                                    "kind": "SCALAR",
                                    "name": "String",
                                    "description": "The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.",
                                    "ofType": None,
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "__typename": "__Field",
                                "name": "locations",
                                "description": None,
                                "args": [],
                                "type": {
                                    "__typename": "__Type",
                                    "kind": "NON_NULL",
                                    "name": None,
                                    "description": None,
                                    "ofType": {
                                        "__typename": "__Type",
                                        "kind": "LIST",
                                        "name": None,
                                        "description": None,
                                        "ofType": {
                                            "__typename": "__Type",
                                            "kind": "NON_NULL",
                                            "name": None,
                                            "description": None,
                                            "ofType": {
                                                "__typename": "__Type",
                                                "kind": "ENUM",
                                                "name": "__DirectiveLocation",
                                                "description": "A Directive can be adjacent to many parts of the GraphQL language, a __DirectiveLocation describes one such possible adjacencies.",
                                            },
                                        },
                                    },
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "__typename": "__Field",
                                "name": "args",
                                "description": None,
                                "args": [],
                                "type": {
                                    "__typename": "__Type",
                                    "kind": "NON_NULL",
                                    "name": None,
                                    "description": None,
                                    "ofType": {
                                        "__typename": "__Type",
                                        "kind": "LIST",
                                        "name": None,
                                        "description": None,
                                        "ofType": {
                                            "__typename": "__Type",
                                            "kind": "NON_NULL",
                                            "name": None,
                                            "description": None,
                                            "ofType": {
                                                "__typename": "__Type",
                                                "kind": "OBJECT",
                                                "name": "__InputValue",
                                                "description": "Arguments provided to Fields or Directives and the input fields of an InputObject are represented as Input Values which describe their type and optionally a default value.",
                                            },
                                        },
                                    },
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                        ],
                        "interfaces": [],
                        "possibleTypes": None,
                        "enumValues": None,
                        "inputFields": None,
                        "ofType": None,
                    },
                }
            },
        ),
        (
            "__DirectiveLocation",
            {
                "data": {
                    "__typename": "MyQuery",
                    "__type": {
                        "__typename": "__Type",
                        "kind": "ENUM",
                        "name": "__DirectiveLocation",
                        "description": "A Directive can be adjacent to many parts of the GraphQL language, a __DirectiveLocation describes one such possible adjacencies.",
                        "fields": None,
                        "interfaces": None,
                        "possibleTypes": None,
                        "enumValues": [
                            {
                                "__typename": "__EnumValue",
                                "name": "QUERY",
                                "description": "Location adjacent to a query operation.",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "__typename": "__EnumValue",
                                "name": "MUTATION",
                                "description": "Location adjacent to a mutation operation.",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "__typename": "__EnumValue",
                                "name": "SUBSCRIPTION",
                                "description": "Location adjacent to a subscription operation.",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "__typename": "__EnumValue",
                                "name": "FIELD",
                                "description": "Location adjacent to a field.",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "__typename": "__EnumValue",
                                "name": "FRAGMENT_DEFINITION",
                                "description": "Location adjacent to a fragment definition.",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "__typename": "__EnumValue",
                                "name": "FRAGMENT_SPREAD",
                                "description": "Location adjacent to a fragment spread.",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "__typename": "__EnumValue",
                                "name": "INLINE_FRAGMENT",
                                "description": "Location adjacent to an inline fragment.",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "__typename": "__EnumValue",
                                "name": "SCHEMA",
                                "description": "Location adjacent to a schema definition.",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "__typename": "__EnumValue",
                                "name": "SCALAR",
                                "description": "Location adjacent to a scalar definition.",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "__typename": "__EnumValue",
                                "name": "OBJECT",
                                "description": "Location adjacent to an object type definition.",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "__typename": "__EnumValue",
                                "name": "FIELD_DEFINITION",
                                "description": "Location adjacent to a field definition.",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "__typename": "__EnumValue",
                                "name": "ARGUMENT_DEFINITION",
                                "description": "Location adjacent to an argument definition.",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "__typename": "__EnumValue",
                                "name": "INTERFACE",
                                "description": "Location adjacent to an interface definition.",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "__typename": "__EnumValue",
                                "name": "UNION",
                                "description": "Location adjacent to a union definition.",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "__typename": "__EnumValue",
                                "name": "ENUM",
                                "description": "Location adjacent to an enum definition.",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "__typename": "__EnumValue",
                                "name": "ENUM_VALUE",
                                "description": "Location adjacent to an enum value definition.",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "__typename": "__EnumValue",
                                "name": "INPUT_OBJECT",
                                "description": "Location adjacent to an input object type definition.",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "__typename": "__EnumValue",
                                "name": "INPUT_FIELD_DEFINITION",
                                "description": "Location adjacent to an input object field definition.",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                        ],
                        "inputFields": None,
                        "ofType": None,
                    },
                }
            },
        ),
    ],
)
async def test_introspection_type(engine, type_name, expected):
    assert (
        await engine.execute(_TYPE_INTROSPECTION_QUERY.format(type_name))
        == expected
    )
