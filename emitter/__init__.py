import collections


__version__ = "3.1.0"


class Emitter:
    def __init__(self):
        self._events = {}

    def on(self, event=None, listener=None, credit=-1):
        """
        Attach listeners to events.
        See events and listeners currently registered.
        """

        if event is None:
            # list all the registered events
            return set(self._events.keys())

        if listener is None:
            # return all the listeners of the event
            return self._events.get(event, collections.OrderedDict())

        # sanitize arguments types and values

        credit = int(credit)
        if credit == 0:
            return

        if not callable(listener):
            raise TypeError("{}: listener is not callable".format(listener))

        # if the event doesn't exists yet, initialize it
        if event not in self._events:
            self._events[event] = collections.OrderedDict()

        # plug the listener to the event object and set its credit
        self._events[event][listener] = credit
        return

    def emit(self, event, *args, **kwargs):
        """
        Call the listeners attached to the event.
        """

        # if user tries to emits an event that doesn't exists
        if self._events.get(event) is None:
            return

        # trigger each listener attached to the event
        for listener in self._events[event]:
            # trigger the current listener
            try:
                listener(*args, **kwargs)
            except Exception as err:
                if event == "error":
                    raise RecursionError("error listener throws an error")
                self.emit("error", err)

            # subtract a credit to the listener
            if self._events[event][listener] > 0:
                self._events[event][listener] -= 1

            # if no more credit, remove listener
            if self._events[event][listener] == 0:
                self.off(event, listener)

        return

    def off(self, event=None, listener=None):
        """
        Remove events or listeners.
        """

        # remove all events
        if event is None:
            self._events = {}
            return

        # if user tries to remove an non-existent event
        if self._events.get(event) is None:
            return

        # if listener argument isn't specified, delete the whole event
        if listener is None:
            del self._events[event]
            return

        # if user tries to remove a non-existent listener
        if self._events[event].get(listener) is None:
            return

        # delete only the specified listener
        del self._events[event][listener]

        # if the event have no more listeners registered, delete it
        if len(self._events[event]) == 0:
            del self._events[event]

        return
