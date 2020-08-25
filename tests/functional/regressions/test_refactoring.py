import pytest

from tartiflette import Resolver

_EXPECTED = {
    "data": {
        "dog": {
            "name": "Dog",
            "nickname": "Doggo",
            "barkVolume": 2,
            "doesKnowCommand": True,
            "isHousetrained": False,
            "owner": {"name": "Hooman"},
        }
    }
}


def bakery(schema_name):
    @Resolver("Query.dog", schema_name=schema_name)
    async def resolve_query_dog(parent, args, ctx, info):
        return {"name": "Dog", "nickname": "Doggo", "barkVolume": 2}

    @Resolver("Dog.doesKnowCommand", schema_name=schema_name)
    async def resolve_dog_does_know_command(parent, args, ctx, info):
        return True

    @Resolver("Dog.isHousetrained", schema_name=schema_name)
    async def resolve_dog_is_housetrained(parent, args, ctx, info):
        return False

    @Resolver("Dog.owner", schema_name=schema_name)
    async def resolve_dog_owner(parent, args, ctx, info):
        return {"name": "Hooman"}

    @Resolver("Dog.friends", schema_name=schema_name)
    async def resolve_dog_friends(parent, args, ctx, info):
        return [
            {"_typename": "Dog", "name": "Dog", "nickname": "Doggo"},
            {"_typename": "Cat", "name": "Cat", "nickname": "Catto"},
        ]

    @Resolver("Query.cat", schema_name=schema_name)
    async def resolve_query_cat(parent, args, ctx, info):
        return {"name": "Cat", "nickname": "Catto", "meowVolume": 1}

    @Resolver("Cat.doesKnowCommand", schema_name=schema_name)
    async def resolve_cat_does_know_command(parent, args, ctx, info):
        return False

    @Resolver("Query.human", schema_name=schema_name)
    async def resolve_query_human(parent, args, ctx, info):
        return {"name": "Hooman"}

    @Resolver("Query.catOrDog", schema_name=schema_name)
    async def resolve_query_cat_or_dog(parent, args, ctx, info):
        return {"_typename": "Dog", "name": "Dog", "nickname": "Doggo"}


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="animals", bakery=bakery)
@pytest.mark.parametrize(
    "operation_name,query,variables,expected",
    [
        (
            None,
            """
            query {
              dog {
                name
                nickname
                barkVolume
                doesKnowCommand(dogCommand: DOWN)
                isHousetrained(atOtherHomes: true)
                owner {
                  name
                }
              }
            }
            """,
            None,
            _EXPECTED,
        ),
        (
            "Dog",
            """
            query Dog {
              dog {
                name
                nickname
                barkVolume
                doesKnowCommand(dogCommand: DOWN)
                isHousetrained(atOtherHomes: true)
                owner {
                  name
                }
              }
            }

            query Cat {
              cat {
                ... on Dog {
                  name
                }
                name
              }
            }
            """,
            None,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Fragment cannot be spread here as objects of type < Cat > can never be of type < Dog >.",
                        "path": None,
                        "locations": [{"line": 17, "column": 17}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.5.2.3",
                            "tag": "fragment-spread-is-possible",
                            "details": "https://spec.graphql.org/June2018/#sec-Fragment-spread-is-possible",
                        },
                    }
                ],
            },
        ),
        (
            None,
            """
            fragment CatOrDogFields on CatOrDog {
              ... on Dog {
                name
                dogNickname: nickname
              }
              ... on Cat {
                name
                catNickname: nickname
              }
            }

            query {
              catOrDog(id: 1) {
                ... on Dog {
                  name
                  friends {
                    ...CatOrDogFields
                  }
                }
                ... on Cat {
                  name
                  catNickname: nickname
                }
              }
            }
            """,
            None,
            {
                "data": {
                    "catOrDog": {
                        "name": "Dog",
                        "friends": [
                            {"dogNickname": "Doggo", "name": "Dog"},
                            {"catNickname": "Catto", "name": "Cat"},
                        ],
                    }
                }
            },
        ),
        (
            "Dog",
            """
            fragment HumanFields on Human {
              ... on Human {
                name
              }
            }

            fragment LightCatOrDogFields on CatOrDog {
               ... on Cat {
                 name
                 nickname
               }
               ... on Dog {
                 name
                 nickname
               }
            }

            fragment LightDogFields on Dog {
              name
              barkVolume
            }

            fragment DogFields on Dog {
              name
              doesKnowCommand(dogCommand: DOWN)
              isHousetrained(atOtherHomes: true)
              owner {
                ... on Human {
                  ...HumanFields
                }
              }
              friends {
                ...LightCatOrDogFields
              }
            }

            fragment CatFields on Cat {
              name
            }

            fragment QueryDogFields on Query {
              ... on Query {
                ... {
                  dog {
                    ... on Dog {
                      ...DogFields
                    }
                  }
                  dog {
                    name
                    nickname
                    barkVolume
                  }
                  dog {
                    ...LightDogFields
                  }
                }
              }
            }

            query Dog {
              ... on Query {
                ...QueryDogFields
              }
            }

            query Cat {
              cat {
                ...CatFields
              }
            }
            """,
            None,
            {
                "data": {
                    "dog": {
                        "name": "Dog",
                        "nickname": "Doggo",
                        "barkVolume": 2,
                        "doesKnowCommand": True,
                        "isHousetrained": False,
                        "owner": {"name": "Hooman"},
                        "friends": [
                            {"name": "Dog", "nickname": "Doggo"},
                            {"name": "Cat", "nickname": "Catto"},
                        ],
                    }
                }
            },
        ),
        (
            None,
            """
            query CatOrDog {
              catOrDog(id: 1) {
                ... on Dog {
                  name
                }
                ... on Dog {
                  nickname
                }
                ... on Cat {
                  name
                }
              }
            }
            """,
            None,
            {"data": {"catOrDog": {"name": "Dog", "nickname": "Doggo"}}},
        ),
        (
            "Dog",
            """
            fragment HumanFields on Human {
              ... on Human {
                name
              }
            }

            fragment DogFields on Dog {
              name
              nickname
              barkVolume
              doesKnowCommand(dogCommand: $dogCommand)
              isHousetrained(atOtherHomes: $atOtherHomes)
              owner {
                ... on Human {
                  ...HumanFields
                }
              }
            }

            fragment CatFields on Cat {
              name
            }

            fragment QueryDogFields on Query {
              ... on Query {
                dog {
                  ... on Dog {
                    ...DogFields
                  }
                }
              }
            }

            query Dog($dogCommand: DogCommand!, $atOtherHomes: Boolean) {
              ... on Query {
                ...QueryDogFields
              }
            }

            query Cat {
              cat {
                ...CatFields
              }
            }
            """,
            {"dogCommand": "DOWN", "atOtherHomes": True},
            _EXPECTED,
        ),
        (
            "Dog",
            """
            fragment HumanFields on Human {
              ... on Human {
                name
              }
            }

            fragment DogFields on Dog {
              name
              nickname
              barkVolume
              doesKnowCommand(dogCommand: $dogCommand)
              isHousetrained(atOtherHomes: $atOtherHomes)
              owner {
                ... on Human {
                  ...HumanFields
                }
              }
            }

            fragment CatFields on Cat {
              name
            }

            fragment QueryDogFields on Query {
              ... on Query {
                dog {
                  ... on Dog {
                    ...DogFields
                  }
                }
              }
            }

            query Dog($dogCommand: DogCommand! = DOWN, $atOtherHomes: Boolean = true) {
              ... on Query {
                ...QueryDogFields
              }
            }

            query Cat {
              cat {
                ...CatFields
              }
            }
            """,
            None,
            _EXPECTED,
        ),
    ],
)
async def test_refactoring(
    schema_stack, operation_name, query, variables, expected
):
    assert (
        await schema_stack.execute(
            query, operation_name=operation_name, variables=variables
        )
        == expected
    )
