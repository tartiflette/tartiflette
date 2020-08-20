import pytest


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(
    sdl="""
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
    """,
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
                        "message": "Directive < @queryDirective > may not be used on MUTATION.",
                        "path": None,
                        "locations": [{"line": 6, "column": 24}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.7.2",
                            "tag": "directives-are-in-valid-locations",
                            "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-In-Valid-Locations",
                        },
                    },
                    {
                        "message": "Directive < @queryDirective > may not be used on SUBSCRIPTION.",
                        "path": None,
                        "locations": [{"line": 10, "column": 28}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.7.2",
                            "tag": "directives-are-in-valid-locations",
                            "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-In-Valid-Locations",
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
                        "message": "Directive < @mutationDirective > may not be used on QUERY.",
                        "path": None,
                        "locations": [{"line": 2, "column": 21}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.7.2",
                            "tag": "directives-are-in-valid-locations",
                            "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-In-Valid-Locations",
                        },
                    },
                    {
                        "message": "Directive < @mutationDirective > may not be used on SUBSCRIPTION.",
                        "path": None,
                        "locations": [{"line": 10, "column": 28}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.7.2",
                            "tag": "directives-are-in-valid-locations",
                            "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-In-Valid-Locations",
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
                        "message": "Directive < @subscriptionDirective > may not be used on QUERY.",
                        "path": None,
                        "locations": [{"line": 2, "column": 21}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.7.2",
                            "tag": "directives-are-in-valid-locations",
                            "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-In-Valid-Locations",
                        },
                    },
                    {
                        "message": "Directive < @subscriptionDirective > may not be used on MUTATION.",
                        "path": None,
                        "locations": [{"line": 6, "column": 24}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.7.2",
                            "tag": "directives-are-in-valid-locations",
                            "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-In-Valid-Locations",
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
                        "message": "Directive < @fragmentSpreadDirective > may not be used on FIELD.",
                        "path": None,
                        "locations": [{"line": 7, "column": 21}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.7.2",
                            "tag": "directives-are-in-valid-locations",
                            "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-In-Valid-Locations",
                        },
                    },
                    {
                        "message": "Directive < @inlineFragmentDirective > may not be used on FIELD.",
                        "path": None,
                        "locations": [{"line": 11, "column": 21}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.7.2",
                            "tag": "directives-are-in-valid-locations",
                            "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-In-Valid-Locations",
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
                        "message": "Directive < @fieldDirective > may not be used on FRAGMENT_DEFINITION.",
                        "path": None,
                        "locations": [{"line": 2, "column": 55}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.7.2",
                            "tag": "directives-are-in-valid-locations",
                            "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-In-Valid-Locations",
                        },
                    },
                    {
                        "message": "Directive < @inlineFragmentDirective > may not be used on FRAGMENT_SPREAD.",
                        "path": None,
                        "locations": [{"line": 7, "column": 50}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.7.2",
                            "tag": "directives-are-in-valid-locations",
                            "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-In-Valid-Locations",
                        },
                    },
                    {
                        "message": "Directive < @fragmentSpreadDirective > may not be used on INLINE_FRAGMENT.",
                        "path": None,
                        "locations": [{"line": 11, "column": 58}],
                        "extensions": {
                            "spec": "June 2018",
                            "rule": "5.7.2",
                            "tag": "directives-are-in-valid-locations",
                            "details": "https://spec.graphql.org/June2018/#sec-Directives-Are-In-Valid-Locations",
                        },
                    },
                ],
            },
        ),
    ],
)
async def test_validators_directives_are_in_valid_locations(
    schema_stack, query, expected
):
    assert await schema_stack.execute(query) == expected
