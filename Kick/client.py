import socket
import numpy as np

def up(port, fname):
    """send fname to server and retrieve corresponding results.
    
    # https://stackoverflow.com/questions/9382045/send-a-file-through-sockets-in-python
    """
    # create socket and connect
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', port)) 

    # send source to server
    with open(fname, "rb") as f:
        l = f.read(1024)
    s.send(l) 
        
    # receive results from server and unpack bytes to numpy
    res = s.recv(1024)
    res_unpacked = np.frombuffer(res)  # https://markhneedham.com/blog/2018/04/07/python-serialize-deserialize-numpy-2d-arrays/
    
    # close the connection 
    if res:
        s.close()
        return res_unpacked
    else:
        raise ValueError