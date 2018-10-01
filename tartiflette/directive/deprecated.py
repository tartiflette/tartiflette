from .common import CommonDirective


class Deprecated(CommonDirective):
    @staticmethod
    def on_introspection(directive_args, next_directive, introspected_element):
        introspected_element = next_directive(introspected_element)
        introspected_element.isDeprecated = True
        setattr(
            introspected_element, "deprecationReason", directive_args["reason"]
        )
        return introspected_element
