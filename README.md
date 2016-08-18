# emitter.py

A minimalist event emitter for Python 3.

```sh
$ pip install emitter.py
```


## Quick Use

```python
from emitter import Emitter


emitter = Emitter()
emitter.on("birthday", print)

emitter.emit("birthday", "Frank", 37)
```


## Methods Overview

* `emitter.on(event, listener[, errorHandler])`
* `emitter.once(event, listener[, errorHandler])`
* `emitter.onError(errorHandler)`
* `emitter.off([event][, listener])`
* `emitter.emit(event[, *args][, **kwargs])`
* `emitter.events()`
* `emitter.listeners(event)`

### `emitter.on(event, listener[, errorHandler])`

```python
emitter.on("click", listener)
```

### `emitter.once(event, listener[, errorHandler])`

```python
emitter.once("click", listener)
```

### `emitter.onError(errorHandler)`

```python
emitter.onError(errorHandler)
```

See [Error Handling][error-handling].

### `emitter.off([event][, listener])`

```python
# remove all the events
emitter.off()

# remove all "click" listeners
emitter.off("click")

# remove a specific listener
emitter.off("click", listener1)
```

### `emitter.emit(event[, *args][, **kwargs])`

```python
# emit event with no data
emitter.emit("click")

# emit event with data
emitter.emit("click", {"x": 16, "y": 78})
emitter.emit("click", 28, y=72)
```

### `emitter.events()`

```python
emitter.events()
# => {event1, event2}
```

### `emitter.listeners(event)`

```python
emitter.listeners(event1)
# => [listener1, listener2]
```


## Error Handling

When exceptions occurs, an error handler function can be triggered.

```python
def errorHandler(err, *args, **kwargs):
    ...
```

Errors can be handled locally, or globally.

**Local Error Handling**

Error is handled at the listener level.

```python
emitter.on(event, listener, errorHandler)
```

If the error handler throws himself an exception, the error is handled globally.

**Global Error Handling**

Errors that are not locally catched are handled at the event emitter level.

```python
emitter.onError(errorHandler)
```

If the global error handler throws himself an exception, it is propagated above.


## Tests

[PyTest][pytest] is used for tests. Python 2 is not supported.

**Install PyTest**

```sh
$ pip install pytest
```

**Test**

```sh
$ py.test test/*

# or to be sure to use python3
$ py.test-3 test/*
```


[error-handling]: #error-handling
[pytest]: http://pytest.org/

