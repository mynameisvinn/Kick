# PieKick
evaluate python functions on the cloud by adding a single decorator. over time, the goal is to seamlessly link local source code with remote execution.

## example
we have the following code:
```python
def foobar():
    for i in range(5):
        print(i)
    print(os.getpid())
```

we can add `@kick` decorator, which will automatically target execution on a remote host.
```python
@kick
def foobar():
    for i in range(5):
        print(i)
    print(os.getpid())
```