from typing import Any, Callable, Dict, Optional, Union

import pytest

from tartiflette import Directive, Resolver, Scalar, create_engine
from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import StringValueNode
from tests.functional.utils import is_expected

_PET_DATASET = [
    {
        "_typename": "Dog",
        "id": 1,
        "name": "Dog",
        "nickname": "Doggo",
        "barkVolume": 10,
    },
    {
        "_typename": "Cat",
        "id": 2,
        "name": "Cat",
        "nickname": "Catto",
        "meowVolume": 5,
    },
    {
        "_typename": "Dog",
        "id": 3,
        "name": "Lil Dog",
        "nickname": "Doggy",
        "barkVolume": 4,
    },
]

_SDL = """
scalar CapitalizedString @concatenate(with: "scalar")

directive @validateMaxLength(
  limit: Int!
) on ARGUMENT_DEFINITION | INPUT_FIELD_DEFINITION

directive @concatenate(
  with: String! @validateMaxLength(limit: 25)
) on SCALAR | FIELD_DEFINITION | FIELD

interface Identifiable {
  id: Int!
}

interface Named {
  name: CapitalizedString!
}

enum OrderDirection { ASC, DESC }
enum OwnerOrderField { NAME }
enum PetOrderField { NAME, NICKNAME }
enum OwnerKind { ALIEN, HUMAN }
enum PetKind { CAT, DOG }
enum CatCommand { JUMP }
enum DogCommand { SIT, DOWN, HEEL }

type Alien implements Identifiable & Named {
  id: Int!
  name: CapitalizedString! @concatenate(with: "Alien.name")
}

type Human implements Identifiable & Named {
  id: Int!
  name: CapitalizedString! @concatenate(with: "Human.name")
  owner: Alien
}

type Cat implements Identifiable & Named {
  id: Int!
  name: CapitalizedString! @concatenate(with: "Cat.name")
  nickname: String
  doesKnowCommand(catCommand: CatCommand!): Boolean!
  meowVolume: Int
  owner: Human
  friends: [Pet!]
}

type Dog implements Identifiable & Named {
  id: Int!
  name: CapitalizedString! @concatenate(with: "Dog.name")
  nickname: String
  doesKnowCommand(dogCommand: DogCommand!): Boolean!
  barkVolume: Int
  owner: Human
  friends: [Pet!]
}

union Pet = Cat | Dog
union Owner = Alien | Human

input OwnerOrder {
  field: OwnerOrderField!
  direction: OrderDirection!
}

input PetOrder {
  field: PetOrderField!
  direction: OrderDirection!
}

input AddCatInput {
  clientMutationId: String
  name: String!
  nickname: String
  knownCommands: [DogCommand!]
  barkVolume: Int
  ownerId: Int
  friendIds: [Int!]
}

type AddCatPayload {
  clientMutationId: String
  cat: Cat!
}

input AddDogInput {
  clientMutationId: String
  name: String!
  nickname: String
  knownCommands: [DogCommand!]
  meowVolume: Int
  ownerId: Int
  friendIds: [Int!]
}

type AddDogPayload {
  clientMutationId: String
  dog: Dog!
}

input AddHumanInput {
  clientMutationId: String
  name: String!
  ownerId: Int
}

type AddHumanPayload {
  clientMutationId: String
  human: Human!
}

input AddAlienInput {
  clientMutationId: String
  name: String!
}

type AddAlienPayload {
  clientMutationId: String
  alien: Alien!
}

type Query {
  pet(id: Int!): Pet
  pets(ids: [Int!], orderBy: PetOrder, kind: PetKind): [Pet!]
  nullablePets(ids: [Int!], orderBy: PetOrder, kind: PetKind): [Pet]

  owner(id: Int!): Pet
  owners(ids: [Int!], orderBy: OwnerOrder, kind: OwnerKind): [Owner!]
}

type Mutation {
  addCat(input: AddCatInput!): AddCatPayload!
  addDog(input: AddDogInput!): AddDogPayload!
  addHuman(input: AddHumanInput!): AddHumanPayload!
  addAlien(input: AddAlienInput!): AddAlienPayload!
}

type Subscription {
  petAdded(kind: PetKind): Pet
  ownerAdded(kind: OwnerKind): Owner
}

schema {
  query: Query
  mutation: Mutation
  subscription: Subscription
}
"""


@pytest.fixture(scope="module")
async def ttftt_engine():
    @Scalar("CapitalizedString", schema_name="test_oh_god")
    class CapitalizedString:
        @staticmethod
        def coerce_output(val) -> str:
            return str(val)

        @staticmethod
        def coerce_input(val: str) -> str:
            if not isinstance(val, str):
                raise TypeError(
                    f"String cannot represent a non string value: < {val} >."
                )
            return val.capitalize()

        @staticmethod
        def parse_literal(ast: "Node") -> Union[str, "UNDEFINED_VALUE"]:
            return (
                ast.value.capitalize()
                if isinstance(ast, StringValueNode)
                else UNDEFINED_VALUE
            )

    @Directive("validateMaxLength", schema_name="test_oh_god")
    class ValidateMaxLengthDirective:
        @staticmethod
        async def on_field_execution(
            directive_args: Dict[str, Any],
            next_resolver: Callable,
            parent: Optional[Any],
            args: Dict[str, Any],
            ctx: Optional[Any],
            info: "ResolveInfo",
        ) -> Any:
            result = await next_resolver(parent, args, ctx, info)
            if len(result) > directive_args["limit"]:
                raise Exception(
                    f"Value of field < {info.schema_field.name} is too long."
                )
            return result

        @staticmethod
        async def on_argument_execution(
            directive_args: Dict[str, Any],
            next_directive: Callable,
            parent_node: Union["FieldNode", "DirectiveNode"],
            argument_node: "ArgumentNode",
            value: Any,
            ctx: Optional[Any],
        ) -> Any:
            result = await next_directive(
                parent_node, argument_node, value, ctx
            )
            if len(result) > directive_args["limit"]:
                raise Exception(
                    f"Value of argument < {argument_node.name.value} > is too "
                    "long."
                )
            return result

    @Directive("concatenate", schema_name="test_oh_god")
    class ConcatenateDirective:
        @staticmethod
        async def on_field_execution(
            directive_args: Dict[str, Any],
            next_resolver: Callable,
            parent: Optional[Any],
            args: Dict[str, Any],
            ctx: Optional[Any],
            info: "ResolveInfo",
        ) -> Any:
            result = await next_resolver(parent, args, ctx, info)
            return (
                f'{result}+{directive_args["with"]}'
                if isinstance(result, str)
                else result
            )

        @staticmethod
        async def on_argument_execution(
            directive_args: Dict[str, Any],
            next_directive: Callable,
            parent_node: Union["FieldNode", "DirectiveNode"],
            argument_node: "ArgumentNode",
            value: Any,
            ctx: Optional[Any],
        ) -> Any:
            result = await next_directive(
                parent_node, argument_node, value, ctx
            )
            return (
                f'{result}+{directive_args["with"]}'
                if isinstance(result, str)
                else result
            )

    @Resolver("Query.pets", schema_name="test_oh_god")
    @Resolver("Query.nullablePets", schema_name="test_oh_god")
    async def resolve_query_pets(parent, args, ctx, info):
        kind = args.get("kind")
        return [
            pet
            for pet in _PET_DATASET
            if kind is None or kind == pet["_typename"].upper()
        ]

    @Resolver("Cat.doesKnowCommand", schema_name="test_oh_god")
    @Resolver("Dog.doesKnowCommand", schema_name="test_oh_god")
    async def resolve_pet_does_know_command(*_, **__):
        return True

    @Resolver("Cat.owner", schema_name="test_oh_god")
    @Resolver("Dog.owner", schema_name="test_oh_god")
    async def resolve_pet_owner(*_, **__):
        return {"id": 1, "name": "Hooman"}

    @Resolver("Cat.friends", schema_name="test_oh_god")
    @Resolver("Dog.friends", schema_name="test_oh_god")
    async def resolve_pet_friends(*_, **__):
        return _PET_DATASET

    return await create_engine(_SDL, schema_name="test_oh_god")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """
            fragment HumanFields on Human {
              __typename
              id
              name
            }

            fragment LightPetFields on Pet {
              # __typename
              ... on Cat {
                id
                name
              }
              ... on Dog {
                id
                name
              }
            }

            query PetQuery {
              pets(ids: [1, 10, 15], orderBy: { field: NAME, direction: ASC }, kind: DOG) {
                # __typename
                ... on Cat {
                  id
                  name
                  nickname @concatenate(with: "Cat.nickname")
                  doesKnowCommand(catCommand: JUMP)
                  meowVolume
                  owner {
                    ...HumanFields
                  }
                  friends {
                    ...LightPetFields
                  }
                }
                ... on Dog {
                  id
                  name
                  nickname @concatenate(with: "Dog.nickname")
                  doesKnowCommand(dogCommand: SIT)
                  barkVolume
                  owner {
                    ...HumanFields
                  }
                  friends {
                    ...LightPetFields
                  }
                }
              }
            }
            """,
            None,
            {
                "data": {
                    "pets": [
                        {
                            "id": 1,
                            "name": "Dog+Dog.name",
                            "nickname": "Doggo+Dog.nickname",
                            "doesKnowCommand": True,
                            "barkVolume": 10,
                            "owner": {
                                "__typename": "Human",
                                "id": 1,
                                "name": "Hooman+Human.name",
                            },
                            "friends": [
                                {"id": 1, "name": "Dog+Dog.name"},
                                {"id": 2, "name": "Cat+Cat.name"},
                                {"id": 3, "name": "Lil Dog+Dog.name"},
                            ],
                        },
                        {
                            "id": 3,
                            "name": "Lil Dog+Dog.name",
                            "nickname": "Doggy+Dog.nickname",
                            "doesKnowCommand": True,
                            "barkVolume": 4,
                            "owner": {
                                "__typename": "Human",
                                "id": 1,
                                "name": "Hooman+Human.name",
                            },
                            "friends": [
                                {"id": 1, "name": "Dog+Dog.name"},
                                {"id": 2, "name": "Cat+Cat.name"},
                                {"id": 3, "name": "Lil Dog+Dog.name"},
                            ],
                        },
                    ]
                }
            },
        ),
        (
            """
            query PetQuery {
              pets {
                ... on Cat {
                  id
                  name @concatenate(with: "Catto")
                }
                ... on Dog {
                  id
                  name @concatenate(with: "Doggo")
                }
              }
            }
            """,
            None,
            {
                "data": {
                    "pets": [
                        {"id": 1, "name": "Dog+Dog.name+Doggo"},
                        {"id": 2, "name": "Cat+Cat.name+Catto"},
                        {"id": 3, "name": "Lil Dog+Dog.name+Doggo"},
                    ]
                }
            },
        ),
        (
            """
            query PetQuery {
              pets {
                ... on Cat @skip(if: true) {
                  id
                  name @concatenate(with: "suffixWayTooLongToBeAValidOne")
                }
                ... on Dog {
                  id
                  name @concatenate(with: "suffixWayTooLongToBeAValidOne")
                }
              }
            }
            """,
            None,
            {
                "data": {"pets": None},
                "errors": [
                    {
                        "message": "Value of argument < with > is too long.",
                        "path": ["pets", 0, "name"],
                        "locations": [{"line": 10, "column": 37}],
                    },
                    {
                        "message": "Value of argument < with > is too long.",
                        "path": ["pets", 2, "name"],
                        "locations": [{"line": 10, "column": 37}],
                    },
                ],
            },
        ),
        (
            """
            query {
              nullablePets {
                ... on Cat @skip(if: true) {
                  id
                  name @concatenate(with: "suffixWayTooLongToBeAValidOne")
                }
                ... on Dog {
                  id
                  name @concatenate(with: "suffixWayTooLongToBeAValidOne")
                }
              }
            }
            """,
            None,
            {
                "data": {"nullablePets": [None, {}, None]},
                "errors": [
                    {
                        "message": "Value of argument < with > is too long.",
                        "path": ["nullablePets", 0, "name"],
                        "locations": [{"line": 10, "column": 37}],
                    },
                    {
                        "message": "Value of argument < with > is too long.",
                        "path": ["nullablePets", 2, "name"],
                        "locations": [{"line": 10, "column": 37}],
                    },
                ],
            },
        ),
    ],
)
async def test_oh_god(query, variables, expected, ttftt_engine):
    is_expected(
        await ttftt_engine.execute(query, variables=variables), expected
    )
