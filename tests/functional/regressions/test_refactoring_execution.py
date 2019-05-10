import pytest


async def resolve_query_dog(parent, args, ctx, info):
    return {"name": "Dog", "nickname": "Doggo", "barkVolume": 2}


async def resolve_dog_does_know_command(parent, args, ctx, info):
    return True


async def resolve_dog_is_housetrained(parent, args, ctx, info):
    return False


async def resolve_dog_owner(parent, args, ctx, info):
    return {"name": "Hooman"}


async def resolve_query_cat(parent, args, ctx, info):
    return {"name": "Cat", "nickname": "Catto", "meowVolume": 1}


async def resolve_cat_does_know_command(parent, args, ctx, info):
    return False


async def resolve_query_human(parent, args, ctx, info):
    return {"name": "Hooman"}


async def resolve_query_cat_or_dog(parent, args, ctx, info):
    return {"_typename": "Dog", "name": "Dog", "nickname": "Doggo"}


async def resolve_dog_friends(parent, args, ctx, info):
    return [
        {"_typename": "Dog", "name": "Dog", "nickname": "Doggo"},
        {"_typename": "Cat", "name": "Cat", "nickname": "Catto"},
    ]


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


@pytest.mark.asyncio
@pytest.mark.ttftt_engine(
    resolvers={
        "Query.dog": resolve_query_dog,
        "Dog.doesKnowCommand": resolve_dog_does_know_command,
        "Dog.isHousetrained": resolve_dog_is_housetrained,
        "Dog.owner": resolve_dog_owner,
        "Dog.friends": resolve_dog_friends,
        "Query.cat": resolve_query_cat,
        "Cat.doesKnowCommand": resolve_cat_does_know_command,
        "Query.human": resolve_query_human,
        "Query.catOrDog": resolve_query_cat_or_dog,
    }
)
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

            fragment LightDogFields on Dog @myDirective0 {
              name
              barkVolume
            }

            fragment DogFields on Dog @myDirective8 {
              name @myDirective9
              doesKnowCommand(dogCommand: DOWN)
              isHousetrained(atOtherHomes: true)
              owner {
                ... on Human {
                  ...HumanFields
                  ...CatFields
                }
              }
              friends {
                ...LightCatOrDogFields
              }
            }

            fragment CatFields on Cat {
              name
            }

            fragment QueryDogFields on Query @myDirective3 {
              ... on Query @myDirective4 {
                ... @myDirective5_1 {
                  dog @myDirective5 {
                    ... on Dog @myDirective6 {
                      ...DogFields @myDirective7
                    }
                  }
                  dog {
                    name
                    nickname @myDirective10
                    barkVolume
                  }
                  dog {
                    ...LightDogFields
                  }
                }
              }
            }

            query Dog {
              ... on Query @myDirective1 {
                ...QueryDogFields @myDirective2
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
                    "pets": [
                        {
                            "barkVolume": 10,
                            "doesKnowCommand": True,
                            "friends": [
                                {"id": 1, "name": "Dog+Dog.name"},
                                {"id": 2, "name": "Cat+Cat.name"},
                            ],
                            "id": 1,
                            "name": "Dog+Dog.name",
                            "nickname": "Doggo+Dog.nickname",
                            "owner": {
                                "__typename": "Human",
                                "id": 1,
                                "name": "Hooman+Human.name",
                            },
                        }
                    ]
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
    ],
)
async def test_refactoring_execution(
    engine, operation_name, query, variables, expected
):
    assert (
        await engine.execute(
            query, operation_name=operation_name, variables=variables
        )
        == expected
    )
