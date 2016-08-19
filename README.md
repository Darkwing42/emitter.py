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

* `emitter.on(event, listener[, error_handler])`
* `emitter.once(event, listener[, error_handler])`
* `emitter.on_error(error_handler)`
* `emitter.clear([event][, listener])`
* `emitter.emit(event[, *args][, **kwargs])`
* `emitter.get([event][, listener])`

### `emitter.on(event, listener[, error_handler])`

```python
emitter.on("click", listener)
```

### `emitter.once(event, listener[, error_handler])`

```python
emitter.once("click", listener)
```

### `emitter.on_error(error_handler)`

```python
emitter.on_error(error_handler)
```

See [Error Handling][error-handling].

### `emitter.clear([event][, listener])`

```python
# remove all the events
emitter.clear()

# remove all "click" listeners
emitter.clear("click")

# remove a specific listener
emitter.clear("click", listener1)
```

### `emitter.emit(event[, *args][, **kwargs])`

```python
# emit event with no data
emitter.emit("click")

# emit event with data
emitter.emit("click", {"x": 16, "y": 78})
emitter.emit("click", 28, y=72)
```

### `emitter.get([event][, listener])`

```python
emitter.get()
# => {event1, event2}

emitter.get(event1)
# => [listener1, listener2]

emitter.get(event1, listener1)
# => error_handler
```


## Error Handling

When exceptions occurs, an error handler function can be triggered.

```python
def error_handler(err, *args, **kwargs):
    ...
```

Errors can be handled locally, or globally.

**Local Error Handling**

Error is handled at the listener level.

```python
emitter.on(event, listener, error_handler)
```

If the error handler throws himself an exception, the error is handled globally.

**Global Error Handling**

Errors that are not locally catched are handled at the event emitter level.

```python
emitter.on_error(error_handler)
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

