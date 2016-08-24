# emitter.py

A neat event emitter for Python 3.

```sh
$ pip install emitter.py

# if several versions of Python installed
$ pip3 install emitter.py
```


## Quick Use

```python
from emitter import Emitter


emitter = Emitter()

emitter.on("event", print)
emitter.emit("event", "data1", "data2")
```


## API Overview

* `emitter.on(event, listener): bool`
* `emitter.once(event, listener): bool` 
* `emitter.emit(event[, *args][, **kwargs]): bool`
* `emitter.off([event][, listener]): bool`
* `emitter.events(): set`
* `emitter.listeners(event): list`


### `emitter.on(event, listener)`

```python
emitter.on("click", listener1)
```


### `emitter.once(event, listener)`

```python
emitter.once("click", listener)
```


### `emitter.emit(event[, *args][, **kwargs])`

```python
# emit event with no data
emitter.emit("click")

# emit event with data
emitter.emit("click", 28, y=72)
```


### `emitter.off([event][, listener])`

```python
# remove all the events
emitter.off()

# remove all "click" listeners
emitter.off("click")

# remove a specific listener
emitter.off("click", listener1)
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


## Special Events

### `Emitter.ERROR`

```python
def handler(err, *args, **kwargs):
    ...

emitter.on(Emitter.ERROR, handler)
```


### `Emitter.ATTACH`

```python
def handler(event, listener):
    ...

emitter.on(Emitter.ATTACH, handler)
```


### `Emitter.DETACH`

```python
def handler(event, listener):
    ...

emitter.on(Emitter.DETACH, handler)
```


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

