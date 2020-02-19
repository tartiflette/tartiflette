from typing import Dict, List, Any


class Validators:
    """
    Prove a single point of entry for rule validation.

    Calling validate('rule-name') on this will try to validate the rule with the current context.

    The errors field will contain every errors found, so they can all be returned at once.
    BUT if a rule set the internal abort flag at "true", then no other rules are executed.
    Some rules do so, because if invalid, other errors are meaning less.

    """

    __slots__ = ("ctx", "schema", "errors", "rules", "_abort")

    def __init__(
        self, schema: "GraphqlSchema", rules: Dict[str, "ValidationRule"]
    ):
        self.ctx: Dict[str, Any] = {}
        self.schema: "GraphqlSchema" = schema
        self.errors: List["TartifletteError"] = []
        self.rules: Dict[str, "ValidationRule"] = rules
        self._abort = False

    def validate(self, rule: str, path: "Path", **kwargs) -> None:
        """
        Will execute the rule referenced by `rule`. It'll look in the ruleset
        and calls validate giving it **kwargs and **self.ctx so the validator
        has all the needed data to work.

        Will fill self.errors with errors if any.

        :param rule: The rule name to validate
        :type rule: str
        :param kwargs: Any parameters
        :param path: The current Query Path were the validation is taking place.
        :type: path: Path
        """

        if not self._abort:
            rule_errors = self.rules[rule].validate(
                path=path, schema=self.schema, **kwargs, **self.ctx
            )

            if self.rules[rule].abort and rule_errors:
                self._abort = True

            self.errors.extend(rule_errors)
