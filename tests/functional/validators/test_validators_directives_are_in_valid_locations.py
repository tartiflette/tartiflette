import pytest

from tartiflette import create_engine


@pytest.fixture(scope="module", name="ttftt_engine")
async def ttftt_engine_fixture():
    SDL = """
directive @queryDirective on QUERY
directive @subscriptionDirective on SUBSCRIPTION
directive @mutationDirective on MUTATION
directive @fieldDirective on FIELD
directive @fragmentDirective on FRAGMENT_DEFINITION
directive @fragmentSpreadDirective on FRAGMENT_SPREAD
directive @inlineFragmentDirective on INLINE_FRAGMENT

type Query {
    bob: Int
}

type Mutation {
    lol: Int
}

type Subscription {
    mdr: Int
}
"""
    return await create_engine(
        SDL, schema_name="test_validators_directives_are_in_valid_locations"
    )


@pytest.mark.parametrize(
    "query,expected",
    [
        (
            """
            query a @queryDirective {
                bob
            }

            mutation b @queryDirective {
                lol
            }

            subscription c @queryDirective {
                mdr
            }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Directive < @queryDirective > is not used in a valid location.",
                        "path": None,
                        "locations": [
                            {"line": 6, "column": 13},
                            {"line": 6, "column": 24},
                        ],
                        "extensions": {
                            "rule": "5.7.2",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Directives-Are-In-Valid-Locations",
                            "tag": "directives-are-in-valid-locations",
                        },
                    },
                    {
                        "message": "Directive < @queryDirective > is not used in a valid location.",
                        "path": None,
                        "locations": [
                            {"line": 10, "column": 13},
                            {"line": 10, "column": 28},
                        ],
                        "extensions": {
                            "rule": "5.7.2",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Directives-Are-In-Valid-Locations",
                            "tag": "directives-are-in-valid-locations",
                        },
                    },
                ],
            },
        ),
        (
            """
            query a @mutationDirective  {
                bob
            }

            mutation b @mutationDirective  {
                lol
            }

            subscription c @mutationDirective {
                mdr
            }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Directive < @mutationDirective > is not used in a valid location.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 13},
                            {"line": 2, "column": 21},
                        ],
                        "extensions": {
                            "rule": "5.7.2",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Directives-Are-In-Valid-Locations",
                            "tag": "directives-are-in-valid-locations",
                        },
                    },
                    {
                        "message": "Directive < @mutationDirective > is not used in a valid location.",
                        "path": None,
                        "locations": [
                            {"line": 10, "column": 13},
                            {"line": 10, "column": 28},
                        ],
                        "extensions": {
                            "rule": "5.7.2",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Directives-Are-In-Valid-Locations",
                            "tag": "directives-are-in-valid-locations",
                        },
                    },
                ],
            },
        ),
        (
            """
            query a @subscriptionDirective {
                bob
            }

            mutation b @subscriptionDirective {
                lol
            }

            subscription c @subscriptionDirective {
                mdr
            }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Directive < @subscriptionDirective > is not used in a valid location.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 13},
                            {"line": 2, "column": 21},
                        ],
                        "extensions": {
                            "rule": "5.7.2",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Directives-Are-In-Valid-Locations",
                            "tag": "directives-are-in-valid-locations",
                        },
                    },
                    {
                        "message": "Directive < @subscriptionDirective > is not used in a valid location.",
                        "path": None,
                        "locations": [
                            {"line": 6, "column": 13},
                            {"line": 6, "column": 24},
                        ],
                        "extensions": {
                            "rule": "5.7.2",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Directives-Are-In-Valid-Locations",
                            "tag": "directives-are-in-valid-locations",
                        },
                    },
                ],
            },
        ),
        (
            """
            query a {
                bob @fieldDirective
            }

            mutation b {
                lol @fragmentSpreadDirective
            }

            subscription c {
                mdr @inlineFragmentDirective
            }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Directive < @fragmentSpreadDirective > is not used in a valid location.",
                        "path": ["lol"],
                        "locations": [
                            {"line": 7, "column": 17},
                            {"line": 7, "column": 21},
                        ],
                        "extensions": {
                            "rule": "5.7.2",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Directives-Are-In-Valid-Locations",
                            "tag": "directives-are-in-valid-locations",
                        },
                    },
                    {
                        "message": "Directive < @inlineFragmentDirective > is not used in a valid location.",
                        "path": ["mdr"],
                        "locations": [
                            {"line": 11, "column": 17},
                            {"line": 11, "column": 21},
                        ],
                        "extensions": {
                            "rule": "5.7.2",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Directives-Are-In-Valid-Locations",
                            "tag": "directives-are-in-valid-locations",
                        },
                    },
                ],
            },
        ),
        (
            """
            fragment John on Query @fragmentDirective @fieldDirective {
                bob
            }

            query a {
                ...John @fragmentSpreadDirective @inlineFragmentDirective
            }

            mutation b {
                ... on Mutation @inlineFragmentDirective @fragmentSpreadDirective {
                    lol
                }
            }

            subscription c {
                mdr
            }
            """,
            {
                "data": None,
                "errors": [
                    {
                        "message": "Directive < @fieldDirective > is not used in a valid location.",
                        "path": None,
                        "locations": [
                            {"line": 2, "column": 13},
                            {"line": 2, "column": 55},
                        ],
                        "extensions": {
                            "rule": "5.7.2",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Directives-Are-In-Valid-Locations",
                            "tag": "directives-are-in-valid-locations",
                        },
                    },
                    {
                        "message": "Directive < @inlineFragmentDirective > is not used in a valid location.",
                        "path": None,
                        "locations": [
                            {"line": 7, "column": 17},
                            {"line": 7, "column": 50},
                        ],
                        "extensions": {
                            "rule": "5.7.2",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Directives-Are-In-Valid-Locations",
                            "tag": "directives-are-in-valid-locations",
                        },
                    },
                    {
                        "message": "Directive < @fragmentSpreadDirective > is not used in a valid location.",
                        "path": None,
                        "locations": [
                            {"line": 11, "column": 17},
                            {"line": 11, "column": 58},
                        ],
                        "extensions": {
                            "rule": "5.7.2",
                            "spec": "June 2018",
                            "details": "https://graphql.github.io/graphql-spec/June2018/#sec-Directives-Are-In-Valid-Locations",
                            "tag": "directives-are-in-valid-locations",
                        },
                    },
                ],
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_validators_directives_are_in_valid_locations(
    query, expected, ttftt_engine
):
    assert await ttftt_engine.execute(query) == expected
