

__version__ = "6.0.0"


class Emitter:
    ERROR = object()
    ATTACH = object()
    DETACH = object()

    def __init__(self):
        pass

    def on(self, event, listener):
        pass

    def once(self, event, listener):
        pass

    def emit(self, event, *args, **kwargs):
        pass

    def off(self, event=None, listener=None):
        pass

    def events(self):
        pass

    def listeners(self, event):
        pass
