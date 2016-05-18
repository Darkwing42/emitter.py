# emitter.py
A minimalist event emitter for Python.

## Examples

```python

from emitter import Emitter


def congratulate(name):
    print("Happy birthday {}!".format(name))


emitter = Emitter()

emitter.on("birthday", congratulate)

emitter.emit("birthday", "Jim")
emitter.emit("birthday", "Claire")
emitter.emit("birthday", "William")

```

