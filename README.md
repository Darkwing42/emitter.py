# emitter.py

A simple event emitter for Python 3.

```sh
$ pip install emitter.py

# if several versions of Python installed
$ pip3 install emitter.py
```


## Quick Use

```python
from emitter import Emitter


emitter = Emitter()
emitter.on("birthday", print)

emitter.emit("birthday", "Frank", 37)
```


## API Overview

* `emitter.on(event, listener[, error_handler])`
* `emitter.once(event, listener[, error_handler])` 
* `emitter.emit(event[, *args][, **kwargs])`
* `emitter.clear([event][, listener][, error_handler])`
* `emitter.get([event][, listener])`
* `emitter.events()`
* `emitter.listeners(event)`
* `emitter.on_error([error_handler])` 


### `emitter.on(event, listener[, error_handler])`

```python
emitter.on("click", listener1)
```

See [Error Handling][error-handling].


### `emitter.once(event, listener[, error_handler])`

```python
emitter.once("click", listener)
```

See [Error Handling][error-handling].


### `emitter.emit(event[, *args][, **kwargs])`

```python
# emit event with no data
emitter.emit("click")

# emit event with data
emitter.emit("click", {"x": 16, "y": 78})
emitter.emit("click", 28, y=72)
```


### `emitter.clear([event][, listener][, error_handler])`

```python
# remove all the events
emitter.clear()

# remove all "click" listeners
emitter.clear("click")

# remove a specific listener
emitter.clear("click", listener1)

# remove the error handler
emitter.clear("click", listener1, error_handler)
```


### `emitter.get([event][, listener])`

```python
emitter.get()  # get all the events
# => {event1, event2}

emitter.get("click")  # get all "click" listeners
# => [listener1, listener2]

emitter.clear("click", listener1)  # get the error handler
# => error_handler
```


### `emitter.events()`

Equivalent of `emitter.get()`.

```python
emitter.events()
# => {event1, event2}
```


### `emitter.listeners(event)`

Equivalent of `emitter.get(event)`.

```python
emitter.listeners(event1)
# => [listener1, listener2]
```


### `emitter.on_error([error_handler])`

```python
emitter.on_error()  # get error handler
# => error_handler

emitter.on_error(error_handler)  # set a new error handler
```

See [Error Handling][error-handling].


## Error Handling

Errors raised by listeners can be intercepted through error handlers.

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
emitter.on(event, listener1)  # no error handler

emitter.on_error(error_handler)  # global error handler
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

