import pytest
from emitter import Emitter


# Testing each method of Emitter


# Testing the on() method


def test_on_1():
    """
    on() allows to register a callback.
    """
    emitter = Emitter()
    emitter.on("test", callable)
    assert emitter.listeners("test").get(callable, False)


def test_on_2():
    """
    on() requires the callback to be a callable.
    """
    emitter = Emitter()
    with pytest.raises(TypeError):
        emitter.on("test", "not callable")


def test_on_3():
    """
    on() allows a third parameter which is the credit.
    """
    emitter = Emitter()
    emitter.on("test", callable, 3)
    assert emitter.listeners("test")[callable] == 3


def test_on_4():
    """
    on() set the credit to -1 by default
    """
    emitter = Emitter()
    emitter.on("test", callable)
    assert emitter.listeners("test")[callable] == -1


def test_on_5():
    """
    Max of calls for a callback can be set using the "credit" argument.
    """
    emitter = Emitter()
    l = []

    emitter.on("test", lambda x: l.append(x), 2)

    emitter.emit("test", 1)
    emitter.emit("test", 2)
    emitter.emit("test", 3)
    emitter.emit("test", 4)

    assert len(l) == 2


def test_on_6():
    """
    When "credit" argument is not used, callbacks can be triggered infinitely.
    """
    emitter = Emitter()
    l = []

    emitter.on("test", lambda x: l.append(x))

    emitter.emit("test", 1)
    emitter.emit("test", 2)
    emitter.emit("test", 3)
    emitter.emit("test", 4)

    assert len(l) == 4


# Testing the once() method


def test_once_1():
    """
    once() only triggers the callable one time max
    """
    emitter = Emitter()
    l = []

    emitter.once("test", lambda x: l.append(x))

    emitter.emit("test", 1)
    emitter.emit("test", 2)
    emitter.emit("test", 3)

    assert len(l) == 1


# Testing the emit() method


def test_emit_1():
    """
    Triggers all the functions attached to the event.
    """
    emitter = Emitter()
    a = []
    b = []
    c = []

    emitter.on("test", lambda x: a.append(x))
    emitter.on("test", lambda x: b.append(x))
    emitter.on("test", lambda x: c.append(x))

    emitter.emit("test", "hello")
    assert a[0] == "hello"
    assert b[0] == "hello"
    assert c[0] == "hello"


def test_emit_2():
    """
    Passing all the event data to the callback.
    """
    emitter = Emitter()
    l = []

    def func(param1, param2, unused=None, param3=None):
        l.append(param1)
        l.append(param2)
        l.append(unused)
        l.append(param3)

    emitter.on("test", func)
    emitter.emit("test", 10, 20, param3="hello")

    assert l[0] == 10
    assert l[1] == 20
    assert l[2] is None
    assert l[3] == "hello"


# Testing the events() method


def test_events_1():
    """
    When no events registered, events() returns an empty list.
    """
    emitter = Emitter()
    assert emitter.events() == []


def test_events_2():
    """
    events() returns the list of all events that have listeners registered.
    Order is not guaranteed.
    """
    emitter = Emitter()
    emitter.on("test1", callable)
    emitter.on("test2", callable)
    emitter.on("test3", callable)

    events = emitter.events()

    assert "test1" in events
    assert "test2" in events
    assert "test3" in events


# Testing the listeners() method


def test_listeners_1():
    """
    When passing an event that doesn't exists, returns an empty object.
    """
    emitter = Emitter()
    assert emitter.listeners("unknown_event") == {}


def test_listeners_2():
    """
    When passing an event, returning all callbacks attached to this event.
    The response is a dict formatted like so:
    {
        callable_1: credit_1,
        callable_2: credit_2,
        ...
    }
    """
    emitter = Emitter()
    emitter.on("test", callable, 10)
    emitter.on("test", list, 42)

    listeners = emitter.listeners("test")

    assert isinstance(listeners, dict)

    assert callable in listeners
    assert list in listeners

    assert listeners[callable] == 10
    assert listeners[list] == 42


# Testing the remove() method


def test_remove_1():
    """
    Removing a whole event.
    """
    emitter = Emitter()
    emitter.on("test", callable)
    emitter.on("test", str)
    emitter.remove("test")

    assert emitter.listeners("test") == {}


def test_remove_2():
    """
    Removing a listener.
    """
    emitter = Emitter()
    emitter.on("test", callable)
    emitter.on("test", str)

    emitter.remove("test", callable)

    listeners = emitter.listeners("test")

    assert callable not in listeners
    assert str in listeners

