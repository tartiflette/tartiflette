import pytest

from tartiflette import Resolver, create_engine

_SDL = """
type ListContainer {
  listA: [String]
  listB: [String]
  listC: [String]
  listD: [String]
}

type Query {
  lists: ListContainer
}
"""


@pytest.fixture(scope="module")
async def ttftt_engine():
    @Resolver("Query.lists", schema_name="test_skip_include")
    async def resolve_query_lists(*_):
        return {}

    @Resolver("ListContainer.listA", schema_name="test_skip_include")
    @Resolver("ListContainer.listB", schema_name="test_skip_include")
    @Resolver("ListContainer.listC", schema_name="test_skip_include")
    @Resolver("ListContainer.listD", schema_name="test_skip_include")
    async def resolve_list_container_list(*_):
        return [str(i) for i in range(2)]

    return await create_engine(sdl=_SDL, schema_name="test_skip_include")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query,expected",
    [
        # Skip
        (
            """
            query {
              lists {
                listA
                listB
                listC
                listD
              }
            }
            """,
            {
                "data": {
                    "lists": {
                        "listA": ["0", "1"],
                        "listB": ["0", "1"],
                        "listC": ["0", "1"],
                        "listD": ["0", "1"],
                    }
                }
            },
        ),
        (
            """
            query {
              lists {
                listA
                listB @skip(if: true)
                listC
                listD
              }
            }
            """,
            {
                "data": {
                    "lists": {
                        "listA": ["0", "1"],
                        "listC": ["0", "1"],
                        "listD": ["0", "1"],
                    }
                }
            },
        ),
        (
            """
            query {
              lists {
                listA @skip(if: true)
                listB @skip(if: true)
                listC
                listD
              }
            }
            """,
            {"data": {"lists": {"listC": ["0", "1"], "listD": ["0", "1"]}}},
        ),
        (
            """
            query {
              lists {
                listA
                listB
                listC
                listD @skip(if: true)
              }
            }
            """,
            {
                "data": {
                    "lists": {
                        "listA": ["0", "1"],
                        "listB": ["0", "1"],
                        "listC": ["0", "1"],
                    }
                }
            },
        ),
        (
            """
            query {
              lists {
                listA
                listB
                listC
                listD
              }
            }
            """,
            {
                "data": {
                    "lists": {
                        "listA": ["0", "1"],
                        "listB": ["0", "1"],
                        "listC": ["0", "1"],
                        "listD": ["0", "1"],
                    }
                }
            },
        ),
        (
            """
            query {
              lists {
                listA
                listB
                listC @skip(if: true)
                listD
              }
            }
            """,
            {
                "data": {
                    "lists": {
                        "listA": ["0", "1"],
                        "listB": ["0", "1"],
                        "listD": ["0", "1"],
                    }
                }
            },
        ),
        # Include
        (
            """
            query {
              lists {
                listA
                listB
                listC
                listD
              }
            }
            """,
            {
                "data": {
                    "lists": {
                        "listA": ["0", "1"],
                        "listB": ["0", "1"],
                        "listC": ["0", "1"],
                        "listD": ["0", "1"],
                    }
                }
            },
        ),
        (
            """
            query {
              lists {
                listA
                listB @include(if: false)
                listC
                listD
              }
            }
            """,
            {
                "data": {
                    "lists": {
                        "listA": ["0", "1"],
                        "listC": ["0", "1"],
                        "listD": ["0", "1"],
                    }
                }
            },
        ),
        (
            """
            query {
              lists {
                listA @include(if: false)
                listB @include(if: false)
                listC
                listD
              }
            }
            """,
            {"data": {"lists": {"listC": ["0", "1"], "listD": ["0", "1"]}}},
        ),
        (
            """
            query {
              lists {
                listA
                listB
                listC
                listD @include(if: false)
              }
            }
            """,
            {
                "data": {
                    "lists": {
                        "listA": ["0", "1"],
                        "listB": ["0", "1"],
                        "listC": ["0", "1"],
                    }
                }
            },
        ),
        (
            """
            query {
              lists {
                listA
                listB
                listC
                listD
              }
            }
            """,
            {
                "data": {
                    "lists": {
                        "listA": ["0", "1"],
                        "listB": ["0", "1"],
                        "listC": ["0", "1"],
                        "listD": ["0", "1"],
                    }
                }
            },
        ),
        (
            """
            query {
              lists {
                listA
                listB
                listC @include(if: false)
                listD
              }
            }
            """,
            {
                "data": {
                    "lists": {
                        "listA": ["0", "1"],
                        "listB": ["0", "1"],
                        "listD": ["0", "1"],
                    }
                }
            },
        ),
    ],
)
async def test_skip_include(query, expected, ttftt_engine):
    assert await ttftt_engine.execute(query) == expected
