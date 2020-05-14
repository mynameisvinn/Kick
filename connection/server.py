"""
spin up server for remote execution. 

https://www.geeksforgeeks.org/socket-programming-python/
"""

import socket
import numpy as np
import sys
import subprocess

def execute(fname):
    """
    # https://www.semicolonworld.com/question/59697/return-value-from-one-python-script-to-another
    s2_out = subprocess.check_output([sys.executable, fname])
    return s2_out
    """
    
    # https://github.com/mynameisvinn/piegrad/blob/master/PieGrad.py
    # https://stackoverflow.com/questions/16877323/getting-return-information-from-another-python-script
    # https://stackoverflow.com/questions/6357361/alternative-to-execfile-in-python-3
    namespace={}  # environment
    with open(fname, "rb") as source_file:
        code = compile(source_file.read(), fname, "exec")
    exec(code, namespace)  # put results in namespace env 
    
    # send numpy results as bytes https://markhneedham.com/blog/2018/04/07/python-serialize-deserialize-numpy-2d-arrays/
    # could picklet
    res = namespace['res']
    res_bytes = res.tobytes()
    return res_bytes
    

def receive_file(c, out_fname):
    """receive file from client and save as out_fname.
    
    https://stackoverflow.com/questions/9382045/send-a-file-through-sockets-in-python
    """
    # data = c.recv(1024).decode('utf-8')

    l = c.recv(1024)
    print("reading", l)
    f = open(out_fname,'wb')
    f.write(l)
    f.close()
    return True



if __name__ == '__main__':

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    endpoint = ("localhost", 4001)
    s.bind(endpoint)
    s.listen(5)
    while True:

        # connect with whoever pinged server
        c, addr = s.accept()      
        print('connected to', addr )

        # receive source file from client
        temp_fname = "barfoo.py"
        _ = receive_file(c, temp_fname)

        # server evaluates source and returns results
        res = execute(temp_fname)  # res is numpy answer in bytes
        print(np.frombuffer(res))

        # return result back to client
        c.send(res)  # res is sent as bytes, so it will have to be converted back to numpy array

        # close connection 
        c.close() 