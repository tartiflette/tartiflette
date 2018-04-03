from copy import deepcopy
from unittest.mock import Mock

import pytest

from tartiflette.sdl.ast_types.string import String


@pytest.mark.parametrize("given", [
    "Some String",
    "",
])
def test_string_class_new(given):
    var = String(given)

    assert var == String(given)
    assert var.value == given
    assert var.ast_node is None


def test_string_class_repr():
    var = String("TestStr")

    assert var.__repr__() == "'TestStr'"


def test_string_class_deepcopy():
    mock_ast = Mock()
    var = String("TestStr", ast_node=mock_ast)

    var2 = deepcopy(var)
    assert var.__class__ is var2.__class__
    assert var.value == var2.value
    assert var.ast_node == var2.ast_node
