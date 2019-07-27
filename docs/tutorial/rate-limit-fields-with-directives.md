---
id: rate-limit-fields-with-directives
title: Rate limit your fields with directives
sidebar_label: 12. Rate limit your fields with directives
---

Based [on what we discovered in the previous step](./extend-with-directives.md), we will extend the capabilities of our GraphQL API with the help of directives.

In our fabulous **Tartiflette recipes manager**, we want to limit the use of the recipe update by adding a rate limit behavior.

This rate limiting will be added by extending our SDL by creating a new directive called `rateLimiting`. It will allow us to apply a rate limiting on whichever field we want.

## Write code

### `recipes_manager/sdl/Mutation.graphql`

Here is the new SDL for the mutation:
```graphql
directive @rateLimiting(
  name: String!
  maxAttempts: Int! = 5
  duration: Int! = 60
) on FIELD_DEFINITION

input RecipeInput {
  id: Int!
  name: String
  cookingTime: Int
}

type Mutation {
  updateRecipe(input: RecipeInput!): Recipe! @rateLimiting(name: "update_recipe")
}
```

### `recipes_manager/directives/rate_limiting.py`

This file will contain our implementation of the `@rateLimiting` directive described previously.

> Note: This is a pretty simple implementation of rate limiting, built for our tutorial purpose, you should not use this dumb implementation in production.

```python
import time

from typing import Any, Callable, Dict, Optional

from tartiflette import Directive

_RATE_LIMIT_RULES = {}


def rate_limit_new_rule(name, max_attempts, duration):
    _RATE_LIMIT_RULES[name] = {
        "max_attempts": max_attempts,
        "duration": duration,
        "start_time": int(time.time()),
        "nb_attempts": 1,
    }


def rate_limit_check_and_bump(name, max_attempts, duration):
    rule = _RATE_LIMIT_RULES[name]

    if int(time.time()) > (rule["start_time"] + rule["duration"]):
        rate_limit_new_rule(name, max_attempts, duration)
        return True

    _RATE_LIMIT_RULES[name]["nb_attempts"] += 1

    return rule["nb_attempts"] <= rule["max_attempts"]


@Directive("rateLimiting")
class RateLimiting:
    async def on_field_execution(
        self,
        directive_args: Dict[str, Any],
        next_resolver: Callable,
        parent: Optional[Any],
        args: Dict[str, Any],
        ctx: Optional[Any],
        info: "ResolveInfo",
    ) -> Any:
        if directive_args["name"] not in _RATE_LIMIT_RULES:
            rate_limit_new_rule(
                directive_args["name"],
                directive_args["maxAttempts"],
                directive_args["duration"],
            )

        is_valid = rate_limit_check_and_bump(
            directive_args["name"],
            directive_args["maxAttempts"],
            directive_args["duration"],
        )
        if not is_valid:
            raise Exception("You reached the limit of the rate limiting")
        return await next_resolver(parent, args, ctx, info)
```

## How can we test it?

To simulate the rate limiting, make sure that your application is running, then execute the GraphQL request below.

```bash
python -m recipes_manager
```

### GraphQL Query

```graphql
mutation {
  updateRecipe(input: {
    id: 1
    name: "The best Tartiflette by Eric Guelpa"
    cookingTime: 12
  }) {
    id
    name
    cookingTime
  }
}
```

Execute the query 6 times and you will notice you have been rate limited. :tada:

![Rate limiting demo](/docs/assets/ratelimiting.gif)
