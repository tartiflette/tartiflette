def test_types_helpers_wraps_with_directives():
    from unittest.mock import Mock
    from tartiflette.types.helpers import wraps_with_directives

    cllbs_a = Mock()
    cllbs_a.on_field_execution = Mock()
    cllbs_b = Mock()
    cllbs_b.on_field_execution = Mock()

    directives = [
        {
            "callables": {"on_field_execution": cllbs_a.on_field_execution},
            "args": {"a": "b"},
        },
        {
            "callables": {"on_field_execution": cllbs_b.on_field_execution},
            "args": {"c": "d"},
        },
    ]

    r = wraps_with_directives(directives, "on_field_execution", func="A")
    assert r is not None
    assert r.func is cllbs_a.on_field_execution
    a, b = r.args
    assert a == {"a": "b"}
    assert b.func is cllbs_b.on_field_execution
    a, b = b.args
    assert a == {"c": "d"}
    assert b == "A"

    assert wraps_with_directives([], "on_field_execution", func="A") == "A"
