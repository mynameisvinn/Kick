# PieKick
evaluate functions on a remote machine by adding a single decorator.

## aws
to use piekick, spin up an ec2 instance
```bash
# spin up an ubuntu server
aws ec2 run-instances --image-id ami-07ebfd5b3428b6f4d --count 1 --instance-type t2.micro --key-name test --subnet-id subnet-0c4a486ccce2225a0

# authorize ssh with the security group-id, which you can get from describe instances
aws ec2 authorize-security-group-ingress --group-id sg-06114f84ba28b1f1c --protocol tcp --port 22

# find public ip so you know whwere to ssh
aws ec2 describe-instances --instance-ids i-0c5093e98d4c81f4d
```

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