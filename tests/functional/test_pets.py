import pytest

from tests.functional.reusable.pets.storage import PETS, find_object


async def resolve_query_version(parent, args, ctx, info):
    return "v0.1.0"


async def resolve_query_service_status(parent, args, ctx, info):
    return "UP"


async def resolve_query_human(parent, args, ctx, info):
    return find_object("Human", args["id"])


async def resolve_query_pet(parent, args, ctx, info):
    return find_object("Pet", args["id"])


async def resolve_query_pets(parent, args, ctx, info):
    return [find_object("Pet", pet.split(".")[1]) for pet in PETS]


async def resolve_friends(parent, args, ctx, info):
    friend_ids = parent.get("friend_ids")
    if friend_ids is None:
        return None

    friends = []
    for friend_type_id in friend_ids:
        friend_type, friend_id = friend_type_id.split(".")
        friends.append(find_object(friend_type, friend_id))
    return friends


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    name="pets",
    resolvers={
        "MyQuery.version": resolve_query_version,
        "MyQuery.serviceStatus": resolve_query_service_status,
        "MyQuery.human": resolve_query_human,
        "Human.friends": resolve_friends,
        "MyQuery.pet": resolve_query_pet,
        "Cat.friends": resolve_friends,
        "Dog.friends": resolve_friends,
    },
)
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """
            {
              __typename
              version
            }
            """,
            None,
            {"data": {"__typename": "MyQuery", "version": "v0.1.0"}},
        ),
        (
            """
            {
              __typename
              serviceStatus
            }
            """,
            None,
            {"data": {"__typename": "MyQuery", "serviceStatus": "UP"}},
        ),
        (
            """
            {
              human(id: 1) {
                __typename
                id
                name
              }
            }
            """,
            None,
            {
                "data": {
                    "human": {
                        "__typename": "Human",
                        "id": 1,
                        "name": "Human 1",
                    }
                }
            },
        ),
        (
            """
            {
              human(id: 1) {
                __typename
                id
                name
                friends {
                  __typename
                  ... on Human {
                    id
                  }
                  ... on Cat {
                    id
                  }
                  ... on Dog {
                    id
                  }
                }
              }
            }
            """,
            None,
            {
                "data": {
                    "human": {
                        "__typename": "Human",
                        "id": 1,
                        "name": "Human 1",
                        "friends": [{"__typename": "Human", "id": 2}],
                    }
                }
            },
        ),
        (
            """
            {
              human(id: 999) {
                __typename
                id
                name
                friends {
                  __typename
                  ... on Human {
                    id
                  }
                  ... on Cat {
                    id
                  }
                  ... on Dog {
                    id
                  }
                }
              }
            }
            """,
            None,
            {
                "data": {"human": None},
                "errors": [
                    {
                        "message": "Object < Human.999 > doesn't exists.",
                        "path": ["human"],
                        "locations": [{"line": 3, "column": 15}],
                        "extensions": {"kind": "Human", "id": 999},
                    }
                ],
            },
        ),
        (
            """
            {
              pet(id: 1) {
                __typename
                id
                name
                friends {
                  __typename
                  ... on Human {
                    id
                  }
                  ... on Cat {
                    id
                  }
                  ... on Dog {
                    id
                  }
                }
              }
            }
            """,
            None,
            {
                "data": {
                    "pet": {
                        "__typename": "Dog",
                        "id": 1,
                        "name": "Dog 1",
                        "friends": None,
                    }
                },
                "errors": [
                    {
                        "message": "Runtime object type < Human > is not a possible type for < Pet >.",
                        "path": ["pet", "friends", 1],
                        "locations": [{"line": 7, "column": 17}],
                    }
                ],
            },
        ),
        (
            """
            {
              pet(id: 2) {
                __typename
                id
                name
                friends {
                  __typename
                  ... on Human {
                    id
                  }
                  ... on Cat {
                    id
                  }
                  ... on Dog {
                    id
                  }
                }
              }
            }
            """,
            None,
            {
                "data": {
                    "pet": {
                        "__typename": "Cat",
                        "id": 2,
                        "name": "Cat 2",
                        "friends": [
                            {"__typename": "Dog", "id": 1},
                            {"__typename": "Cat", "id": 3},
                            {"__typename": "Dog", "id": 5},
                        ],
                    }
                }
            },
        ),
        (
            """
            {
              human(id: 999) {
                __typename
                id
                name
                friends {
                  __typename
                  ... on Human {
                    id
                  }
                  ... on Cat {
                    id
                  }
                  ... on Dog {
                    id
                  }
                }
              }
            }
            """,
            None,
            {
                "data": {"human": None},
                "errors": [
                    {
                        "message": "Object < Human.999 > doesn't exists.",
                        "path": ["human"],
                        "locations": [{"line": 3, "column": 15}],
                        "extensions": {"kind": "Human", "id": 999},
                    }
                ],
            },
        ),
    ],
)
async def test_pets(engine, query, variables, expected):
    assert await engine.execute(query, variables=variables) == expected


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    name="pets", resolvers={"MyQuery.pets": resolve_query_pets}
)
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """
            query ($petFilters: PetFilters) {
              pets(filters: $petFilters) { ... on Dog { name } }
            }
            """,
            {"petFilters": {"kind": "DG"}},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $petFilters > got invalid value < {'kind': 'DG'} >; Expected type < PetKind > at value.kind; Did you mean DOG?",
                        "path": None,
                        "locations": [{"line": 2, "column": 20}],
                    }
                ],
            },
        ),
        (
            """
            query ($petFilters: PetFilters) {
              pets(filters: $petFilters) { ... on Dog { name } }
            }
            """,
            {"petFilters": {"kind": "CA"}},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $petFilters > got invalid value < {'kind': 'CA'} >; Expected type < PetKind > at value.kind; Did you mean CAT?",
                        "path": None,
                        "locations": [{"line": 2, "column": 20}],
                    }
                ],
            },
        ),
        (
            """
            query ($petFilters: PetFilters) {
              pets(filters: $petFilters) { ... on Dog { name } }
            }
            """,
            {"petFilters": {"na": "C"}},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $petFilters > got invalid value < {'na': 'C'} >; Field < na > is not defined by type < PetFilters >; Did you mean name?",
                        "path": None,
                        "locations": [{"line": 2, "column": 20}],
                    }
                ],
            },
        ),
        (
            """
            query ($petFilters: PetFilters) {
              pets(filters: $petFilters) { ... on Dog { name } }
            }
            """,
            {"petFilters": {"hasien": True}},
            {
                "data": None,
                "errors": [
                    {
                        "message": "Variable < $petFilters > got invalid value < {'hasien': True} >; Field < hasien > is not defined by type < PetFilters >; Did you mean hasFriends or hasChildren?",
                        "path": None,
                        "locations": [{"line": 2, "column": 20}],
                    }
                ],
            },
        ),
    ],
)
async def test_pets_errors(engine, query, variables, expected):
    assert await engine.execute(query, variables=variables) == expected
