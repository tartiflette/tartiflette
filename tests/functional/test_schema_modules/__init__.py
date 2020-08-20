from tartiflette import Resolver
from tests.functional.test_schema_modules.resolver import resolver_a_b


def bake(schema_name, config):
    Resolver("A.b", schema_name=schema_name)(resolver_a_b)
