import pytest
from emitter import Emitter


def test_error__1():
    """
    ERROR event is emitted when listener raises exception.
    """
    emitter = Emitter()
    l = []

    def listener(*args, **kwargs):
        raise Exception()

    emitter.on("thing", listener)
    emitter.on(Emitter.ERROR, lambda err: l.append(1))

    emitter.emit("thing")
    assert len(l) == 1


def test_error__2():
    """
    ERROR event handler gets error, *args and **kwargs.
    """
    emitter = Emitter()
    d = {}

    def listener(*args, **kwargs):
        raise Exception()

    def handler(err, *args, **kwargs):
        d["err"] = err
        d["args"] = args
        d["kwargs"] = kwargs

    emitter.on("thing", listener)
    emitter.on(Emitter.ERROR, handler)

    emitter.emit("thing", 10, b=20)

    assert isinstance(d["err"], Exception)
    assert d["args"][0] == 10
    assert d["kwargs"]["b"] == 20


def test_error__3():
    """
    If ERROR event handler raises exception, it is re-raised, and Emitter
    does not emit the ERROR event.
    """
    emitter = Emitter()
    l = []

    def listener(*args, **kwargs):
        raise Exception()

    def handler(err, *args, **kwargs):
        l.append(1)
        raise StopIteration()

    emitter.on(Emitter.ERROR, handler)
    emitter.on("event", listener)

    with pytest.raises(StopIteration):
        emitter.emit("event")

    assert len(l) == 1


def test_error__4():
    """
    One time ERROR listener is removed even if it raises exception.
    """
    emitter = Emitter()
    l = []

    def listener(*args, **kwargs):
        raise Exception()

    def handler(err, *args, **kwargs):
        l.append(1)
        raise StopIteration()

    emitter.once(Emitter.ERROR, handler)
    emitter.on("event", listener)

    assert len(emitter.listeners(Emitter.ERROR)) == 1

    with pytest.raises(StopIteration):
        emitter.emit("event")

    assert len(emitter.listeners(Emitter.ERROR)) == 0


