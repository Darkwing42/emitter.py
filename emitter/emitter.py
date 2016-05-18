class Emitter:
    def __init__(self):
        self._events = {}

    def on(self, event, listener, credit=-1):
        """
        Attach the listener to the event.

        The credit (optional) is the greatest number of times the
        listener will be triggered.
        """

        # sanitize args
        credit = int(credit)
        if not callable(listener):
            raise TypeError("{}: listener is not callable".format(listener))

        # if the event do not exists, we create & init an object that will
        # contains the callbacks, and the credit of each callback
        if event not in self._events:
            self._events[event] = {listener: credit}
            return True

        # if event exists, plug the listener to the event, and set its credit
        self._events[event][listener] = credit
        return True

    def once(self, event, listener):
        """ Attach the listener to the event. """

        return self.on(event, listener, 1)

    def emit(self, event, *args, **kwargs):
        """ Trigger the listeners attached to the event """

        # if user emits an event that doesn't exist, return
        if self._events.get(event) is None:
            return False

        # trigger each callback related to the event
        for callback in self._events[event]:
            # if the callback have not enough credit, jump to next iteration
            if self._events[event][callback] == 0:
                continue

            # trigger the current callback
            callback(*args, **kwargs)

            # remove one credit
            self._events[event][callback] -= 1

        return True

    def listeners(self, event):
        """ Return the listeners of the event. """

        return self._events.get(event, {})

    def events(self):
        """ Return all the events. """

        return list(self._events.keys())

    def remove(self, event, listener=None):
        """ Remove the specified event, or only one of its listeners """

        # if user tries to remove an non-existent event
        if self._events.get(event) is None:
            return False

        # if listener argument isn't specified, delete the whole event
        if listener is None:
            self._events = {}
            return True

        # if user tries to remove a non-existent listener
        if self._events[event].get(listener) is None:
            return False

        # delete only the specified listener
        del self._events[event][listener]

        return True
