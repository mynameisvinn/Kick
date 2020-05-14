# https://stackoverflow.com/questions/9382045/send-a-file-through-sockets-in-python

import socket

def up(port, fname):
    """send file to server.
    """
    # create socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # connect to the server on local computer 
    s.connect(('localhost', port)) 

    # send source to server
    f = open (fname, "rb")
    l = f.read(1024)
    s.send(l) 
        
    # receive results from remote execution
    res = s.recv(1024)
    print(res)
    
    # close the connection 
    if res:
        s.close()
        f.close()
        # return res
    else:
        raise ValueError