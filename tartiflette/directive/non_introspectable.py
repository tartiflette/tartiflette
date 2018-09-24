from .common import CommonDirective


class NonIntrospectable(CommonDirective):
    @staticmethod
    def on_introspection(
        _directive_args, _next_directive, _introspected_element
    ):
        return None
