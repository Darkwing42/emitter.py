# emitter.py
A minimalist event emitter for Python 3.

## Example

```python
from emitter import Emitter

# create a listener
def congratulate(name):
    print("Happy birthday {}!".format(name))

# create an emitter
emitter = Emitter()

# register the listener for the "birthday" event
emitter.on("birthday", congratulate)

# emit the "birthday" event along with data
emitter.emit("birthday", "Jim")
emitter.emit("birthday", "Claire")
emitter.emit("birthday", "William")
```

## Methods overview

* `emitter.on()`
* `emitter.once()`
* `emitter.emit()`
* `emitter.events()`
* `emitter.listeners()`
* `emitter.remove()`

### `emitter.on()`

```python
# basic signature
emitter.on("click", listener)

# specify the credit
# max number of times the listener can be triggered
emitter.on("click", listener, 3)
```

### `emitter.once()`

```python
# the listener will be triggered only once
emitter.once("click", listener)
```

### `emitter.emit()`

```python
# basic signature
# no data passed to the listeners
emitter.on("click")

# data can be passed when event is fired
emitter.on("click", {"x": 16, "y": 78})
```

### `emitter.events()`

```python
# get all the registered events
emitter.events()
# => {"birthday", "click"}
```

### `emitter.listeners()`

```python
# get an ordered dict containing all the listeners for an event
# along with the credit of each listener
# the insertion order of the listeners is preserved

emitter.listeners("click")
# =>
#   { listener1: -1,
#     listener2: 12, ... }
```

### `emitter.remove()`

```python
# remove all the events
emitter.remove()

# remove all the listeners of this event
emitter.remove("click")

# remove only one specific listener of the event
emitter.remove("click", listener1)
```

## Tests

[PyTest][pytest] is used for tests. Python2 is not supported.
If PyTest uses Python2, an exception will be raised.

```sh
$ py.test test/*

# or to be sure to use python3
$ py.test-3 test/*
```

## Roadmap

* Write more tests, one file per method
* Test the module, imports from outside, ...
* Release first public version: tag v1.0


[pytest]: http://pytest.org/

