import paramiko
import inspect
import os

def kick(func):

    # grab context from calling jupyter notebook so we can get its cells
    previous_frame = inspect.currentframe().f_back  # previous frame is the notebook
    callers_objects = inspect.getmembers(previous_frame)  # grab all objects from caller
    env = callers_objects[27][1]  # this slice refers to global env from jupyter notebook
    cells =  env['_ih']  # cells
    # cells = globals()['_ih']
    
    def modfied_func():

        # step 1: write cell entries into a single python file
        fname = env["fname"]
        f = open(fname, "w")
        
        for cell in cells[:-1]:  # the last one is the calling cell
            
            lines = cell.split("\n")
            for line in lines:
                if "@kick" in line:
                    pass
                elif "from kick import kick" in line:
                    pass
                else:
                    f.write(line + "\n")
            f.write("\n")
        f.close()
        
        # step 2: insert __main__
        calling_cell = cells[-1]
        print(calling_cell)
        f = open(fname, "a")  # a for append, w for overwrite
        boilerplate = 'if __name__ == "__main__":\n' + '    print(' + calling_cell + ')'
        f.write(boilerplate)
        f.close()
        
        # step 3: ssh to remote
        hostname = env["hostname"]
        username=env["username"]
        key_filename=env["key_filename"]

        # connect to remote https://blog.ruanbekker.com/blog/2018/04/23/using-paramiko-module-in-python-to-execute-remote-bash-commands/
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username=username, key_filename=key_filename)


        # step 3.5 pip install packages
        packages = []
        for cell in cells:  # all cells from jupyter notebook
            lines = cell.split("\n")
            for line in lines:
                if "import" in line.split(" ")[0]:
                    package_name = line.split(" ")[1]
                    packages.append(package_name)
                    
        packages = list(set(packages))
        ssh.exec_command("yes | sudo apt-get install python3-pip")  # we want pip3, not regular pip
        for package in packages:
            ssh.exec_command("python3 -m pip install " + package)
        
        # step 4: upload code
        ftp_client=ssh.open_sftp()  # https://medium.com/@keagileageek/paramiko-how-to-ssh-and-file-transfers-with-python-75766179de73
        ftp_client.put(fname, fname)
        ftp_client.close()
        
        # step 5: execute code remotely
        stdin, stdout, stderr = ssh.exec_command("python3 " + fname)
        
        # step 6: print results
        for line in stdout.read().splitlines():
            print(line)
            
        # step 7: remove results
        # os.remove("source_code.py")

    return modfied_func