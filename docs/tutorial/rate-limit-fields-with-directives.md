---
id: rate-limit-fields-with-directives
title: Rate limit your fields with directives
sidebar_label: 12. Rate limit your fields with directives
---

Based [on what we discovered in the previous step](/docs/tutorial/extend-with-directives/), we will extend the capabilities of our GraphQL with the help of directives..

In our fabulous **Recipe Manager GraphQL API**, we want to limit the use of the recipe modification by adding a rate limit behavior.

This rate limiting will be added by extending our SDL by creating a new directive called `rateLimiting`. It will allow us to apply a rate limiting on whichever field we want.

## **recipes_manager/sdl/Mutation.graphql**

Here is the new SDL for the mutation:

```graphql
directive @rateLimiting(
  name: String
  max_attempts: Int = 5
  duration: Int = 60
) on FIELD_DEFINITION

type Mutation {
  updateRecipe(input: RecipeInput!): Recipe @rateLimiting(name: "update_recipe")
}

input RecipeInput {
  id: Int!
  name: String
  cookingTime: Int
}
```

## **recipes_manager/directives/rate_limiting.py**

This file will contain our implementation of the `@rateLimiting` directive, described previously.

This is a pretty simple implementation of rate limiting, built for our tutorial purpose, you should not use this dumb implementation in production.

```python
from typing import Any, Callable, Dict, Optional

import time

from tartiflette.directive import Directive
from tartiflette.directive import CommonDirective

_RATE_LIMIT_RULES = {}


def rate_limit_new_rule(name, max_attempts, duration):
    _RATE_LIMIT_RULES[name] = {
        "max_attempts": max_attempts,
        "duration": duration,
        "start_time": int(time.time()),
        "nb_attempts": 1
    }


def rate_limit_check_and_bump(name, max_attempts, duration):
    rule = _RATE_LIMIT_RULES[name]

    if int(time.time()) > (rule["start_time"] + rule["duration"]):
        rate_limit_new_rule(name, max_attempts, duration)
        return True
    
    _RATE_LIMIT_RULES[name]["nb_attempts"] = rule["nb_attempts"] + 1

    if rule["nb_attempts"] >= rule["max_attempts"]:
        rate_limit_new_rule(name, max_attempts, duration)
        return False
    
    return True


@Directive("rateLimiting")
class RateLimiting(CommonDirective):
    @staticmethod
    async def on_execution(
        _directive_args: Dict[str, Any],
        next_resolver: Callable,
        parent_result: Optional[Any],
        args: Dict[str, Any],
        ctx: Optional[Dict[str, Any]],
        info: "Info",
    ) -> Any:
        if not (_directive_args.get('name') in _RATE_LIMIT_RULES):
            rate_limit_new_rule(
                _directive_args.get('name'),
                _directive_args.get("max_attempts"),
                _directive_args.get("duration")
            )
        else:
            is_valid = rate_limit_check_and_bump(
                _directive_args.get('name'),
                _directive_args.get("max_attempts"),
                _directive_args.get("duration")
            )
            if not is_valid:
                raise Exception("You reached the limit of the rate limiting")

        return await next_resolver(parent_result, args, ctx, info)

```

## How can we test it?

In order to simulate the rate limiting. Be sure that your application is running.

```bash
$ python -m recipes_manager
======== Running on http://0.0.0.0:8080 ========
(Press CTRL+C to quit)

```

### GraphQL Query

```graphql
mutation {
  updateRecipe(input: {
        id: 1, 
        name: "The best Tartiflette by Eric Guelpa", 
        cookingTime: 12
  }) {
    id
    name
    cookingTime
  }
}
```

Execute the query 6 times. :tada:

![Rate limiting demo](/docs/assets/ratelimiting.gif)