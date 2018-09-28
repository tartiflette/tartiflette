# pylint: disable=no-member


class String(str):
    """
    String wraps a simple Python string and encapsulates the ast_node if there
    was one at creation. It allows storing the SDL context for
    debugging purposes (for GraphQL named types and fields).

    The usage is straightforward:

        String("Something")  # for a simple String
        String("Something", ast_node=<lark.Token>)  # for an "AST aware" name.
    """

    def __new__(cls, value, ast_node=None):
        inst = super().__new__(cls, value)
        inst.value = value
        inst.ast_node = ast_node
        return inst

    def __repr__(self):
        return "'" + self.value + "'"

    def __deepcopy__(self, memo):
        return String(self.value, self.ast_node)
