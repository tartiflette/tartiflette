from unittest.mock import Mock

import pytest

from tartiflette.executors.types import ExecutionContext
from tartiflette.parser.nodes.field import _add_errors_to_execution_context
from tartiflette.types.exceptions.tartiflette import (
    GraphQLError,
    MultipleException,
)
from tartiflette.types.location import Location


def test_parser_node_nodefield():
    from tartiflette.parser.nodes.field import NodeField

    nf = NodeField("Roberto", None, None, None, [], None, None)

    assert nf.name == "Roberto"
    assert nf.alias == "Roberto"

    nf = NodeField("Roberto", None, None, None, [], None, "James")

    assert nf.name == "Roberto"
    assert nf.alias == "James"


@pytest.mark.parametrize("value", [True, False])
def test_parser_node_nodefield_cant_be_null(value):
    from tartiflette.parser.nodes.field import NodeField

    fe = Mock()
    fe.cant_be_null = value

    nf = NodeField("Rb", None, fe, None, None, None, None)

    assert nf.cant_be_null == value


@pytest.mark.parametrize("value", [True, False])
def test_parser_node_nodefield_contains_not_null(value):
    from tartiflette.parser.nodes.field import NodeField

    fe = Mock()
    fe.contains_not_null = value

    nf = NodeField("Rb", None, fe, None, None, None, None)

    assert nf.contains_not_null == value


@pytest.mark.parametrize("value", [True, False])
def test_parser_node_nodefield_shall_produce_list(value):
    from tartiflette.parser.nodes.field import NodeField

    fe = Mock()
    fe.shall_produce_list = value

    nf = NodeField("Rb", None, fe, None, None, None, None)

    assert nf.shall_produce_list == value


def test_parser_node_nodefield_bubble_error():
    from tartiflette.parser.nodes.field import NodeField

    fe = Mock()
    fe.cant_be_null = False

    nf = NodeField("Rb", None, fe, None, None, None, None)

    nf.marshalled = {}
    nf.parent = None

    nf.bubble_error()

    assert nf.marshalled is None

    nf.marshalled = {}
    nf.parent = Mock()
    nf.parent.marshalled = {"Rb": "Lol"}
    nf.parent.bubble_error = Mock()

    nf.bubble_error()

    assert "Rb" in nf.parent.marshalled
    assert nf.parent.marshalled["Rb"] is None

    fe.cant_be_null = True

    nf.bubble_error()

    assert nf.parent.bubble_error.called

    nf.parent = None
    nf.marshalled = {}

    nf.bubble_error()

    assert nf.marshalled is None


def test_parser_node_nodefield__get_coroutz_from_child_no_cond():
    from tartiflette.parser.nodes.field import NodeField

    nf = NodeField("NtM", None, None, None, None, None, None)

    child = Mock()
    child.type_condition = None

    exectx = Mock()
    reqctx = Mock()
    result = Mock()
    coerce = Mock()

    nf.children = [child, child, child]

    crtz = nf._get_coroutz_from_child(exectx, reqctx, result, coerce, None)

    assert len(crtz) == 3
    assert child.call_args_list == [
        (
            (exectx, reqctx),
            {"parent_result": result, "parent_marshalled": coerce},
        ),
        (
            (exectx, reqctx),
            {"parent_result": result, "parent_marshalled": coerce},
        ),
        (
            (exectx, reqctx),
            {"parent_result": result, "parent_marshalled": coerce},
        ),
    ]


def test_parser_node_nodefield__get_coroutz_from_child_cond():
    from tartiflette.parser.nodes.field import NodeField

    nf = NodeField("NtM", None, None, None, None, None, None)

    child = Mock()
    child.type_condition = "LOL"

    exectx = Mock()
    reqctx = Mock()
    result = Mock()
    coerce = Mock()

    nf.children = [child, child, child]

    crtz = nf._get_coroutz_from_child(exectx, reqctx, result, coerce, "LL")

    assert crtz == []

    crtz = nf._get_coroutz_from_child(exectx, reqctx, result, coerce, "LOL")

    assert len(crtz) == 3
    assert child.call_args_list == [
        (
            (exectx, reqctx),
            {"parent_result": result, "parent_marshalled": coerce},
        ),
        (
            (exectx, reqctx),
            {"parent_result": result, "parent_marshalled": coerce},
        ),
        (
            (exectx, reqctx),
            {"parent_result": result, "parent_marshalled": coerce},
        ),
    ]


@pytest.mark.asyncio
async def test_parser_node_nodefield__execute_children_not_a_list():
    from tartiflette.parser.nodes.field import NodeField
    from tests.unit.utils import AsyncMock

    exectx = Mock()
    reqctx = Mock()
    result = Mock()
    coerce = Mock()

    fe = Mock()
    fe.shall_produce_list = False

    child = AsyncMock()
    child.type_condition = None

    nf = NodeField("NtM", None, fe, None, None, None, None)

    nf.children = [child]

    await nf._execute_children(exectx, reqctx, result, coerce)

    assert child.called
    assert child.call_args == (
        (exectx, reqctx),
        {"parent_result": result, "parent_marshalled": coerce},
    )


@pytest.mark.asyncio
async def test_parser_node_nodefield__execute_children_a_list():
    from tartiflette.parser.nodes.field import NodeField
    from tests.unit.utils import AsyncMock

    exectx = Mock()
    reqctx = Mock()
    result = [Mock(), Mock()]
    coerce = [Mock(), Mock()]

    fe = Mock()
    fe.shall_produce_list = True

    child = AsyncMock()
    child.type_condition = None

    nf = NodeField("NtM", None, fe, None, None, None, None)

    nf.children = [child]

    await nf._execute_children(exectx, reqctx, result, coerce)

    assert child.called
    assert (
        (exectx, reqctx),
        {"parent_result": result[0], "parent_marshalled": coerce[0]},
    ) in child.call_args_list
    assert (
        (exectx, reqctx),
        {"parent_result": result[1], "parent_marshalled": coerce[1]},
    ) in child.call_args_list


@pytest.mark.asyncio
async def test_parser_node_nodefield___call__():
    from tartiflette.parser.nodes.field import NodeField

    raw = Mock()
    coerced = Mock()

    class fex:
        async def __call__(self, *_, **__):
            return raw, coerced

    fe = fex()
    fe.schema_field = Mock()

    nf = NodeField("B", None, fe, None, None, None, None)
    nf.children = None

    exectx = Mock()
    reqctx = Mock()

    await nf(exectx, reqctx)

    assert nf.marshalled == coerced


@pytest.mark.asyncio
async def test_parser_node_nodefield___call___with_a_parent():
    from tartiflette.parser.nodes.field import NodeField

    raw = Mock()
    coerced = Mock()

    class fex:
        async def __call__(self, *_, **__):
            return raw, coerced

    fe = fex()
    fe.schema_field = Mock()

    nf = NodeField("B", None, fe, None, None, None, None)
    nf.children = None

    exectx = Mock()
    reqctx = Mock()

    prm = {}

    await nf(exectx, reqctx, parent_marshalled=prm)

    assert nf.marshalled == {}
    assert prm["B"] == coerced


@pytest.mark.asyncio
async def test_parser_node_nodefield___call___with_children():
    from tartiflette.parser.nodes.field import NodeField
    from tests.unit.utils import AsyncMock

    raw = Mock()
    coerced = Mock()

    class fex:
        async def __call__(self, *_, **__):
            return raw, coerced

    fe = fex()
    fe.schema_field = Mock()

    nf = NodeField("B", None, fe, None, None, None, None)
    nf.children = [Mock()]
    nf._execute_children = AsyncMock()

    exectx = Mock()
    reqctx = Mock()

    prm = {}

    await nf(exectx, reqctx, parent_marshalled=prm)

    assert nf.marshalled == {}
    assert prm["B"] == coerced
    assert nf._execute_children.called
    assert nf._execute_children.call_args == (
        (exectx, reqctx),
        {"result": raw, "coerced": coerced},
    )


@pytest.mark.asyncio
async def test_parser_node_nodefield___call___fe_is_excepting():
    from tartiflette.parser.nodes.field import NodeField
    from tests.unit.utils import AsyncMock

    raw = Exception("ninja")
    coerced = None

    class fex:
        async def __call__(self, *_, **__):
            return raw, coerced

    fe = fex()
    fe.schema_field = Mock()
    fe.cant_be_null = True

    nf = NodeField("B", None, fe, None, None, None, None)
    nf.children = [Mock()]
    nf._execute_children = AsyncMock()
    nf.parent = Mock()
    nf.parent.bubble_error = Mock()

    exectx = Mock()
    exectx.add_error = Mock()
    reqctx = Mock()

    prm = {}

    await nf(exectx, reqctx, parent_marshalled=prm)

    assert nf.marshalled == {}
    assert prm["B"] == coerced
    assert nf.parent.bubble_error.called
    assert exectx.add_error.called


@pytest.mark.asyncio
async def test_parser_node_nodefield__call__exception():
    from tartiflette.parser.nodes.field import NodeField
    from tests.unit.utils import AsyncMock

    raw = Exception("ninja")
    coerced = None

    class fex:
        async def __call__(self, *_, **__):
            return raw, coerced

    fe = fex()
    fe.schema_field = Mock()
    fe.cant_be_null = True

    nf = NodeField("B", None, fe, None, None, None, None)
    nf.children = [Mock()]
    nf._execute_children = AsyncMock()
    nf.parent = Mock()
    nf.parent.bubble_error = Mock()

    exectx = ExecutionContext()
    reqctx = Mock()

    prm = {}

    assert not bool(exectx.errors)

    await nf(exectx, reqctx, parent_marshalled=prm)

    assert bool(exectx.errors)

    assert exectx.errors[0] is not raw
    assert isinstance(exectx.errors[0], GraphQLError)
    assert exectx.errors[0].coerce_value() == {
        "message": "ninja",
        "path": None,
        "locations": [],
    }


@pytest.mark.asyncio
async def test_parser_node_nodefield__call__custom_exception():
    from tartiflette.parser.nodes.field import NodeField
    from tests.unit.utils import AsyncMock

    class CustomException(Exception):
        def coerce_value(self, *_args, path=None, locations=None, **_kwargs):
            return {"msg": "error", "type": "bad_request"}

    raw = CustomException("ninja")
    coerced = None

    class fex:
        async def __call__(self, *_, **__):
            return raw, coerced

    fe = fex()
    fe.schema_field = Mock()
    fe.cant_be_null = True

    nf = NodeField("B", None, fe, None, None, None, None)
    nf.children = [Mock()]
    nf._execute_children = AsyncMock()
    nf.parent = Mock()
    nf.parent.bubble_error = Mock()

    exectx = ExecutionContext()
    reqctx = Mock()

    prm = {}

    assert not bool(exectx.errors)

    await nf(exectx, reqctx, parent_marshalled=prm)

    assert bool(exectx.errors)

    assert exectx.errors[0] is raw
    assert exectx.errors[0].coerce_value() == {
        "msg": "error",
        "type": "bad_request",
    }


@pytest.mark.parametrize(
    "raw_exception,expected_messages,expected_original_errors",
    [
        (GraphQLError("AGraphQLError"), ["AGraphQLError"], [type(None)]),
        (TypeError("ATypeError"), ["ATypeError"], [TypeError]),
        (
            MultipleException(
                exceptions=[
                    GraphQLError("AGraphQLError"),
                    TypeError("ATypeError"),
                ]
            ),
            ["AGraphQLError", "ATypeError"],
            [type(None), TypeError],
        ),
    ],
)
def test_add_errors_to_execution_context(
    raw_exception, expected_messages, expected_original_errors
):
    execution_context = ExecutionContext()

    location = Location(line=1, column=1)
    path = ["error", "path"]

    _add_errors_to_execution_context(
        execution_context, raw_exception, path, location
    )

    assert len(execution_context.errors) == len(expected_messages)

    for error, expected_message, expected_original_error in zip(
        execution_context.errors, expected_messages, expected_original_errors
    ):
        assert isinstance(error, GraphQLError)
        assert error.message == expected_message
        assert type(error.original_error) is expected_original_error
