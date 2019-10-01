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


@Directive("rateLimiting")
class RateLimitingDirective:
    """
    Directive to rate limit the access to some fields.
    """

    def __init__(self) -> None:
        self._rate_limit_rules = {}

    def _set_new_rate_limit_rule(
        self, name: str, max_attempts: int, duration: int, nb_attempts: int = 0
    ) -> None:
        """
        Registers a new rate limit entry.
        :param name: identifier of the rate limit
        :param max_attempts: maximum allowed attempts during the duration
        :param duration: interval before resetting the rate limiting
        :param nb_attempts: number of attempts already made
        :type name: str
        :type max_attempts: int
        :type duration: int
        :type nb_attempts: int
        """
        self._rate_limit_rules[name] = {
            "max_attempts": max_attempts,
            "duration": duration,
            "start_time": int(time.time()),
            "nb_attempts": nb_attempts,
        }

    def _rate_limit_check_and_bump(
        self, name: str, max_attempts: int, duration: int
    ) -> bool:
        """
        Increments the number of attempts and determines whether or not the
        rate limit has been reached.
        :param name: identifier of the rate limit
        :param max_attempts: maximum allowed attempts during the duration
        :param duration: interval before resetting the rate limiting
        :type name: str
        :type max_attempts: int
        :type duration: int
        :return: whether or not the rate limit has been reached
        :rtype: bool
        """
        rule = self._rate_limit_rules[name]

        if int(time.time()) > (rule["start_time"] + rule["duration"]):
            self._set_new_rate_limit_rule(
                name, max_attempts, duration, nb_attempts=1
            )
            return True

        self._rate_limit_rules[name]["nb_attempts"] += 1

        return rule["nb_attempts"] <= rule["max_attempts"]

    async def on_field_execution(
        self,
        directive_args: Dict[str, Any],
        next_resolver: Callable,
        parent: Optional[Any],
        args: Dict[str, Any],
        ctx: Dict[str, Any],
        info: "ResolveInfo",
    ) -> Any:
        """
        Checks that the user did not reach the rate limit before proceeding
        with the execution and resolution of the field.
        :param directive_args: computed arguments related to the directive
        :param next_resolver: next resolver to call
        :param parent: initial value filled in to the engine `execute` or
        `subscribe` method or field parent value
        :param args: computed arguments related to the field
        :param ctx: context filled in at engine initialization
        :param info: information related to the execution and field resolution
        :type directive_args: Dict[str, Any]
        :type next_resolver: Callable
        :type parent: Optional[Any]
        :type args: Dict[str, Any]
        :type ctx: Dict[str, Any]
        :type info: ResolveInfo
        :return: result of the field resolution
        :rtype: Any
        :raises Exception: if the user has reached the rate limit
        """
        if directive_args["name"] not in self._rate_limit_rules:
            self._set_new_rate_limit_rule(
                directive_args["name"],
                directive_args["maxAttempts"],
                directive_args["duration"],
            )

        is_valid = self._rate_limit_check_and_bump(
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
