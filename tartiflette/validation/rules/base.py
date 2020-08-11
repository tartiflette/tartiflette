from tartiflette.language.visitor.visitor import Visitor

__all__ = ("ASTValidationRule",)


class ASTValidationRule(Visitor):
    """
    Base class for validation rule visitor.
    """

    def __init__(self, context: "ASTValidationContext") -> None:
        """
        :param context: context forwarded to the validation rule
        :type context: ASTValidationContext
        """
        self.context = context
