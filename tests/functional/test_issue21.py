from collections import namedtuple
from typing import Any, List
from unittest.mock import Mock
import pytest

from tartiflette.executors.types import ExecutionData, CoercedValue
from tartiflette.schema import GraphQLSchema

GQLTypeMock = namedtuple("GQLTypeMock", ["name", "coerce_value"])


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'query, expected, varis', [
        (
            """
            query LOL($xid: Int) {
                A(xid: $xid)
            }
            """,
            '{"data":{"A":{"iam": "A", "args":{"xid":45}}}}',
            {"xid": 45}
        ),
        (
            """
            query LOL {
                A(xid: "RE")
            }
            """,
            '{"data":{"A":{"iam": "A", "args":{"xid":"RE"}}}}',
            {}
        ),
        (
            """
            query LOL($xid: Int = 56) {
                A(xid: $xid)
            }
            """,
            '{"data":{"A":{"iam": "A", "args":{"xid":56}}}}',
            {}
        ),
        (
            """
            query LOL($xid: [Int]) {
                A(xid: $xid)
            }
            """,
            '{"data":{"A":{"iam": "A", "args":{"xid":[1, 6]}}}}',
            {"xid": [1, 6]}
        ),
        (
            """
            query LOL($xid: Int) {
                A(xid: $xid)
            }
            """,
            '{"data":{"A":{"iam": "A", "args":{"xid":null}}}}',
            {}
        ),
    ]
)
async def test_issue21_okayquery(query, expected, varis):
    import json
    from tartiflette.tartiflette import Tartiflette

    class default_resolver(Mock):
        async def __call__(self, ctx, exe):
            super(default_resolver, self).__call__(ctx, exe)
            return {"iam": exe.name, "args": exe.arguments}

    def coerce_value(value: Any, execution_data: ExecutionData) -> (
        Any, List):
        return CoercedValue(value, None)

    field = Mock()
    field.gql_type = GQLTypeMock(name="Test", coerce_value=coerce_value)
    field.name = "test"
    field.resolver = default_resolver()
    GraphQLSchema.wrap_field_resolver(field)

    def get_field_by_name(_):
        return field

    sdm = Mock()
    sdm.query_type = "Query"
    sdm.get_field_by_name = get_field_by_name
    sdm.types = {
        "Query": GQLTypeMock(name="Query", coerce_value=coerce_value),
        "Test": GQLTypeMock(name="Test", coerce_value=coerce_value),
    }

    ttftt = Tartiflette(schema=sdm)
    results = await ttftt.execute(query, context={}, variables=varis)

    assert json.loads(results) == json.loads(expected)


from tartiflette.types.exceptions.tartiflette import UnknownVariableException

@pytest.mark.asyncio
@pytest.mark.parametrize(
    'query, expected, varis', [
        (
            """
            query LOL($xid: Int!) {
                A(xid: $xid)
            }
            """,
            UnknownVariableException,
            {}
        ),
        (
            """
            query LOL($xid: Int) {
                A(xid: $xid)
            }
            """,
            TypeError,
            {"xid": "RE"}
        ),
        (
            """
            query LOL($xid: [Int]) {
                A(xid: $xid)
            }
            """,
            TypeError,
            {"xid": "RE"}
        ),
        (
            """
            query LOL($xid: [Int]) {
                A(xid: $xid)
            }
            """,
            TypeError,
            {"xid": ["RE"]}
        ),
    ]
)
async def test_issue21_exceptquery(query, expected, varis):
    from tartiflette.tartiflette import Tartiflette

    class default_resolver(Mock):
        async def __call__(self, ctx, exe):
            super(default_resolver, self).__call__(ctx, exe)
            return {"iam": exe.name, "args": exe.arguments}

    def coerce_value(value: Any, execution_data: ExecutionData) -> (
        Any, List):
        return CoercedValue(value, None)

    field = Mock()
    field.gql_type = GQLTypeMock(name="Test", coerce_value=coerce_value)
    field.name = "test"
    field.resolver = default_resolver()
    GraphQLSchema.wrap_field_resolver(field)

    def get_field_by_name(_):
        return field

    sdm = Mock()
    sdm.query_type = "Query"
    sdm.get_field_by_name = get_field_by_name
    sdm.types = {
        "Query": GQLTypeMock(name="Query", coerce_value=coerce_value),
    }

    ttftt = Tartiflette(schema=sdm)
    with pytest.raises(expected):
        results = await ttftt.execute(query, context={}, variables=varis)


