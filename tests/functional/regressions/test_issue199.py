import pytest

from tartiflette import Engine, Resolver


@Resolver("Query.lists", schema_name="test_skip_include")
async def resolve_query_lists(*_):
    return {}


@Resolver("ListContainer.listA", schema_name="test_skip_include")
@Resolver("ListContainer.listB", schema_name="test_skip_include")
@Resolver("ListContainer.listC", schema_name="test_skip_include")
@Resolver("ListContainer.listD", schema_name="test_skip_include")
async def resolve_list_container_list(*_):
    return [str(i) for i in range(2)]


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


_TTFTT_ENGINE = Engine(_SDL, schema_name="test_skip_include")


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
async def test_skip_include(query, expected):
    assert await _TTFTT_ENGINE.execute(query) == expected
