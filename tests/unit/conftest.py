import pytest
from tests.unit.utils import MOCKED_GET_RESOLVER_EXECUTOR


@pytest.fixture()
def fixture_mocked_get_resolver_executor():
    return MOCKED_GET_RESOLVER_EXECUTOR


@pytest.yield_fixture()
def mocked_resolver_factory(monkeypatch, fixture_mocked_get_resolver_executor):
    from tartiflette.resolver.factory import ResolverExecutorFactory

    monkeypatch.setattr(
        ResolverExecutorFactory,
        "get_resolver_executor",
        fixture_mocked_get_resolver_executor,
    )

    yield fixture_mocked_get_resolver_executor

    monkeypatch.undo()
