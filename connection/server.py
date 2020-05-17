"""
spin up server for remote execution. 

server application should be run on ec2 instance with $ python server.py

https://www.geeksforgeeks.org/socket-programming-python/
"""

import socket
import numpy as np
import sys
import subprocess
import jsonpickle

def execute(fname):
    """evaluate python source and return res to client.

    evaluate python source and place its runtime environment into namespace, a dict. then, extract res
    from environment and return it to client.
    """
    
    # https://github.com/mynameisvinn/piegrad/blob/master/PieGrad.py
    # https://stackoverflow.com/questions/16877323/getting-return-information-from-another-python-script
    # https://stackoverflow.com/questions/6357361/alternative-to-execfile-in-python-3
    namespace={}
    with open(fname, "rb") as source_file:
        code = compile(source_file.read(), fname, "exec")
    exec(code, namespace)  # put results in namespace env 
    
    # send numpy results as bytes https://markhneedham.com/blog/2018/04/07/python-serialize-deserialize-numpy-2d-arrays/
    res = namespace['res']
    return res
    

def receive_file(c, out_fname):
    """receive file from client and save as out_fname.
    
    https://stackoverflow.com/questions/9382045/send-a-file-through-sockets-in-python
    """
    # data = c.recv(1024).decode('utf-8')

    l = c.recv(1024)
    print("reading", l)
    with open(out_fname,'wb') as f:
        f.write(l)
    return True


def to_bytes(o):
    """convert arbitrary python object to bytes.
    """
    j = jsonpickle.encode(o)  # python object to json, which is a str  # https://www.journaldev.com/23500/python-string-to-bytes-to-string    
    b = bytes(j, encoding='utf-8')  # json to bytes# https://www.journaldev.com/23500/python-string-to-bytes-to-string
    return b


def from_bytes(b):
    """convert bytes back to python object.
    """
    j = b.decode()  # from bytes to json
    o = jsonpickle.decode(j)  # from json to python object
    return o

if __name__ == '__main__':
    print(">> server up")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    endpoint = ('', 4002)  # https://stackoverflow.com/questions/8033552/python-socket-bind-to-any-ip
    s.bind(endpoint)
    s.listen(5)
    while True:

        # step 1: connect with incoming clinet
        c, addr = s.accept()      
        print('connected to', addr )

        # step 2: receive source file from client and save it
        temp_fname = "barfoo.py"
        _ = receive_file(c, temp_fname)

        # step3 3: evaluates source and return result
        res = execute(temp_fname)

        # step 4: convert results to bytes so it can be sent over socket
        b = to_bytes(res)
        print(from_bytes(b))

        # step 5: send bytes to client
        c.send(b)

        # close connection 
        c.close() 