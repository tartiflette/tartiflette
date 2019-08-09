from unittest.mock import Mock

import pytest

from tartiflette import Resolver
from tartiflette.schema.bakery import SchemaBakery
from tartiflette.types.exceptions.tartiflette import NonAwaitableResolver


@pytest.mark.asyncio
async def test_resolver_decorator(clean_registry):
    from tartiflette.engine import _import_builtins

    schema_sdl = """
    schema {
        query: RootQuery
        mutation: Mutation
        subscription: Subscription
    }

    type Foo {
        a: String
    }

    type Bar {
        b: String
    }

    type Baz {
        c: String
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
        field(input: UserInfo): String!
        anotherField: [Int]
        fieldWithDefaultValueArg(test: String = "default"): ID
        simpleField: Date
    }
    """

    _, schema_sdl = await _import_builtins([], schema_sdl, "default")

    clean_registry.register_sdl("default", schema_sdl)

    mock_one = Mock()
    mock_two = Mock()

    @Resolver("Test.field")
    async def func_field_resolver(*args, **kwargs):
        mock_one()
        return

    @Resolver("RootQuery.defaultField")
    async def func_default_resolver(*args, **kwargs):
        mock_two()
        return

    with pytest.raises(NonAwaitableResolver):

        @Resolver("Test.simpleField")
        def func_default_resolver(*args, **kwargs):
            pass

    generated_schema = await SchemaBakery.bake("default")

    assert (
        generated_schema.get_field_by_name("Test.field").resolver is not None
    )
    assert callable(generated_schema.get_field_by_name("Test.field").resolver)
    assert mock_one.called is False
    assert (
        generated_schema.get_field_by_name("RootQuery.defaultField").resolver
        is not None
    )
    assert callable(
        generated_schema.get_field_by_name("RootQuery.defaultField").resolver
    )
    assert mock_two.called is False
