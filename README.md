# PieKick
evaluate functions on a remote machine by adding a single decorator.

## example
we have code that executes locally. 
```python
def foobar():
    res = 0
    for i in range(3):
        res += i
    print(res)

foobar()  # foobar() evaluated on local machine and prints 3
```

we can evaluate `foobar()` on a remote machine (eg ec2 instance) by adding a single decorator `@kick`. thats it: no `ssh`, `scp`, or moving bytes back and forth.
```python
from kick import kick

@kick
def foobar():
    res = 0
    for i in range(3):
        res += i
    print(res)

foobar()  # foobar() evaluated remotely and prints 3
```