# emitter.py
A minimalist event emitter for Python 3.

```sh
$ pip install emitter.py
```

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

# returns the registered events
emitter.events()

# returns listeners for an event
emitter.listeners("birthday")

# delete a listener
emitter.remove("birthday", congratulate)
```

## Methods overview

* `emitter.on(event, listener[, credit])`
* `emitter.once(event, listener)`
* `emitter.emit(event[, data...])`
* `emitter.events()`
* `emitter.listeners(event)`
* `emitter.remove([event][, listener])`

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

# equivalent using emitter.on()
emitter.on("click", listener, 1)
```

### `emitter.emit()`

```python
# basic signature
# no data passed to the listeners
emitter.on("click")

# data can be passed when event is fired
emitter.on("click", {"x": 16, "y": 78})
emitter.on("click", 28, y=72)
```

### `emitter.events()`

```python
# returns a set containing all the registered events
emitter.events()
# => {"birthday", "click"}
```

### `emitter.listeners()`

```python
# returns an ordered dict containing listeners for the event
# each listener comes along with its credit
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

## Listeners credits

Each listener have a credit. It is the maximal number of times the listener can be called.

```python
# listener will be called 3 times max on "click" events
emitter.on("click", listener, 3)

emitter.emit("click")
emitter.emit("click")
emitter.emit("click")
emitter.emit("click") # nothing happens
```

By default, the credit is `-1`. Negative values mean infinity.

A shortcut to register a listener called 1 time max is using the `emitter.once()` method.

```python
# equivalent for emitter.on("120", die, 1)
cat.once("120", die)

cat.emit("120")
cat.emit("120") # nothing happens
```

The credit of a listener can be updated using `on()` or `once()`.

If the listener already exists, its credit is updated.

```python
cat.once("fall", die)

# wait, a cat has 9 lives
# we update the credit of the die listener
cat.on("fall", die, 9)

cat.emit("fall") # still 8 lives
cat.emit("fall") # still 7 lives

# if our cat can now die infinitely
cat.on("fall", die)
```

## Order of insertion

The listeners are called in the order in which they were registered.

```python
emitter.on("click", listener1)
emitter.once("click", listener2)
emitter.on("click", listener3)

# on a "click" event, these 3 listeners are called
# listener1 is called first
# listener2 is called secondly
# ...
```

> What if listener already registered?

Trying to insert a listener that is already registered only updates its credit.
Its original position is kept.

In this example, `listener2` will still be called secondly, but its credit is updated from 1 (once) to 12.

```python
emitter.on("click", listener1)
emitter.once("click", listener2)
emitter.on("click", listener3)
emitter.on("click", listener2, 12)

emitter.emit("click")
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


[pytest]: http://pytest.org/
