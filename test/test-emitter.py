import pytest
from collections import OrderedDict
from emitter import Emitter


# Emitter()


# emitter.on()


def test_on_1():
    """
    This method can take 2 args - an event and a listener.
    """
    emitter = Emitter()
    emitter.on("event", callable)
    assert callable in emitter.get("event")


def test_on_2():
    """
    This method can take 3 args - an event, a listener and a credit.
    """
    emitter = Emitter()
    emitter.on("event", callable, 3)
    assert emitter.get("event", callable) == 3


def test_on_3():
    """
    The listener arg must be a callable.
    """
    emitter = Emitter()
    with pytest.raises(TypeError):
        emitter.on("event", False)


def test_on_4():
    """
    The default value of the credit arg is -1.
    """
    emitter = Emitter()
    emitter.on("event", callable)
    assert emitter.get("event", callable) == -1


def test_on_5():
    """
    The credit argument can be negative, meaning infinity.
    """
    emitter = Emitter()
    emitter.on("event", callable, -10)
    assert emitter.get("event", callable) == -10


def test_on_6():
    """
    Each listener have its own credit.
    """
    emitter = Emitter()
    emitter.on("event", callable, 10)
    emitter.on("event", str, 20)
    emitter.on("event", int, -10)
    assert emitter.get("event", callable) == 10
    assert emitter.get("event", str) == 20
    assert emitter.get("event", int) == -10


def test_on_7():
    """
    Multiple events can be registered in an emitter.
    """
    emitter = Emitter()
    emitter.on("event1", callable)
    emitter.on("event2", str)
    assert callable in emitter.get("event1")
    assert str in emitter.get("event2")


def test_on_8():
    """
    Each event have its own listeners.
    """
    emitter = Emitter()
    emitter.on("event1", callable)
    emitter.on("event2", str)
    assert str not in emitter.get("event1")
    assert callable not in emitter.get("event2")


def test_on_9():
    """
    Max of calls for a listener can be set using the credit arg.
    """
    emitter = Emitter()
    l = []
    emitter.on("event", lambda: l.append(1), 2)
    emitter.emit("event")
    emitter.emit("event")
    emitter.emit("event")  # nothing happens
    assert len(l) == 2


def test_on_10():
    """
    When credit arg is not specified, listener can be called infinitely.
    """
    emitter = Emitter()
    l = []
    emitter.on("event", lambda: l.append(1))
    emitter.emit("event")
    emitter.emit("event")
    emitter.emit("event")
    assert len(l) == 3


def test_on_11():
    """
    False value can be used as an event.
    """
    emitter = Emitter()
    emitter.on(False, str)
    assert False in emitter.get()


def test_on_12():
    """
    Listener with credit equals to 0 is not inserted.
    """
    emitter = Emitter()
    emitter.on("event", str, 0)
    assert str not in emitter.get("event")


def test_on_13():
    """
    This method does not insert listener if credit arg is equal to 0.
    """
    emitter = Emitter()
    emitter.on("event", callable, 0)
    assert callable not in emitter.get("event")


def test_on_14():
    """
    This method returns False if listener is not registered.
    """
    emitter = Emitter()
    result = emitter.on("event", callable, 0)  # 0 credit, no registration
    assert result is False


def test_on_15():
    """
    This method returns True if listener has been registered.
    """
    emitter = Emitter()
    result = emitter.on("event", callable)
    assert result is True


# emitter.emit()


def test_em_1():
    """
    This method triggers all the listeners for the event.
    """
    emitter = Emitter()
    l = []
    emitter.on("event", lambda: l.append(1))
    emitter.on("event", lambda: l.append(1))
    emitter.on("event", lambda: l.append(1))
    emitter.emit("event")
    assert len(l) == 3


def test_em_2():
    """
    This method triggers listener in order of insertion.
    """
    emitter = Emitter()
    l = []
    emitter.on("event", lambda: l.append(1))
    emitter.on("event", lambda: l.append(2))
    emitter.on("event", lambda: l.append(3))
    emitter.emit("event")
    assert l == [1, 2, 3]


def test_em_3():
    """
    This method only triggers the listeners of the specified event.
    """
    emitter = Emitter()
    l = []
    emitter.on("event1", lambda: l.append(1))
    emitter.on("event2", lambda: l.append(2))
    emitter.emit("event1")
    assert l == [1]


def test_em_4():
    """
    This method returns False if trying to emit a non-existent event.
    """
    emitter = Emitter()
    result = emitter.emit("event")
    assert result is False


def test_em_5():
    """
    This method returns True when the event is emitted.
    """
    emitter = Emitter()
    emitter.on("event", callable)
    result = emitter.emit("event")
    assert result is True


def test_em_6():
    """
    *args and **kwargs args given to emit() are passed to the listeners.
    """
    emitter = Emitter()
    params = []

    def listener(param1, param2, unused=None, param3=None):
        params.append(param1)
        params.append(param2)
        params.append(unused)
        params.append(param3)

    emitter.on("event", listener)
    emitter.emit("event", 10, 20, param3="hello")
    assert params == [10, 20, None, "hello"]


def test_em_7():
    """
    The emitter can emit the False event.
    """
    emitter = Emitter()
    l = []
    emitter.on(False, lambda: l.append(1))
    emitter.emit(False)
    assert 1 in l


def test_em_8():
    """
    Negative credit listeners can be triggered infinitely.
    """
    emitter = Emitter()
    l = []
    emitter.on("event", lambda: l.append(1), -22)
    emitter.emit("event")
    emitter.emit("event")
    emitter.emit("event")
    assert len(l) == 3


def test_em_9():
    """
    'error' event is emitted when listener throws exception.
    """
    emitter = Emitter()

    def listener(*args, **kwargs):
        raise Exception()

    l = []
    emitter.on("thing", listener)
    emitter.on("error", lambda err: l.append(err))
    emitter.emit("thing")
    assert len(l) == 1


def test_em_10():
    """
    Credit is updated even if listener throws exception.
    """
    emitter = Emitter()

    def listener(*args, **kwargs):
        raise Exception()

    emitter.on("event", listener, 5)
    emitter.emit("event")
    assert emitter.get("event", listener) == 4


def test_em_11():
    """
    If error listeners throw exceptions, avoid infinite recursion.
    """
    emitter = Emitter()

    def listener(*args, **kwargs):
        raise Exception()

    emitter.on("event", listener)
    emitter.on("error", listener)

    with pytest.raises(Exception):
        emitter.emit("event")


def test_em_12():
    """
    When a listener have no more credits, delete it.
    """
    emitter = Emitter()
    emitter.on("event", callable, 3)
    emitter.emit("event")
    emitter.emit("event")
    emitter.emit("event")
    assert callable not in emitter.get("event")


def test_em_13():
    """
    No errors should be triggered when a listener have no more credit.
    """
    emitter = Emitter()
    l = []
    emitter.on("event", str, 2)
    emitter.on("error", lambda: l.append(1))
    emitter.emit("event")
    emitter.emit("event")
    emitter.emit("event")
    assert len(l) == 0


# emitter.events()


def test_events_10():
    """ When no events registered, events() returns an empty obj. """
    emitter = Emitter()

    assert emitter.get() == {}


def test_events_20():
    """ events() returns a set containing all events. """
    emitter = Emitter()

    emitter.on("event1", callable)
    emitter.on("event2", callable)
    emitter.on("event3", callable)

    events = emitter.get()

    assert "event1" in events
    assert "event2" in events
    assert "event3" in events


def test_events_30():
    """ Using the False event. """
    emitter = Emitter()

    emitter.on(False, callable)

    assert False in emitter.get()


# Testing the listeners() method


def test_listeners_10():
    """ When passing an event that doesn't exists, returns an empty dict. """
    emitter = Emitter()

    assert emitter.get("unknown") == {}


def test_listeners_20():
    """
    When passing an event, returning all callbacks attached to this event.
    The response is an OrderedDict formatted like so:
    {
        callable_1: credit_1,
        callable_2: credit_2,
        ...
    }
    """
    emitter = Emitter()

    emitter.on("event", callable, 10)
    emitter.on("event", list, 42)

    listeners = emitter.get("event")

    assert isinstance(listeners, OrderedDict)

    assert listeners[callable] == 10
    assert listeners[list] == 42


def test_listeners_30():
    """ Check that the insertion order of the listeners is conserved. """
    emitter = Emitter()

    emitter.on("raccoon", bool)
    emitter.on("raccoon", callable)
    emitter.on("raccoon", dict)

    assert type(emitter.get("raccoon")) is OrderedDict

    listeners = list(emitter.get("raccoon"))

    assert listeners == [bool, callable, dict]


def test_listeners_40():
    """ Listeners insertion order should be conserved even after update. """
    emitter = Emitter()

    emitter.on("raccoon", bool)
    emitter.on("raccoon", callable, 10)
    emitter.on("raccoon", dict)

    # update callable, setting credit from 10 to -1 (infinity)
    emitter.on("raccoon", callable)

    # update bool, setting credit from infinity to 10
    emitter.on("raccoon", bool, 10)

    listeners = list(emitter.get("raccoon"))

    assert listeners == [bool, callable, dict]


def test_listeners_50():
    """ Check that even if no listeners, an OrderedDict is returned. """
    emitter = Emitter()

    assert type(emitter.get("unknown")) is OrderedDict


def test_listeners_60():
    """ Get the listeners for the False event. """
    emitter = Emitter()

    emitter.on(False, callable)

    assert callable in emitter.get(False)


# Testing the remove() method


def test_remove_10():
    """ Remove all the events. """
    emitter = Emitter()

    emitter.on("raccoon", callable)
    emitter.on("fox", callable)

    emitter.off()

    assert emitter.get() == {}


def test_remove_20():
    """ Removing only a specified event. """
    emitter = Emitter()

    emitter.on("event", callable)
    emitter.on("event", str)

    emitter.on("raccoon", callable)
    emitter.on("raccoon", str)

    emitter.off("event")

    assert emitter.get("event") == {}
    assert callable in emitter.get("raccoon")
    assert str in emitter.get("raccoon")


def test_remove_30():
    """ Removing a listener. """
    emitter = Emitter()

    emitter.on("event", callable)
    emitter.on("event", str)

    emitter.off("event", callable)

    listeners = emitter.get("event")

    assert callable not in listeners
    assert str in listeners


def test_remove_40():
    """ Remove the False event. """
    emitter = Emitter()

    emitter.on(False, callable)

    assert False in emitter.get()

    emitter.off(False)

    assert False not in emitter.get()


def test_remove_50():
    """ Remove a listener of the False event. """
    emitter = Emitter()

    emitter.on(False, callable)

    assert callable in emitter.get(False)

    emitter.off(False, callable)

    assert callable not in emitter.get(False)
