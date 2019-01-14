import pytest
from unittest.mock import Mock


def test_tartiflette_request_parser_except(clean_registry, monkeypatch):
    from tartiflette.parser.parser import TartifletteRequestParser

    trp = TartifletteRequestParser()

    with pytest.raises(Exception):
        trp.parse_and_tartify(None, "query aq { }} ", variables={})

    monkeypatch.undo()


def test_tartiflette_request_parser(clean_registry, monkeypatch):
    from tartiflette.parser.visitor import TartifletteVisitor

    def myUpdate(*args, **kwargs):
        pass

    monkeypatch.setattr(TartifletteVisitor, "update", myUpdate)

    from tartiflette.parser.parser import TartifletteRequestParser

    trp = TartifletteRequestParser()

    assert trp.parse_and_tartify(None, "query aq { __schema }") == ([], None)

    monkeypatch.undo()


def test_tartiflette_request_parser_vistor_except(clean_registry, monkeypatch):
    from tartiflette.parser.visitor import TartifletteVisitor

    def myUpdate(self, *args, **kwargs):
        self.exception = Exception("Ninja")

    monkeypatch.setattr(TartifletteVisitor, "update", myUpdate)

    from tartiflette.parser.parser import TartifletteRequestParser

    trp = TartifletteRequestParser()

    assert trp.parse_and_tartify(None, "query aq { __schema }") == ([], None)

    monkeypatch.undo()
