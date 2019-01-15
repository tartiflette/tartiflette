import pytest
from unittest import mock
from unittest.mock import patch

from tartiflette.schema.registry import SchemaRegistry, _get_builtins_sdl_files
from tartiflette.sdl.builder import build_graphql_schema_from_sdl
from tartiflette.schema.bakery import SchemaBakery
from tartiflette.types.exceptions.tartiflette import (
    GraphQLSchemaError,
    UnknownSchemaFieldResolver,
    ImproperlyConfigured
)


def test_schema_object_get_field_name(clean_registry):
    schema_sdl = """
    schema {
        query: RootQuery
        mutation: Mutation
        subscription: Subscription
    }

    union Group = Foo | Bar | Baz

    interface Something {
        oneField: [Int]
        anotherField: [String]
        aLastOne: [[Date!]]!
    }

    input UserInfo {
        name: String
        dateOfBirth: [Date]
        graphQLFan: Boolean!
    }

    type RootQuery {
        defaultField: Int
    }

    # Query has been replaced by RootQuery as entrypoint
    type Query {
        nonDefaultField: String
    }

    \"\"\"
    This is a docstring for the Test Object Type.
    \"\"\"
    type Test {
        \"\"\"
        This is a field description :D
        \"\"\"
        field(input: InputObject): String!
        anotherField: [Int]
        fieldWithDefaultValueArg(test: String = "default"): ID
        simpleField: Date
    }
    """

    clean_registry.register_sdl("A", schema_sdl)
    generated_schema = SchemaBakery._preheat("A", None)

    with pytest.raises(ImproperlyConfigured):
        generated_schema.get_field_by_name("Invalid.Field.name")
    with pytest.raises(ImproperlyConfigured):
        generated_schema.get_field_by_name("")
    with pytest.raises(ImproperlyConfigured):
        generated_schema.get_field_by_name("unknownField")

    # Happy path
    assert (
        generated_schema.get_field_by_name("Query.nonDefaultField") is not None
    )
    assert (
        generated_schema.get_field_by_name("RootQuery.defaultField")
        is not None
    )
    assert generated_schema.get_field_by_name("Test.field") is not None
    assert generated_schema.get_field_by_name("Test.simpleField") is not None

    # Sad path
    with pytest.raises(UnknownSchemaFieldResolver):
        assert generated_schema.get_field_by_name("Something.unknownField")


@pytest.mark.parametrize(
    "full_sdl,expected_error,expected_value",
    [
        # Happy path
        (
            """
        type SimpleObject {
            firstField: Int
            secondField: String
            thirdField: ID!
            fourthField: [Float]
            fifthField: [Boolean!]
            sixthField: [[String]!]!
        }

        type Query {
            placeholder: String
        }
        """,
            False,
            True,
        ),
        (
            """

        type Query {
            placeholder: Date
        }
        """,
            False,
            True,
        ),
        (
            """
        type Query {
            firstField: Date
        }
        """,
            False,
            True,
        ),
        (
            """
        type DateTime2 {
            date: Date
            time: Time
        }

        type Date2 {
            day: Int
            month: Int
            year: Int
        }

        type Query {
            placeholder: String
        }
        """,
            False,
            True,
        ),
        # Sad path
        (
            """
        type SimpleObject {
            firstField: CustomType
        }

        type Query {
            placeholder: String
        }
        """,
            True,
            False,
        ),
    ],
)
def test_schema_validate_named_types(
    full_sdl, expected_error, expected_value, clean_registry
):

    clean_registry.register_sdl("A", full_sdl)
    generated_schema = SchemaBakery._preheat("A", None)

    if expected_error:
        with pytest.raises(GraphQLSchemaError):
            generated_schema.validate()
    else:
        assert generated_schema.validate() == expected_value


@pytest.mark.parametrize(
    "full_sdl,expected_error,expected_value",
    [
        # Happy path
        (
            """
        interface Vehicle {
            speedInKmh: Float
        }

        scalar Brand

        type Car implements Vehicle {
            name: String!
            brand: Brand
            speedInKmh: Float
        }

        type Query {
            placeholder: String
        }
        """,
            False,
            True,
        ),
        (
            """
        interface Vehicle {
            speedInKmh: Float
            parts: [String!]!
        }

        scalar Brand

        type Car implements Vehicle {
            name: String!
            brand: Brand
            speedInKmh: Float
            parts: [String!]!
        }

        type Query {
            placeholder: String
        }
        """,
            False,
            True,
        ),
        (
            """
        interface Vehicle {
            speedInKmh: Float
        }

        scalar Part

        interface MechanicalStuff {
            parts: [Part!]!
        }

        type Car implements Vehicle & MechanicalStuff {
            name: String!
            model: String
            speedInKmh: Float
            parts: [Part!]!
        }

        type Query {
            placeholder: String
        }
        """,
            False,
            True,
        ),
        # Sad path
        (
            """
        interface Vehicle {
            speedInKmh: Float
            parts: [String!]!
        }

        scalar Brand

        type Car implements Vehicle {
            name: String!
            brand: Brand
            speedInKmh: Float
            parts: [Int!]!
        }

        type Query {
            placeholder: String
        }
        """,
            True,
            False,
        ),
        (
            """
        scalar Brand

        type Car implements Unknown {
            name: String!
        }

        type Query {
            placeholder: String
        }
        """,
            True,
            False,
        ),
        (
            """
        scalar Brand

        type Car implements Brand {
            name: String!
        }

        type Query {
            placeholder: String
        }
        """,
            True,
            False,
        ),
        (
            """
        interface Vehicle {
            speedInKmh: Float
        }

        interface MechanicalStuff {
            parts: [String!]!
        }

        type Car implements Vehicle & MechanicalStuff {
            name: String!
            model: String
            speedInKmh: Float
        }

        type Query {
            placeholder: String
        }
        """,
            True,
            False,
        ),
    ],
)
def test_schema_validate_object_follow_interfaces(
    full_sdl, expected_error, expected_value, clean_registry
):
    clean_registry.register_sdl("A", full_sdl)
    generated_schema = SchemaBakery._preheat("A", None)

    try:
        generated_schema.find_type("Brand").coerce_output = lambda x: x
        generated_schema.find_type("Brand").coerce_input = lambda x: x
    except KeyError:
        pass

    try:
        generated_schema.find_type("Part").coerce_output = lambda x: x
        generated_schema.find_type("Part").coerce_input = lambda x: x
    except KeyError:
        pass

    if expected_error:
        with pytest.raises(GraphQLSchemaError):
            generated_schema.validate()
    else:
        assert generated_schema.validate() == expected_value


@pytest.mark.parametrize(
    "full_sdl,expected_error,expected_value",
    [
        # Happy path
        (
            """
        type Query {
            placeholder: String
        }
        """,
            False,
            True,
        ),
        (
            """
        schema {
            query: RootQuery
            mutation: RootMutation
            subscription: RootSubscription
        }

        type RootQuery {
            placeholder: String
        }
        type RootMutation {
            placeholder: String
        }
        type RootSubscription {
            placeholder: String
        }
        """,
            False,
            True,
        ),
        # Sad path
        (
            """
        type SomethingNotRootQuery {
            placeholder: String
        }
        """,
            True,
            False,
        ),
        (
            """
        schema {
            query: RootQuery
            mutation: RootMutation
            subscription: RootSubscription
        }

        type RootMutation {
            placeholder: String
        }
        type RootSubscription {
            placeholder: String
        }
        """,
            True,
            False,
        ),
        (
            """
        schema {
            query: RootQuery
            mutation: RootMutation
            subscription: RootSubscription
        }

        type RootQuery {
            placeholder: String
        }
        type RootSubscription {
            placeholder: String
        }
        """,
            True,
            False,
        ),
        (
            """
        schema {
            query: RootQuery
            mutation: RootMutation
            subscription: RootSubscription
        }

        type RootQuery {
            placeholder: String
        }
        type RootMutation {
            placeholder: String
        }
        """,
            True,
            False,
        ),
    ],
)
def test_schema_validate_root_types_exist(
    full_sdl, expected_error, expected_value, clean_registry
):
    clean_registry.register_sdl("a", full_sdl)
    generated_schema = SchemaBakery._preheat("a", None)

    if expected_error:
        with pytest.raises(GraphQLSchemaError):
            generated_schema.validate()
    else:
        assert generated_schema.validate() == expected_value


@pytest.mark.parametrize(
    "full_sdl,expected_error,expected_value",
    [
        # Happy path
        (
            """
        type Query {
            hasAField: Boolean
        }
        """,
            False,
            True,
        ),
        # Sad path
        (
            """
        type Query
        """,
            True,
            False,
        ),
    ],
)
def test_schema_validate_non_empty_object(
    full_sdl, expected_error, expected_value, clean_registry
):
    clean_registry.register_sdl("a", full_sdl)
    generated_schema = SchemaBakery._preheat("a", None)

    if expected_error:
        with pytest.raises(GraphQLSchemaError):
            generated_schema.validate()
    else:
        assert generated_schema.validate() == expected_value


@pytest.mark.parametrize(
    "full_sdl,expected_error,expected_value",
    [
        # Happy path
        (
            """
        type Query {
            something: Something
        }

        type Something {
            field: String
        }

        type Else {
            anotherField: Int
        }

        union Test = Something | Else
        """,
            False,
            True,
        ),
        # Sad path
        (
            """
        type Query {
            something: Test
        }

        union Test = Test | Test
        """,
            True,
            False,
        ),
    ],
)
def test_schema_validate_union_is_acceptable(
    full_sdl, expected_error, expected_value, clean_registry
):
    clean_registry.register_sdl("a", full_sdl)
    generated_schema = SchemaBakery._preheat("a", None)

    if expected_error:
        with pytest.raises(GraphQLSchemaError):
            generated_schema.validate()
    else:
        assert generated_schema.validate() == expected_value


def test_schema_bake_schema(clean_registry):
    clean_registry.register_sdl(
        "a",
        """
        type Query {
            lol: Int
        }
    """,
    )
    assert SchemaBakery.bake("a") is not None


@pytest.mark.parametrize("exclude_date_scalar", [True, False])
def test_schema_bake_schema_exclude_builtins_scalars(
        clean_registry, exclude_date_scalar
):
    exclude_builtins_scalars = ["Date"] if exclude_date_scalar else None

    clean_registry.register_sdl(
        "exclude",
        """
        type Query {
            lol: Int
        }
    """,
        exclude_builtins_scalars=exclude_builtins_scalars,
    )

    schema = SchemaBakery.bake(
        "exclude",
        exclude_builtins_scalars=exclude_builtins_scalars,
    )

    assert schema is not None
    assert len([
        scalar
        for scalar in SchemaRegistry._schemas["exclude"]["scalars"]
        if scalar._name == "Date"
    ]) == 0 if exclude_date_scalar else 1


@patch("tartiflette.schema.registry._DIR_PATH", "/dir")
@pytest.mark.parametrize("exclude_builtins_scalars,expected", [
    (
        None,
        [
            "/dir/builtins/scalars/boolean.sdl",
            "/dir/builtins/scalars/date.sdl",
            "/dir/builtins/scalars/datetime.sdl",
            "/dir/builtins/scalars/float.sdl",
            "/dir/builtins/scalars/id.sdl",
            "/dir/builtins/scalars/int.sdl",
            "/dir/builtins/scalars/string.sdl",
            "/dir/builtins/scalars/time.sdl",
            "/dir/builtins/directives.sdl",
            "/dir/builtins/introspection.sdl",
        ],
    ),
    (
        ["Date", "Time"],
        [
            "/dir/builtins/scalars/boolean.sdl",
            "/dir/builtins/scalars/datetime.sdl",
            "/dir/builtins/scalars/float.sdl",
            "/dir/builtins/scalars/id.sdl",
            "/dir/builtins/scalars/int.sdl",
            "/dir/builtins/scalars/string.sdl",
            "/dir/builtins/directives.sdl",
            "/dir/builtins/introspection.sdl",
        ],
    ),
    (
        ["date", "Time"],
        [
            "/dir/builtins/scalars/boolean.sdl",
            "/dir/builtins/scalars/date.sdl",
            "/dir/builtins/scalars/datetime.sdl",
            "/dir/builtins/scalars/float.sdl",
            "/dir/builtins/scalars/id.sdl",
            "/dir/builtins/scalars/int.sdl",
            "/dir/builtins/scalars/string.sdl",
            "/dir/builtins/directives.sdl",
            "/dir/builtins/introspection.sdl",
        ],
    ),
])
def test_schema_registry_get_builtins_sdl_files(
    exclude_builtins_scalars, expected
):
    assert _get_builtins_sdl_files(exclude_builtins_scalars) == expected


@pytest.mark.parametrize("type_name,expected", [
    (
        "Unknown",
        False,
    ),
    (
        "User",
        True,
    ),
])
def test_schema_has_type(clean_registry, type_name, expected):
    clean_registry.register_sdl(
        "a",
        """
        type User {
            name: String
        }

        type Query {
            viewer: User
        }
        """
    )
    schema = SchemaBakery.bake("a")
    assert schema.has_type(type_name) is expected
