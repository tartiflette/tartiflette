import pytest

from tartiflette.sdl.builder import build_graphql_schema_from_sdl
from tartiflette.schema.bakery import SchemaBakery
from tartiflette.types.exceptions.tartiflette import (
    GraphQLSchemaError,
    UnknownSchemaFieldResolver,
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
    generated_schema = SchemaBakery._preheat("A")

    with pytest.raises(ValueError):
        generated_schema.get_field_by_name("Invalid.Field.name")
    with pytest.raises(ValueError):
        generated_schema.get_field_by_name("")
    with pytest.raises(ValueError):
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
    generated_schema = SchemaBakery._preheat("A")

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
    generated_schema = SchemaBakery._preheat("A")

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
    generated_schema = SchemaBakery._preheat("a")

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
    generated_schema = SchemaBakery._preheat("a")

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
    generated_schema = SchemaBakery._preheat("a")

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
