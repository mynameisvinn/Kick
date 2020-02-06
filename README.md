# PieKick
evaluate functions on a remote machine by adding a single decorator.

## example
we have the following code that is typically executes on a local notebook. 
```python
import os

def foobar():
    res = 0
    for i in range(3):
        res += i
    print(res)

foobar()  # foobar() evaluated on local machine and prints 3
```

if we want to evaluate `foobar()` on a remote machine, we add a single decorator. thats it: no `ssh`, `scp`, or moving bytes back and forth.
```python
@kick
def foobar():
    res = 0
    for i in range(3):
        res += i
    print(res)

foobar()  # foobar() evaluated remotely and prints 3
```