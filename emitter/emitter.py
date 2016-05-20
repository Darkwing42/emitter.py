from collections import OrderedDict


class Emitter:
    def __init__(self):
        self._events = {}

    def on(self, event, listener, credit=-1):
        """ Attach the listener to the event. """

        # sanitize arguments
        credit = int(credit)
        if not callable(listener):
            raise TypeError("{}: listener is not callable".format(listener))

        # if the event doesn't exists yet, initialize it
        if event not in self._events:
            self._events[event] = OrderedDict()

        # plug the listener to the event object and set its credit
        self._events[event][listener] = credit
        return True

    def once(self, event, listener):
        """ Attach the listener to the event. """

        return self.on(event, listener, 1)

    def emit(self, event, *args, **kwargs):
        """ Trigger the listeners attached to the event. """

        # if user tries to emits an event that doesn't exists
        if self._events.get(event) is None:
            return False

        # trigger each listener attached to the event
        for listener in self._events[event]:
            # if the listener have not more credit, we don't trigger it
            if self._events[event][listener] == 0:
                continue

            # trigger the current listener
            listener(*args, **kwargs)

            # remove one credit to the listener
            self._events[event][listener] -= 1

        return True

    def listeners(self, event):
        """ Return the listeners of the event. """

        return self._events.get(event, OrderedDict())

    def events(self):
        """ Return all the events. """

        return set(self._events.keys())

    def remove(self, event=None, listener=None):
        """ Remove all or one event, or only one precise listener. """

        # remove all events
        if event is None:
            self._events = {}
            return True

        # if user tries to remove an non-existent event
        if self._events.get(event) is None:
            return False

        # if listener argument isn't specified, delete the whole event
        if listener is None:
            del self._events[event]
            return True

        # if user tries to remove a non-existent listener
        if self._events[event].get(listener) is None:
            return False

        # delete only the specified listener
        del self._events[event][listener]

        return True
