import pytest

from tartiflette import Resolver, TypeResolver, create_engine
from tartiflette.types.exceptions.tartiflette import (
    InvalidType,
    UnknownTypeDefinition,
)

_SDL = """
interface Named {
  name: String!
}

type Human implements Named {
  id: Int!
  name: String!
}

type Alien implements Named {
  id: Int!
  name: String!
}

type Pet {
  id: Int!
  name: String!
}

type First {
  firstFieldA: String
  firstFieldB: Int
}

type Second {
  secondFieldA: String
  secondFieldB: Int
}

type Third {
  thirdFieldA: String
  thirdFieldB: Float
}

type Fourth {
  fourthFieldA: String
  fourthFieldB: Float
}

union Mixed = First | Second | Third

type Query {
  mixed: Mixed!
  named: Named!
}
"""

_UNION_QUERY = """
query {
  mixed {
    __typename
    ... on First {
      firstFieldA
      firstFieldB
    }
    ... on Second {
      secondFieldA
      secondFieldB
    }
    ... on Third {
      thirdFieldA
      thirdFieldB
    }
  }
}
"""

_INTERFACE_QUERY = """
query {
  named {
    __typename
    name
  }
}
"""


class Human:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class PetType:
    _typename = "Pet"
    id = 1
    name = "Pet"


class First:
    def __init__(self, field_a, field_b):
        self.firstFieldA = field_a  # pylint: disable=invalid-name
        self.firstFieldB = field_b  # pylint: disable=invalid-name


class ThirdType:
    _typename = "Third"

    def __init__(self, field_a, field_b):
        self.thirdFieldA = field_a  # pylint: disable=invalid-name
        self.thirdFieldB = field_b  # pylint: disable=invalid-name

    def __str__(self):
        return f"ThirdType({dict(_typename='ThirdType')})"


class Fourth:
    fourthFieldA = "fourthFieldA"  # pylint: disable=invalid-name
    fourthFieldB = 4.0  # pylint: disable=invalid-name


class UnknownType:
    _typename = "Unknown"

    def __str__(self):
        return f"UnknownType({dict(_typename='Unknown')})"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "result,expected",
    [
        (
            First("firstFieldA", 1),
            {
                "data": {
                    "mixed": {
                        "__typename": "First",
                        "firstFieldA": "firstFieldA",
                        "firstFieldB": 1,
                    }
                }
            },
        ),
        (
            {
                "_typename": "Second",
                "secondFieldA": "secondFieldA",
                "secondFieldB": 2,
            },
            {
                "data": None,
                "errors": [
                    {
                        "message": "Abstract type < Mixed > must resolve to an "
                        "object type at runtime for field < Query.mixed > "
                        "with value < {'_typename': 'Second', 'secondFieldA': 'secondFieldA', 'secondFieldB': 2} >, "
                        "received < dict >. Either the < Mixed > type "
                        "should implements a < @TypeResolver > or the "
                        "< Query.mixed > field resolver should implement "
                        "a `type_resolver` attribute.",
                        "path": ["mixed"],
                        "locations": [{"line": 3, "column": 3}],
                    }
                ],
            },
        ),
        (
            {
                "__typename": "Second",
                "secondFieldA": "secondFieldA",
                "secondFieldB": 2,
            },
            {
                "data": {
                    "mixed": {
                        "__typename": "Second",
                        "secondFieldA": "secondFieldA",
                        "secondFieldB": 2,
                    }
                }
            },
        ),
        (
            ThirdType("thirdFieldA", 3),
            {
                "data": None,
                "errors": [
                    {
                        "message": "Abstract type < Mixed > must resolve to an "
                        "object type at runtime for field < Query.mixed > "
                        "with value < ThirdType({'_typename': 'ThirdType'}) >, "
                        "received < ThirdType >. Either the < Mixed > type "
                        "should implements a < @TypeResolver > or the "
                        "< Query.mixed > field resolver should implement "
                        "a `type_resolver` attribute.",
                        "path": ["mixed"],
                        "locations": [{"line": 3, "column": 3}],
                    }
                ],
            },
        ),
        (
            Fourth(),
            {
                "data": None,
                "errors": [
                    {
                        "message": "Runtime object type < Fourth > is not a possible type for < Mixed >.",
                        "path": ["mixed"],
                        "locations": [{"line": 3, "column": 3}],
                    }
                ],
            },
        ),
        (
            UnknownType(),
            {
                "data": None,
                "errors": [
                    {
                        "message": "Abstract type < Mixed > must resolve to an "
                        "object type at runtime for field < Query.mixed > "
                        "with value < UnknownType({'_typename': 'Unknown'}) >, "
                        "received < UnknownType >. Either the < Mixed > type "
                        "should implements a < @TypeResolver > or the "
                        "< Query.mixed > field resolver should implement "
                        "a `type_resolver` attribute.",
                        "path": ["mixed"],
                        "locations": [{"line": 3, "column": 3}],
                    }
                ],
            },
        ),
    ],
)
async def test_type_resolvers_default_type_resolver(
    random_schema_name, result, expected
):
    def custom_default_type_resolver(result, *args, **kwargs):
        try:
            return result["__typename"]
        except (KeyError, TypeError):
            pass
        return result.__class__.__name__

    @Resolver("Query.mixed", schema_name=random_schema_name)
    async def resolve_query_mixed(parent, args, ctx, info):
        return result

    engine = await create_engine(
        _SDL,
        schema_name=random_schema_name,
        custom_default_type_resolver=custom_default_type_resolver,
    )

    assert await engine.execute(_UNION_QUERY) == expected


@pytest.mark.asyncio
async def test_type_resolvers_type_resolver_unknown_type_0():
    with pytest.raises(
        UnknownTypeDefinition, match="Unknown Type Definition < Unknown >."
    ):
        TypeResolver(
            "Unknown",
            schema_name="test_type_resolvers_type_resolver_unknown_type_0",
        )(lambda result, context, info, abstract_type: "Unknown")

        await create_engine(
            _SDL,
            schema_name="test_type_resolvers_type_resolver_unknown_type_0",
        )


@pytest.mark.asyncio
async def test_type_resolvers_type_resolver_unknown_type_1():
    with pytest.raises(
        InvalidType, match="Type < First > is not an abstract type."
    ):
        TypeResolver(
            "First",
            schema_name="test_type_resolvers_type_resolver_unknown_type_1",
        )(lambda result, context, info, abstract_type: "Unknown")

        await create_engine(
            _SDL,
            schema_name="test_type_resolvers_type_resolver_unknown_type_1",
        )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "result,expected",
    [
        (
            First("firstFieldA", 1),
            {
                "data": {
                    "mixed": {
                        "__typename": "First",
                        "firstFieldA": "firstFieldA",
                        "firstFieldB": 1,
                    }
                }
            },
        ),
        (
            {
                "_typename": "Second",
                "secondFieldA": "secondFieldA",
                "secondFieldB": 2,
            },
            {
                "data": {
                    "mixed": {
                        "__typename": "Second",
                        "secondFieldA": "secondFieldA",
                        "secondFieldB": 2,
                    }
                }
            },
        ),
        (
            ThirdType("thirdFieldA", 3),
            {
                "data": {
                    "mixed": {
                        "__typename": "Third",
                        "thirdFieldA": "thirdFieldA",
                        "thirdFieldB": 3.0,
                    }
                }
            },
        ),
        (
            Fourth(),
            {
                "data": None,
                "errors": [
                    {
                        "message": "Runtime object type < Fourth > is not a possible type for < Mixed >.",
                        "path": ["mixed"],
                        "locations": [{"line": 3, "column": 3}],
                    }
                ],
            },
        ),
        (
            UnknownType(),
            {
                "data": None,
                "errors": [
                    {
                        "message": "Abstract type < Mixed > must resolve to an "
                        "object type at runtime for field < Query.mixed > "
                        "with value < UnknownType({'_typename': 'Unknown'}) >, "
                        "received < Unknown >. Either the < Mixed > type "
                        "should implements a < @TypeResolver > or the "
                        "< Query.mixed > field resolver should implement "
                        "a `type_resolver` attribute.",
                        "path": ["mixed"],
                        "locations": [{"line": 3, "column": 3}],
                    }
                ],
            },
        ),
    ],
)
async def test_union_type_resolvers_default(
    result, expected, random_schema_name
):
    @Resolver("Query.mixed", schema_name=random_schema_name)
    async def resolve_query_mixed(parent, args, ctx, info):
        return result

    engine = await create_engine(_SDL, schema_name=random_schema_name)

    assert await engine.execute(_UNION_QUERY) == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "result,field_type_resolver,expected",
    [
        (
            {"kind": "First", "firstFieldA": "firstFieldA", "firstFieldB": 1},
            lambda result, context, info, abstract_type: result["kind"],
            {
                "data": {
                    "mixed": {
                        "__typename": "First",
                        "firstFieldA": "firstFieldA",
                        "firstFieldB": 1,
                    }
                }
            },
        ),
        (
            {
                "firstFieldA": "firstFieldA",
                "firstFieldB": 1,
                "secondFieldA": "secondFieldA",
                "secondFieldB": 2,
            },
            lambda result, context, info, abstract_type: "Second"
            if "secondFieldA" in result
            else "First",
            {
                "data": {
                    "mixed": {
                        "__typename": "Second",
                        "secondFieldA": "secondFieldA",
                        "secondFieldB": 2,
                    }
                }
            },
        ),
        (
            {"kind": "First", "firstFieldA": "firstFieldA", "firstFieldB": 1},
            lambda result, context, info, abstract_type: "Fourth",
            {
                "data": None,
                "errors": [
                    {
                        "message": "Runtime object type < Fourth > is not a possible type for < Mixed >.",
                        "path": ["mixed"],
                        "locations": [{"line": 3, "column": 3}],
                    }
                ],
            },
        ),
        (
            {"kind": "First", "firstFieldA": "firstFieldA", "firstFieldB": 1},
            lambda result, context, info, abstract_type: "Unknown",
            {
                "data": None,
                "errors": [
                    {
                        "message": "Abstract type < Mixed > must resolve to an "
                        "object type at runtime for field < Query.mixed > "
                        "with value < {'kind': 'First', 'firstFieldA': 'firstFieldA', 'firstFieldB': 1} >, "
                        "received < Unknown >. Either the < Mixed > type "
                        "should implements a < @TypeResolver > or the "
                        "< Query.mixed > field resolver should implement "
                        "a `type_resolver` attribute.",
                        "path": ["mixed"],
                        "locations": [{"line": 3, "column": 3}],
                    }
                ],
            },
        ),
    ],
)
async def test_union_type_resolvers_field_resolver(
    result, field_type_resolver, expected, random_schema_name
):
    @Resolver(
        "Query.mixed",
        type_resolver=field_type_resolver,
        schema_name=random_schema_name,
    )
    async def resolve_query_mixed(parent, args, ctx, info):
        return result

    engine = await create_engine(_SDL, schema_name=random_schema_name)

    assert await engine.execute(_UNION_QUERY) == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "result,type_resolver,expected",
    [
        (
            {"kind": "First", "firstFieldA": "firstFieldA", "firstFieldB": 1},
            lambda result, context, info, abstract_type: result["kind"],
            {
                "data": {
                    "mixed": {
                        "__typename": "First",
                        "firstFieldA": "firstFieldA",
                        "firstFieldB": 1,
                    }
                }
            },
        ),
        (
            {
                "firstFieldA": "firstFieldA",
                "firstFieldB": 1,
                "secondFieldA": "secondFieldA",
                "secondFieldB": 2,
            },
            lambda result, context, info, abstract_type: "Second"
            if "secondFieldA" in result
            else "First",
            {
                "data": {
                    "mixed": {
                        "__typename": "Second",
                        "secondFieldA": "secondFieldA",
                        "secondFieldB": 2,
                    }
                }
            },
        ),
        (
            {"kind": "First", "firstFieldA": "firstFieldA", "firstFieldB": 1},
            lambda result, context, info, abstract_type: "Fourth",
            {
                "data": None,
                "errors": [
                    {
                        "message": "Runtime object type < Fourth > is not a possible type for < Mixed >.",
                        "path": ["mixed"],
                        "locations": [{"line": 3, "column": 3}],
                    }
                ],
            },
        ),
        (
            {"kind": "First", "firstFieldA": "firstFieldA", "firstFieldB": 1},
            lambda result, context, info, abstract_type: "Unknown",
            {
                "data": None,
                "errors": [
                    {
                        "message": "Abstract type < Mixed > must resolve to an "
                        "object type at runtime for field < Query.mixed > "
                        "with value < {'kind': 'First', 'firstFieldA': 'firstFieldA', 'firstFieldB': 1} >, "
                        "received < Unknown >. Either the < Mixed > type "
                        "should implements a < @TypeResolver > or the "
                        "< Query.mixed > field resolver should implement "
                        "a `type_resolver` attribute.",
                        "path": ["mixed"],
                        "locations": [{"line": 3, "column": 3}],
                    }
                ],
            },
        ),
    ],
)
async def test_union_type_resolvers_type_resolver(
    type_resolver, result, expected, random_schema_name
):
    TypeResolver("Mixed", schema_name=random_schema_name)(type_resolver)

    @Resolver("Query.mixed", schema_name=random_schema_name)
    async def resolve_query_mixed(parent, args, ctx, info):
        return result

    engine = await create_engine(_SDL, schema_name=random_schema_name)

    assert await engine.execute(_UNION_QUERY) == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "result,expected",
    [
        (
            Human(1, "Human"),
            {"data": {"named": {"__typename": "Human", "name": "Human"}}},
        ),
        (
            {"_typename": "Alien", "name": "Alien"},
            {"data": {"named": {"__typename": "Alien", "name": "Alien"}}},
        ),
        (
            PetType(),
            {
                "data": None,
                "errors": [
                    {
                        "message": "Runtime object type < Pet > is not a possible type for < Named >.",
                        "path": ["named"],
                        "locations": [{"line": 3, "column": 3}],
                    }
                ],
            },
        ),
        (
            UnknownType(),
            {
                "data": None,
                "errors": [
                    {
                        "message": "Abstract type < Named > must resolve to an object type at runtime for field < Query.named > with value < UnknownType({'_typename': 'Unknown'}) >, received < Unknown >. Either the < Named > type should implements a < @TypeResolver > or the < Query.named > field resolver should implement a `type_resolver` attribute.",
                        "path": ["named"],
                        "locations": [{"line": 3, "column": 3}],
                    }
                ],
            },
        ),
    ],
)
async def test_interface_type_resolvers_default(
    result, expected, random_schema_name
):
    @Resolver("Query.named", schema_name=random_schema_name)
    async def resolve_query_named(parent, args, ctx, info):
        return result

    engine = await create_engine(_SDL, schema_name=random_schema_name)

    assert await engine.execute(_INTERFACE_QUERY) == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "result,field_type_resolver,expected",
    [
        (
            {"kind": "Human", "name": "Human"},
            lambda result, context, info, abstract_type: result["kind"],
            {"data": {"named": {"__typename": "Human", "name": "Human"}}},
        ),
        (
            {"kind": "Human", "name": "Human"},
            lambda result, context, info, abstract_type: "Fourth",
            {
                "data": None,
                "errors": [
                    {
                        "message": "Runtime object type < Fourth > is not a possible type for < Named >.",
                        "path": ["named"],
                        "locations": [{"line": 3, "column": 3}],
                    }
                ],
            },
        ),
        (
            {"kind": "Human", "name": "Human"},
            lambda result, context, info, abstract_type: "Unknown",
            {
                "data": None,
                "errors": [
                    {
                        "message": "Abstract type < Named > must resolve to an "
                        "object type at runtime for field < Query.named > "
                        "with value < {'kind': 'Human', 'name': 'Human'} >, "
                        "received < Unknown >. Either the < Named > type "
                        "should implements a < @TypeResolver > or the "
                        "< Query.named > field resolver should implement "
                        "a `type_resolver` attribute.",
                        "path": ["named"],
                        "locations": [{"line": 3, "column": 3}],
                    }
                ],
            },
        ),
    ],
)
async def test_interface_type_resolvers_field_resolver(
    result, field_type_resolver, expected, random_schema_name
):
    @Resolver(
        "Query.named",
        type_resolver=field_type_resolver,
        schema_name=random_schema_name,
    )
    async def resolve_query_named(parent, args, ctx, info):
        return result

    engine = await create_engine(_SDL, schema_name=random_schema_name)

    assert await engine.execute(_INTERFACE_QUERY) == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "result,type_resolver,expected",
    [
        (
            {"kind": "Human", "name": "Human"},
            lambda result, context, info, abstract_type: result["kind"],
            {"data": {"named": {"__typename": "Human", "name": "Human"}}},
        ),
        (
            {"kind": "Human", "name": "Human"},
            lambda result, context, info, abstract_type: "Fourth",
            {
                "data": None,
                "errors": [
                    {
                        "message": "Runtime object type < Fourth > is not a possible type for < Named >.",
                        "path": ["named"],
                        "locations": [{"line": 3, "column": 3}],
                    }
                ],
            },
        ),
        (
            {"kind": "Human", "name": "Human"},
            lambda result, context, info, abstract_type: "Unknown",
            {
                "data": None,
                "errors": [
                    {
                        "message": "Abstract type < Named > must resolve to an "
                        "object type at runtime for field < Query.named > "
                        "with value < {'kind': 'Human', 'name': 'Human'} >, "
                        "received < Unknown >. Either the < Named > type "
                        "should implements a < @TypeResolver > or the "
                        "< Query.named > field resolver should implement "
                        "a `type_resolver` attribute.",
                        "path": ["named"],
                        "locations": [{"line": 3, "column": 3}],
                    }
                ],
            },
        ),
    ],
)
async def test_interface_type_resolvers_type_resolver(
    type_resolver, result, expected, random_schema_name
):
    TypeResolver("Named", schema_name=random_schema_name)(type_resolver)

    @Resolver("Query.named", schema_name=random_schema_name)
    async def resolve_query_named(parent, args, ctx, info):
        return result

    engine = await create_engine(_SDL, schema_name=random_schema_name)

    assert await engine.execute(_INTERFACE_QUERY) == expected
