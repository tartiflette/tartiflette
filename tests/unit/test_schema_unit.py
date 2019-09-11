import pytest

from tartiflette import Directive, Resolver, Scalar
from tartiflette.engine import _import_builtins
from tartiflette.schema.bakery import SchemaBakery
from tartiflette.schema.registry import SchemaRegistry
from tartiflette.types.exceptions.tartiflette import (
    GraphQLSchemaError,
    ImproperlyConfigured,
    UnknownSchemaFieldResolver,
)


@pytest.mark.asyncio
async def test_schema_object_get_field_name(clean_registry):
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

    _, schema_sdl = await _import_builtins([], schema_sdl, "default")
    clean_registry.register_sdl("A", schema_sdl)
    generated_schema = SchemaBakery._preheat("A")

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
@pytest.mark.asyncio
async def test_schema_validate_named_types(
    full_sdl, expected_error, expected_value, clean_registry
):

    _, full_sdl = await _import_builtins([], full_sdl, "A")
    clean_registry.register_sdl("A", full_sdl)
    generated_schema = SchemaBakery._preheat("A")

    if expected_error:
        with pytest.raises(GraphQLSchemaError):
            generated_schema._validate()
    else:
        assert generated_schema._validate() == expected_value


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
    ids=["1", "2", "3", "4", "5", "6", "7"],
)
@pytest.mark.asyncio
async def test_schema_validate_object_follow_interfaces(
    full_sdl, expected_error, expected_value, clean_registry
):
    _, full_sdl = await _import_builtins([], full_sdl, "A")
    clean_registry.register_sdl("A", full_sdl)
    generated_schema = SchemaBakery._preheat("A")

    try:
        generated_schema.find_type("Brand").coerce_output = lambda x: x
        generated_schema.find_type("Brand").coerce_input = lambda x: x
        generated_schema.find_type("Brand").parse_literal = lambda x: x
    except KeyError:
        pass

    try:
        generated_schema.find_type("Part").coerce_output = lambda x: x
        generated_schema.find_type("Part").coerce_input = lambda x: x
        generated_schema.find_type("Part").parse_literal = lambda x: x
    except KeyError:
        pass

    if expected_error:
        with pytest.raises(GraphQLSchemaError):
            generated_schema._validate()
    else:
        assert generated_schema._validate() == expected_value


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
@pytest.mark.asyncio
async def test_schema_validate_root_types_exist(
    full_sdl, expected_error, expected_value, clean_registry
):
    _, full_sdl = await _import_builtins([], full_sdl, "a")
    clean_registry.register_sdl("a", full_sdl)
    generated_schema = SchemaBakery._preheat("a")

    if expected_error:
        with pytest.raises(GraphQLSchemaError):
            generated_schema._validate()
    else:
        assert generated_schema._validate() == expected_value


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
@pytest.mark.asyncio
async def test_schema_validate_non_empty_object(
    full_sdl, expected_error, expected_value, clean_registry
):
    _, full_sdl = await _import_builtins([], full_sdl, "a")
    clean_registry.register_sdl("a", full_sdl)
    generated_schema = SchemaBakery._preheat("a")

    if expected_error:
        with pytest.raises(GraphQLSchemaError):
            generated_schema._validate()
    else:
        assert generated_schema._validate() == expected_value


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
@pytest.mark.asyncio
async def test_schema_validate_union_is_acceptable(
    full_sdl, expected_error, expected_value, clean_registry
):
    _, full_sdl = await _import_builtins([], full_sdl, "a")
    clean_registry.register_sdl("a", full_sdl)
    generated_schema = SchemaBakery._preheat("a")

    if expected_error:
        with pytest.raises(GraphQLSchemaError):
            generated_schema._validate()
    else:
        assert generated_schema._validate() == expected_value


@pytest.mark.asyncio
async def test_schema_bake_schema(clean_registry):
    _, full_sdl = await _import_builtins(
        [],
        """
        type Query {
            lol: Int
        }""",
        "a",
    )
    clean_registry.register_sdl("a", full_sdl)
    assert await SchemaBakery.bake("a") is not None


@pytest.mark.parametrize(
    "type_name,expected", [("Unknown", False), ("User", True)]
)
@pytest.mark.asyncio
async def test_schema_has_type(clean_registry, type_name, expected):
    _, full_sdl = await _import_builtins(
        [],
        """
        type User {
            name: String
        }

        type Query {
            viewer: User
        }
        """,
        "a",
    )
    clean_registry.register_sdl("a", full_sdl)
    schema = await SchemaBakery.bake("a")
    assert schema.has_type(type_name) is expected


@pytest.mark.parametrize(
    "schema_name,where,obj",
    [
        (
            "directives_schema",
            "directives",
            Directive("my_directive", "directives_schema"),
        ),
        ("scalars_schema", "scalars", Scalar("my_scalar", "scalars_schema")),
        (
            "resolvers_schema",
            "resolvers",
            Resolver("my_resolver", "resolvers_schema"),
        ),
    ],
)
def test_schema_registry_register(clean_registry, schema_name, where, obj):
    SchemaRegistry._register(schema_name, where, obj)

    with pytest.raises(ImproperlyConfigured) as excinfo:
        SchemaRegistry._register(schema_name, where, obj)

    assert str(excinfo.value) == (
        "Can't register < %s > to < %s > %s because it's already registered"
        % (obj.name, schema_name, where)
    )
