# emitter.py
A minimalist event emitter for Python 3.

```sh
$ pip3 install emitter.py
```

## Example

```python
from emitter import Emitter

def congratulate(name, age):
    print("Happy", age, "years", name, "!")

emitter = Emitter()
emitter.on("birthday", congratulate)

emitter.emit("birthday", "Frank", 37)
emitter.emit("birthday", "Claire", 51)
```

## Methods overview

* `emitter.on(event, listener[, credit])`
* `emitter.get([event][, listener])`
* `emitter.off([event][, listener])`
* `emitter.emit(event[, *args][, **kwargs])`

### `emitter.on()`

```python
# basic signature
emitter.on("click", listener)

# specify the credit
# max number of times the listener can be triggered
emitter.on("click", listener, 3)
```

### `emitter.get()`

```python
# without params, returns a set containing all the events
emitter.get()
# => {event1, event2}

# returns an list containing all the listeners of the specified event
emitter.get(event1)
# => [listener1, listener2]

# returns the credit of this listener
emitter.get(event1, listener1)
# => 3
```

### `emitter.off()`

```python
# remove all the events
emitter.off()

# remove all the listeners of this event
emitter.off("click")

# remove only one specific listener of the event
emitter.off("click", listener1)
```

### `emitter.emit()`

```python
# basic signature
# no data passed to the listeners
emitter.emit("click")

# data can be passed when event is fired
emitter.emit("click", {"x": 16, "y": 78})
emitter.emit("click", 28, y=72)
```

## Listeners credits

Each listener have a credit. It is the maximal number of times the listener can be called.

```python
# listener will be called 3 times max on "click" events
emitter.on("click", listener, 3)

emitter.emit("click") # listener fired
emitter.emit("click") # listener fired
emitter.emit("click") # listener fired, then removed

emitter.emit("click") # nothing happens
```

By default, the credit is `-1` (negative values mean infinity).

When a listener have no more credits, it is removed automatically.

### Update listener's credit

The credit of a listener can be updated using the `on()` method.

If the listener already exists, its credit is updated.

```python
# our cat can only die once
cat.on("fall", die, 1)

# wait... a cat has 9 lives!
# we update the credit of the die listener
cat.on("fall", die, 9)

cat.emit("fall") # still 8 lives
cat.emit("fall") # still 7 lives

# if our cat can now die infinitely
cat.on("fall", die)
```

### Get listener's credit

```python
cat.on("fall", die, 9)

cat.get("fall", die) == 9
```


## Order of insertion

The listeners are called in the order in which they were registered.

```python
emitter.on("click", listener1)
emitter.on("click", listener2)
emitter.on("click", listener3)

# on a "click" event, these 3 listeners are called
# listener1 is called first
# listener2 is called secondly
# ...
```

> What if listener already registered?

Trying to insert a listener that is already existing only updates its credit.
Its original position is kept.

In this example, the `listener2` credit is updated from -1 (infinity) to 12.
The listener will still be called secondly.

```python
emitter.on("click", listener1)
emitter.on("click", listener2)
emitter.on("click", listener3)
emitter.on("click", listener2, 12)

emitter.emit("click") # call listener1, listener2, listener3
```

## Error handling

When a listener throws an error, the `"error"` event is emitted.
The exception is passed to the listeners of the `"error"` event.

Even if a listener throws an error, a credit is counted.

```python
def listener(*args, **kwargs):
    raise Exception("This is an error")

emitter.on("click", listener, 10)
emitter.on("error", print)

emitter.emit("click") # display error

# our listener thrown an exception, but one credit is counted anyway
emitter.get("click", listener) == 9
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
