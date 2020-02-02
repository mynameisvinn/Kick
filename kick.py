import sys

modulenames = set(sys.modules) & set(globals())  # https://stackoverflow.com/questions/4858100/how-to-list-imported-modules
allmodules = [sys.modules[name] for name in modulenames]
print(allmodules)

import paramiko
import inspect
import sys

def kick(func):
    hostname = '3.94.21.39'
    username="ubuntu"
    key_filename="test.pem"
    
    def modfied_func():
        
        # fetch source code and write it to file
        print("method name is: ", func.__name__)  # we know the name of the method
        source_code = inspect.getsourcelines(func)[0][1:]
        fname = str(func.__name__) + ".py"
        f = open(fname, "w")  # a for append, w for overwrite
        for line in source_code:
            f.write(line)
        f.close()

        
        # append boilerpate __main__ so we can call from command line
        f = open(fname, "a")  # a for append, w for overwrite
        b = 'if __name__ == "__main__":\n     import os\n     foobar()\n'
        f.write(b)
        f.close()
        
        
        # connect to remote https://blog.ruanbekker.com/blog/2018/04/23/using-paramiko-module-in-python-to-execute-remote-bash-commands/
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username=username, key_filename=key_filename)

        # upload code
        ftp_client=ssh.open_sftp()  # https://medium.com/@keagileageek/paramiko-how-to-ssh-and-file-transfers-with-python-75766179de73
        ftp_client.put(fname, fname)
        ftp_client.close()
        
        # call code
        stdin, stdout, stderr = ssh.exec_command("python3 " + str(fname))

        for line in stdout.read().splitlines():
            print(line)
            
        ssh.exec_command("rm " + str(fname))

        ssh.close()

    return modfied_func