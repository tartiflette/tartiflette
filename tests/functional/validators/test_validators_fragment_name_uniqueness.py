import pytest


@pytest.mark.asyncio
@pytest.mark.with_schema_stack(preset="animals")
async def test_validators_fragment_same_name(schema_stack):
    result = await schema_stack.execute(
        """
        fragment a on Dog {
            name
        }

        fragment a on Cat {
            name
        }


        query {
            dog {
                name
            }
        }
        """
    )
    assert result == {
        "data": None,
        "errors": [
            {
                "message": "There can be only one fragment named < a >.",
                "path": None,
                "locations": [
                    {"line": 2, "column": 18},
                    {"line": 6, "column": 18},
                ],
                "extensions": {
                    "spec": "June 2018",
                    "rule": "5.5.1.1",
                    "tag": "fragment-name-uniqueness",
                    "details": "https://spec.graphql.org/June2018/#sec-Fragment-Name-Uniqueness",
                },
            },
            {
                "message": "Fragment < a > is never used.",
                "path": None,
                "locations": [{"line": 2, "column": 9}],
                "extensions": {
                    "spec": "June 2018",
                    "rule": "5.5.1.4",
                    "tag": "fragment-must-be-used",
                    "details": "https://spec.graphql.org/June2018/#sec-Fragments-Must-Be-Used",
                },
            },
            {
                "message": "Fragment < a > is never used.",
                "path": None,
                "locations": [{"line": 6, "column": 9}],
                "extensions": {
                    "spec": "June 2018",
                    "rule": "5.5.1.4",
                    "tag": "fragment-must-be-used",
                    "details": "https://spec.graphql.org/June2018/#sec-Fragments-Must-Be-Used",
                },
            },
        ],
    }
