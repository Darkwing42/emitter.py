

__version__ = "6.0.0"


class Emitter:
    def __init__(self):
        pass

    def on(self, event, listener, error_handler=None):
        pass

    def once(self, event, listener, error_handler=None):
        pass

    def emit(self, event, *args, **kwargs):
        pass

    def clear(self, event=None, listener=None, error_handler=None):
        pass

    def get(self, event=None, listener=None):
        pass

    def events(self):
        pass

    def listeners(self, event):
        pass

    def on_error(self, error_handler):
        pass
