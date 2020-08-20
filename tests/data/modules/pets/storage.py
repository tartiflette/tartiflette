from typing import Any, Dict

from tartiflette.types.exceptions import TartifletteError


def human_factory(id, name, friends=None):
    return {
        "_typename": "Human",
        "id": id,
        "name": name,
        "friend_ids": friends,
    }


def cat_factory(
    id,
    name,
    birthdate,
    meow_volume,
    nickname=None,
    owner_id=None,
    known_commands=None,
    children=None,
    friends=None,
):
    return {
        "_typename": "Cat",
        "id": id,
        "name": name,
        "nickname": nickname,
        "owner_id": owner_id,
        "birthdate": birthdate,
        "known_commands": known_commands,
        "meow_volume": meow_volume,
        "children_ids": children,
        "friend_ids": friends,
    }


def dog_factory(
    id,
    name,
    birthdate,
    bark_volume,
    nickname=None,
    owner_id=None,
    known_commands=None,
    children=None,
    friends=None,
):
    return {
        "_typename": "Dog",
        "id": id,
        "name": name,
        "nickname": nickname,
        "owner_id": owner_id,
        "birthdate": birthdate,
        "known_commands": known_commands,
        "bark_volume": bark_volume,
        "children_ids": children,
        "friend_ids": friends,
    }


STORAGE = {
    "Human.1": human_factory(1, "Human 1", ["Human.2"]),
    "Human.2": human_factory(2, "Human 2"),
    "Human.3": human_factory(3, "Human 3", ["Pet.1", "Human.2"]),
    "Human.4": human_factory(4, "Human 4"),
    "Human.5": human_factory(5, "Human 5", ["Pet.4"]),
    "Pet.1": dog_factory(1, "Dog 1", None, 3, friends=["Pet.2", "Human.1"]),
    "Pet.2": cat_factory(
        2, "Cat 2", None, 2, friends=["Pet.1", "Pet.3", "Pet.5"]
    ),
    "Pet.3": cat_factory(3, "Cat 3", None, 1),
    "Pet.4": cat_factory(4, "Cat 4", None, 2),
    "Pet.5": dog_factory(5, "Dog 5", None, 4),
    "Pet.6": dog_factory(6, "Dog 6", None, 5),
    "Pet.7": dog_factory(7, "Dog 7", None, 7),
    "Pet.8": cat_factory(8, "Cat 8", None, 1),
    "Pet.9": dog_factory(9, "Dog 9", None, 2),
    "Pet.10": dog_factory(10, "Dog 10", None, 1),
}

PETS = (
    "Pet.1",
    "Pet.2",
    "Pet.3",
    "Pet.4",
    "Pet.5",
    "Pet.6",
    "Pet.7",
    "Pet.8",
    "Pet.9",
    "Pet.10",
)


class ObjectDoesntExists(TartifletteError):
    def __init__(self, *args, kind=None, id=None, **kwargs):
        super().__init__(
            f"Object < {kind}.{id} > doesn't exists.", *args, **kwargs
        )
        self.extensions = {"kind": kind, "id": id}


def find_object(kind: str, id: int) -> Dict[str, Any]:
    key = f"{kind}.{id}"
    if key in STORAGE:
        return STORAGE[key]
    raise ObjectDoesntExists(kind=kind, id=id)
