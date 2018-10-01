import asyncio
from tartiflette.resolver import Resolver
from starwars.sdl import STARWARSTIFLETTE

_LUKE = {
    "type": "Human",
    "id": "1000",
    "name": "Luke Skywalker",
    "friends": ["1002", "1003", "2000", "2001"],
    "appearsIn": [4, 5, 6],
    "homePlanet": "Tatooine",
}

_VADER = {
    "type": "Human",
    "id": "1001",
    "name": "Darth Vader",
    "friends": ["1004"],
    "appearsIn": [4, 5, 6],
    "homePlanet": "Tatooine",
}

_HAN = {
    "type": "Human",
    "id": "1002",
    "name": "Han Solo",
    "friends": ["1000", "1003", "2001"],
    "appearsIn": [4, 5, 6],
}

_LEIA = {
    "type": "Human",
    "id": "1003",
    "name": "Leia Organa",
    "friends": ["1000", "1002", "2000", "2001"],
    "appearsIn": [4, 5, 6],
    "homePlanet": "Alderaan",
}

_TARKIN = {
    "type": "Human",
    "id": "1004",
    "name": "Wilhuff Tarkin",
    "friends": ["1001"],
    "appearsIn": [4],
}

_HUMAN_DATA = {
    "1000": _LUKE,
    "1001": _VADER,
    "1002": _HAN,
    "1003": _LEIA,
    "1004": _TARKIN,
}

_THREEPIO = {
    "type": "Droid",
    "id": "2000",
    "name": "C-3PO",
    "friends": ["1000", "1002", "1003", "2001"],
    "appearsIn": [4, 5, 6],
    "primaryFunction": "Protocol",
}

_ARTOO = {
    "type": "Droid",
    "id": "2001",
    "name": "R2-D2",
    "friends": ["1000", "1002", "1003"],
    "appearsIn": [4, 5, 6],
    "primaryFunction": "Astromech",
}

_DROID_DATA = {"2000": _THREEPIO, "2001": _ARTOO}

_EPISODE = {4: "NEWHOPE", 5: "EMPIRE", 6: "JEDI"}


@Resolver("Query.hero", schema=STARWARSTIFLETTE.schema)
async def resolver_hero(_, arguments, __, ___):
    if arguments.get("episode", "NEWHOPE") == "NEWHOPE":
        return _LUKE
    return _ARTOO


def friends(friend_ids):
    ret = []
    for fid in friend_ids:
        try:
            ret.append(_HUMAN_DATA[fid])
        except KeyError:
            ret.append(_DROID_DATA[fid])
    return ret


def appears_in(appears_in_ids):
    ret = []
    for aid in appears_in_ids:
        ret.append(_EPISODE[aid])
    return ret


@Resolver("Character.friends", schema=STARWARSTIFLETTE.schema)
async def resolver_character_friends(parent_result, *_, **__):
    await asyncio.sleep(0.020)
    return friends(parent_result["friends"])


@Resolver("Character.appearsIn", schema=STARWARSTIFLETTE.schema)
async def resolver_character_appear_in(parent_result, *_, **__):
    await asyncio.sleep(0.020)
    return appears_in(parent_result["appearsIn"])


@Resolver("Query.human", schema=STARWARSTIFLETTE.schema)
async def resolver_human(_, arguments, __, ___):
    await asyncio.sleep(0.020)
    return _HUMAN_DATA[arguments["id"]]


@Resolver("Query.droid", schema=STARWARSTIFLETTE.schema)
async def resolver_droid(_, arguments, __, ___):
    await asyncio.sleep(0.020)
    return _DROID_DATA[arguments["id"]]


# TODO delete when "implement" for sdl is supported on resolver finding.
@Resolver("Human.appearsIn", schema=STARWARSTIFLETTE.schema)
async def resolver_human_appear_in(parent_result, *_, **__):
    await asyncio.sleep(0.020)
    return appears_in(parent_result["appearsIn"])


# TODO delete when "implement" for sdl is supported on resolver finding.
@Resolver("Droid.appearsIn", schema=STARWARSTIFLETTE.schema)
async def resolver_droid_appear_in(parent_result, *_, **__):
    await asyncio.sleep(0.020)
    return appears_in(parent_result["appearsIn"])


# TODO delete when "implement" for sdl is supported on resolver finding.
@Resolver("Droid.friends", schema=STARWARSTIFLETTE.schema)
async def resolver_droid_friends(parent_result, *_, **__):
    await asyncio.sleep(0.020)
    return friends(parent_result["friends"])


# TODO delete when "implement" for sdl is supported on resolver finding.
@Resolver("Human.friends", schema=STARWARSTIFLETTE.schema)
async def resolver_human_friends(parent_result, *_, **__):
    await asyncio.sleep(0.020)
    return friends(parent_result["friends"])
