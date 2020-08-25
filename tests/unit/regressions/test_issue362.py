import pytest


@pytest.mark.asyncio
async def test_create_engine_no_loader():
    import json

    from tartiflette import create_engine

    e = await create_engine(
        sdl="""type A{ B:String } type Query { a:A }""",
        schema_name="test_issue362_test_create_engine_no_loader",
    )

    assert e._schema.json_loader == json.loads


@pytest.mark.asyncio
async def test_create_engine_loader():
    def my_loader(*_args, **__kwargs):
        pass

    from tartiflette import create_engine

    e = await create_engine(
        sdl="""type A{ B:String } type Query { a:A }""",
        schema_name="test_issue362_test_create_engine_loader",
        json_loader=my_loader,
    )

    assert e._schema.json_loader == my_loader


@pytest.mark.asyncio
async def test_engine_init_no_loader():
    import json

    from tartiflette import Engine

    e = Engine(
        sdl="""type A{ B:String } type Query { a:A }""",
        schema_name="test_issue362_test_engine_init_no_loader",
    )
    await e.cook()

    assert e._schema.json_loader == json.loads


@pytest.mark.asyncio
async def test_engine_init_loader():
    def my_loader(*_args, **__kwargs):
        pass

    from tartiflette import Engine

    e = Engine(
        sdl="""type A{ B:String } type Query { a:A }""",
        schema_name="test_issue362_test_engine_init_loader",
        json_loader=my_loader,
    )
    await e.cook()

    assert e._schema.json_loader == my_loader


@pytest.mark.asyncio
async def test_engine_cook_loader():
    def my_loader(*_args, **__kwargs):
        pass

    from tartiflette import Engine

    e = Engine(
        sdl="""type A{ B:String } type Query { a:A }""",
        schema_name="test_issue362_test_engine_cook_loader",
    )

    await e.cook(json_loader=my_loader)

    assert e._schema.json_loader == my_loader


@pytest.mark.asyncio
async def test_engine__init__cook_loader():
    def my_loader(*_args, **__kwargs):
        pass

    def my_loader2(*_args, **__kwargs):
        pass

    from tartiflette import Engine

    e = Engine(
        sdl="""type A{ B:String } type Query { a:A }""",
        schema_name="test_issue362_test_engine__init__cook_loader",
        json_loader=my_loader,
    )

    await e.cook(json_loader=my_loader2)

    assert e._schema.json_loader == my_loader2
