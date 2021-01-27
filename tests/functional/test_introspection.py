import pytest

from tartiflette import create_engine


@pytest.mark.asyncio
async def test_tartiflette_execute_basic_type_introspection_output():
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

    ttftt = await create_engine(
        schema_sdl,
        schema_name="test_tartiflette_execute_basic_type_introspection_output",
    )

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
    """,
        operation_name="Test",
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
                ],
            }
        }
    } == result


@pytest.mark.asyncio
async def test_tartiflette_execute_schema_introspection_output():
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

    ttftt = await create_engine(
        schema_sdl,
        schema_name="test_tartiflette_execute_schema_introspection_output",
    )

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
    """,
        operation_name="Test",
    )

    assert {
        "data": {
            "__schema": {
                "queryType": {"name": "CustomRootQuery"},
                "mutationType": {"name": "CustomRootMutation"},
                "subscriptionType": {"name": "CustomRootSubscription"},
                "types": [
                    {"kind": "OBJECT", "name": "CustomRootQuery"},
                    {"kind": "OBJECT", "name": "CustomRootMutation"},
                    {"kind": "OBJECT", "name": "CustomRootSubscription"},
                    {"kind": "SCALAR", "name": "Boolean"},
                    {"kind": "SCALAR", "name": "Date"},
                    {"kind": "SCALAR", "name": "DateTime"},
                    {"kind": "SCALAR", "name": "Float"},
                    {"kind": "SCALAR", "name": "ID"},
                    {"kind": "SCALAR", "name": "Int"},
                    {"kind": "SCALAR", "name": "String"},
                    {"kind": "SCALAR", "name": "Time"},
                ],
                "directives": [
                    {
                        "name": "deprecated",
                        "description": "Marks an element of a GraphQL schema as no longer supported.",
                        "locations": ["FIELD_DEFINITION", "ENUM_VALUE"],
                        "args": [
                            {
                                "name": "reason",
                                "description": "Explains why this element was deprecated, usually also including a suggestion for how to access supported similar data. Formatted using the Markdown syntax (as specified by [CommonMark](https://commonmark.org/).",
                                "type": {"kind": "SCALAR", "name": "String"},
                                "defaultValue": '"No longer supported"',
                            }
                        ],
                    },
                    {
                        "name": "nonIntrospectable",
                        "description": "Directs the executor to hide the element on introspection queries.",
                        "locations": ["FIELD_DEFINITION", "SCHEMA"],
                        "args": [],
                    },
                    {
                        "name": "skip",
                        "description": "Directs the executor to skip this field or fragment when the `if` argument is true.",
                        "locations": [
                            "FIELD",
                            "FRAGMENT_SPREAD",
                            "INLINE_FRAGMENT",
                        ],
                        "args": [
                            {
                                "name": "if",
                                "description": "Skipped when true.",
                                "type": {"kind": "NON_NULL", "name": None},
                                "defaultValue": None,
                            }
                        ],
                    },
                    {
                        "name": "include",
                        "description": "Directs the executor to include this field or fragment only when the `if` argument is true.",
                        "locations": [
                            "FIELD",
                            "FRAGMENT_SPREAD",
                            "INLINE_FRAGMENT",
                        ],
                        "args": [
                            {
                                "name": "if",
                                "description": "Included when true.",
                                "type": {"kind": "NON_NULL", "name": None},
                                "defaultValue": None,
                            }
                        ],
                    },
                ],
            }
        }
    } == result


@pytest.mark.asyncio
async def test_tartiflette_execute_schema_introspection_output_introspecting_args():
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

    ttftt = await create_engine(
        schema_sdl,
        schema_name="test_tartiflette_execute_schema_introspection_output_introspecting_args",
    )
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
    """,
        operation_name="IntrospectionQuery",
    )

    assert {
        "data": {
            "__schema": {
                "queryType": {"name": "Query"},
                "mutationType": None,
                "subscriptionType": None,
                "types": [
                    {
                        "kind": "OBJECT",
                        "name": "lol",
                        "fields": [
                            {
                                "name": "GGG",
                                "args": [],
                                "type": {
                                    "kind": "SCALAR",
                                    "name": "String",
                                    "ofType": None,
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "GG",
                                "args": [
                                    {
                                        "name": "a",
                                        "type": {
                                            "kind": "NON_NULL",
                                            "name": None,
                                            "ofType": {
                                                "kind": "SCALAR",
                                                "name": "String",
                                                "ofType": None,
                                            },
                                        },
                                        "defaultValue": None,
                                    }
                                ],
                                "type": {
                                    "kind": "SCALAR",
                                    "name": "String",
                                    "ofType": None,
                                },
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                            {
                                "name": "G",
                                "args": [
                                    {
                                        "name": "a",
                                        "type": {
                                            "kind": "NON_NULL",
                                            "name": None,
                                            "ofType": {
                                                "kind": "LIST",
                                                "name": None,
                                                "ofType": {
                                                    "kind": "NON_NULL",
                                                    "name": None,
                                                    "ofType": {
                                                        "kind": "SCALAR",
                                                        "name": "String",
                                                        "ofType": None,
                                                    },
                                                },
                                            },
                                        },
                                        "defaultValue": None,
                                    }
                                ],
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
                                "name": "a",
                                "args": [],
                                "type": {
                                    "kind": "OBJECT",
                                    "name": "lol",
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
    } == result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "include_deprecated,expected",
    [
        (
            "true",
            {
                "data": {
                    "__type": {
                        "name": "MyEnum",
                        "kind": "ENUM",
                        "description": "An amazing enum",
                        "enumValues": [
                            {
                                "name": "ENUM_v1",
                                "description": "MyEnum.ENUM_v1",
                                "isDeprecated": True,
                                "deprecationReason": "Why not?",
                            },
                            {
                                "name": "ENUM_v2",
                                "description": "MyEnum.ENUM_v2",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                        ],
                    }
                }
            },
        ),
        (
            "null",
            {
                "data": {
                    "__type": {
                        "name": "MyEnum",
                        "kind": "ENUM",
                        "description": "An amazing enum",
                        "enumValues": [
                            {
                                "name": "ENUM_v1",
                                "description": "MyEnum.ENUM_v1",
                                "isDeprecated": True,
                                "deprecationReason": "Why not?",
                            },
                            {
                                "name": "ENUM_v2",
                                "description": "MyEnum.ENUM_v2",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                        ],
                    }
                }
            },
        ),
        (
            "false",
            {
                "data": {
                    "__type": {
                        "name": "MyEnum",
                        "kind": "ENUM",
                        "description": "An amazing enum",
                        "enumValues": [
                            {
                                "name": "ENUM_v2",
                                "description": "MyEnum.ENUM_v2",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            }
                        ],
                    }
                }
            },
        ),
    ],
)
async def test_introspection_type_enum_values_include_deprecated(
    include_deprecated, expected, random_schema_name
):
    sdl = '''
    """An amazing enum"""
    enum MyEnum {
      """MyEnum.ENUM_v1"""
      ENUM_v1 @deprecated(reason: "Why not?")

      """MyEnum.ENUM_v2"""
      ENUM_v2
    }

    type Query {
      uselessField: [MyEnum]
    }
    '''

    engine = await create_engine(sdl, schema_name=random_schema_name)

    result = await engine.execute(
        """
        {{
          __type(name: "MyEnum") {{
            name
            kind
            description
            enumValues(includeDeprecated: {}) {{
              name
              description
              isDeprecated
              deprecationReason
            }}
          }}
        }}
        """.format(
            include_deprecated
        )
    )

    assert result == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "type_name,include_deprecated,expected",
    [
        # MyInterface
        (
            "MyInterface",
            "true",
            {
                "data": {
                    "__type": {
                        "name": "MyInterface",
                        "kind": "INTERFACE",
                        "description": "An amazing interface",
                        "fields": [
                            {
                                "name": "firstField",
                                "description": "MyInterface.firstField",
                                "isDeprecated": True,
                                "deprecationReason": "Why not?",
                            },
                            {
                                "name": "secondField",
                                "description": "MyInterface.secondField",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                        ],
                    }
                }
            },
        ),
        (
            "MyInterface",
            "null",
            {
                "data": {
                    "__type": {
                        "name": "MyInterface",
                        "kind": "INTERFACE",
                        "description": "An amazing interface",
                        "fields": [
                            {
                                "name": "firstField",
                                "description": "MyInterface.firstField",
                                "isDeprecated": True,
                                "deprecationReason": "Why not?",
                            },
                            {
                                "name": "secondField",
                                "description": "MyInterface.secondField",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                        ],
                    }
                }
            },
        ),
        (
            "MyInterface",
            "false",
            {
                "data": {
                    "__type": {
                        "name": "MyInterface",
                        "kind": "INTERFACE",
                        "description": "An amazing interface",
                        "fields": [
                            {
                                "name": "secondField",
                                "description": "MyInterface.secondField",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            }
                        ],
                    }
                }
            },
        ),
        # MyType
        (
            "MyType",
            "true",
            {
                "data": {
                    "__type": {
                        "name": "MyType",
                        "kind": "OBJECT",
                        "description": "An amazing object",
                        "fields": [
                            {
                                "name": "firstField",
                                "description": "MyType.firstField",
                                "isDeprecated": True,
                                "deprecationReason": "Why not?",
                            },
                            {
                                "name": "secondField",
                                "description": "MyType.secondField",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                        ],
                    }
                }
            },
        ),
        (
            "MyType",
            "null",
            {
                "data": {
                    "__type": {
                        "name": "MyType",
                        "kind": "OBJECT",
                        "description": "An amazing object",
                        "fields": [
                            {
                                "name": "firstField",
                                "description": "MyType.firstField",
                                "isDeprecated": True,
                                "deprecationReason": "Why not?",
                            },
                            {
                                "name": "secondField",
                                "description": "MyType.secondField",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            },
                        ],
                    }
                }
            },
        ),
        (
            "MyType",
            "false",
            {
                "data": {
                    "__type": {
                        "name": "MyType",
                        "kind": "OBJECT",
                        "description": "An amazing object",
                        "fields": [
                            {
                                "name": "secondField",
                                "description": "MyType.secondField",
                                "isDeprecated": False,
                                "deprecationReason": None,
                            }
                        ],
                    }
                }
            },
        ),
    ],
)
async def test_introspection_type_fields_include_deprecated(
    type_name, include_deprecated, expected, random_schema_name
):
    sdl = '''
    """An amazing enum"""
    enum MyEnum {
      """MyEnum.ENUM_v1"""
      ENUM_v1 @deprecated(reason: "Why not?")

      """MyEnum.ENUM_v2"""
      ENUM_v2
    }

    """An amazing interface"""
    interface MyInterface {
      """MyInterface.firstField"""
      firstField: String @deprecated(reason: "Why not?")

      """MyInterface.secondField"""
      secondField: String
    }

    """An amazing object"""
    type MyType {
      """MyType.firstField"""
      firstField: String @deprecated(reason: "Why not?")

      """MyType.secondField"""
      secondField: String
    }

    type Query {
      uselessField: [MyEnum]
      aField: MyType
    }
    '''

    engine = await create_engine(sdl, schema_name=random_schema_name)

    result = await engine.execute(
        """
        {{
          __type(name: "{}") {{
            name
            kind
            description
            fields(includeDeprecated: {}) {{
              name
              description
              isDeprecated
              deprecationReason
            }}
          }}
        }}
        """.format(
            type_name, include_deprecated
        )
    )

    assert result == expected


@pytest.mark.asyncio
async def test_tartiflette_execute_schema_introspection_non_introspectable_output():
    schema_sdl = """
    schema @nonIntrospectable {
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

    ttftt = await create_engine(
        schema_sdl,
        schema_name="test_tartiflette_execute_schema_introspection_non_introspectable_output",
    )

    result = await ttftt.execute(
        """
    query Test {
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
        __typename
        __type(name: "CustomRootMutation") {
            __typename
            kind
            name
        }
    }
    """,
        operation_name="Test",
    )

    assert {
        "data": None,
        "errors": [
            {
                "message": "Introspection is disabled for this type",
                "path": ["__type"],
                "locations": [{"line": 27, "column": 9}],
            },
            {
                "message": "Introspection is disabled for this schema",
                "path": ["__schema"],
                "locations": [{"line": 3, "column": 9}],
            },
        ],
    } == result
