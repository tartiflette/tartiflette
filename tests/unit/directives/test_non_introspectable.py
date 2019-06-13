from unittest.mock import Mock

import pytest


@pytest.mark.asyncio
async def test_non_introspectable_introspection():
    from tartiflette.directive.builtins.non_introspectable import (
        NonIntrospectable,
    )

    assert (
        await NonIntrospectable().on_introspection(
            Mock(), Mock(), Mock(), Mock(), Mock()
        )
        is None
    )
