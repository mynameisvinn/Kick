# https://stackoverflow.com/questions/9382045/send-a-file-through-sockets-in-python

import socket
import numpy as np

def up(port, fname):
    """send file fname to server and receive results.
    """
    # create socket and connect
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', port)) 

    # send source to server
    f = open (fname, "rb")
    l = f.read(1024)
    f.close()
    s.send(l) 
        
    # receive results from remote execution and then unpack
    res = s.recv(1024)
    res_unpacked = np.frombuffer(res)  # https://markhneedham.com/blog/2018/04/07/python-serialize-deserialize-numpy-2d-arrays/
    print(res_unpacked)
    
    # close the connection 
    if res:
        s.close()
        return res_unpacked
    else:
        raise ValueError