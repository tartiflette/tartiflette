def test_executor_types_ec_instance():
    from tartiflette.executors.types import ExecutionContext

    ec = ExecutionContext()

    assert not ec.errors
    assert not ec.is_introspection


def test_executor_types_ec_add_error():
    from tartiflette.executors.types import ExecutionContext

    ec = ExecutionContext()
    e = Exception

    ec.add_error(e)

    assert e in ec.errors


def test_executor_types_info_repr():
    from tartiflette.executors.types import Info

    inf = Info(
        query_field="A",
        schema_field="B",
        schema="C",
        path=["D", "E"],
        location="F",
        execution_ctx="G",
    )

    assert (
        inf.__repr__()
        == "Info(query_field='A', schema_field='B', schema='C', path=['D', 'E'], location='F', execution_ctx='G')"
    )

    assert inf.__repr__() == inf.__str__()


def test_executor_types_info_eq():
    from tartiflette.executors.types import Info

    inf1 = Info(
        query_field="A",
        schema_field="B",
        schema="C",
        path=["D", "E"],
        location="F",
        execution_ctx="G",
    )

    inf2 = Info(
        query_field="A",
        schema_field="B",
        schema="C",
        path=["D", "E"],
        location="F",
        execution_ctx="G",
    )

    inf3 = Info(
        query_field="A",
        schema_field="B",
        schema="C",
        path=["D", "E"],
        location="H",
        execution_ctx="G",
    )

    assert inf1 == inf2
    assert inf3 != inf2
