import pytest

from tartiflette import Directive, Resolver, Scalar
from tartiflette.scalar.builtins.string import ScalarString


def bakery(schema_name):
    Scalar("Baz", schema_name=schema_name)(ScalarString)

    @Directive("dirA", schema_name=schema_name)
    @Directive("dirB", schema_name=schema_name)
    @Directive("dirC", schema_name=schema_name)
    class GenericDirective:
        pass

    @Resolver("Query.foo", schema_name=schema_name)
    async def resolver_query_foo(parent, args, ctx, info):
        return {"id": "1", "name": "Foo"}


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl="""
    extend scalar Baz @dirB

    extend scalar Baz @dirC

    scalar Baz @dirA

    directive @dirA on | OBJECT | INPUT_OBJECT | ENUM | INTERFACE | SCALAR | UNION
    directive @dirB on | OBJECT | INPUT_OBJECT | ENUM | INTERFACE | SCALAR | UNION
    directive @dirC on | OBJECT | INPUT_OBJECT | ENUM | INTERFACE | SCALAR | UNION

    extend interface Identifiable @dirB

    extend interface Identifiable @dirC {
      id: ID!
    }

    interface Identifiable @dirA

    interface Named {
      name: String!
    }

    extend type Foo implements Identifiable @dirB {
      id: ID!
    }

    extend type Foo implements Named @dirC {
      name: String!
    }

    type Foo @dirA

    extend input Bar @dirB {
      id: ID!
    }

    extend input Bar @dirC {
      name: String!
    }

    input Bar @dirA

    extend enum Foobar @dirB {
      ID
    }

    extend enum Foobar @dirC {
      NAME
    }

    enum Foobar @dirA

    type Foobaz {
      noop: String!
    }

    extend union Qux @dirB = Foo

    extend union Qux @dirC = Foobaz

    union Qux @dirA

    type Query {
      foo: Foo
    }
    """,
    bakery=bakery,
)
async def test_extend_definition(schema_stack):
    assert await schema_stack.execute("{ foo {id, name } }") == {
        "data": {"foo": {"id": "1", "name": "Foo"}}
    }
    scalar_baz = schema_stack.schema.find_type("Baz")
    interface_identifiable = schema_stack.schema.find_type("Identifiable")
    type_foo = schema_stack.schema.find_type("Foo")
    input_bar = schema_stack.schema.find_type("Bar")
    enum_foobar = schema_stack.schema.find_type("Foobar")
    union_qux = schema_stack.schema.find_type("Qux")

    for graphql_type in [
        scalar_baz,
        interface_identifiable,
        type_foo,
        input_bar,
        enum_foobar,
        union_qux,
    ]:
        assert [
            directive.name.value
            for directive in graphql_type.definition.directives
        ] == ["dirA", "dirB", "dirC"]

    assert [
        (field.name.value, str(field.type))
        for field in interface_identifiable.definition.fields
    ] == [("id", "ID!")]

    assert [
        (field.name.value, str(field.type))
        for field in type_foo.definition.fields
    ] == [("id", "ID!"), ("name", "String!")]

    assert [
        (field.name.value, str(field.type))
        for field in input_bar.definition.fields
    ] == [("id", "ID!"), ("name", "String!")]

    assert [value.name.value for value in enum_foobar.definition.values] == [
        "ID",
        "NAME",
    ]

    assert [
        union_type.name.value for union_type in union_qux.definition.types
    ] == ["Foo", "Foobaz"]
