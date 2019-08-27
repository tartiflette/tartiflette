from typing import Optional


class ValidationRule:
    """
    Base class for a Validation Rule.
    """

    RULE_NAME: Optional[str] = None
    RULE_LINK: Optional[str] = None
    RULE_RELEASE: Optional[str] = None
    RULE_NUMBER: Optional[str] = None

    def __init__(self, abort: bool = False):
        """
        Create a Validation Rule object.

        :param abort: Tells the validation algorithm that nothing else should be executed if the validate method return errors.
        :type abort: bool
        """
        self._extensions = {
            "rule": self.RULE_NUMBER,
            "spec": self.RULE_RELEASE,
            "details": self.RULE_LINK,
            "tag": self.RULE_NAME,
        }
        self.abort = abort


class June2018ReleaseValidationRule(ValidationRule):
    """
    A marker class for Validation Rule easier classification.
    """

    RULE_RELEASE: str = "June 2018"
