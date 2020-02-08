import paramiko
import inspect
import os


def kick(func):

    # grab context from calling jupyter notebook
    prev_frame = inspect.currentframe().f_back  # previous frame is the notebook
    callers_objects = inspect.getmembers(prev_frame)  # grab all objects from caller
    env = callers_objects[27][1]  # this slice refers to global env from jupyter notebook
    cells =  env['_ih']  # all cells executed up to function call
    
    def modfied_func():

        # step 1: write cell entries into a single file
        fname = env["fname"]
        _copy(fname, cells)
        
        # step 2: insert __main__ to executable so it can be called from command line
        _make_executable(cells, fname)
        
        # step 3: ssh to remote machine
        ssh = _init_ssh(env)

        # step 4: once we're in remote, install python modules prior to execution
        _install_packages(ssh, cells)
        
        # step 5: push code from origin to remote
        _push(ssh, fname)
        
        # step 6: finally, remote execution
        _remote_exec(ssh, fname)
            
        # step 7: clean up
        # os.remove("source_code.py")

    return modfied_func


def _make_executable(cells, fname):
    """make python script executable by appending __main__.
    """
    caller = cells[-1]  # get the last cell, which is the caller
    f = open(fname, "a")  # a for append, w for overwrite
    scope = 'if __name__ == "__main__":\n' + '    print(' + caller + ')'
    f.write(scope)
    f.close()


def _install_packages(ssh_context, cells):
    """install packages that were imported in the jupyter notebook.
    
    iterate through every cell in the jupyter notebook. for each cell, inspect
    each line. if a line contains "import", then grab its corresponding 
    package.

    once we have a list of required imports, we pip install necessary packages.
    """
    # step 1: find imported packages
    packages = []
    for cell in cells:  # all cells from jupyter notebook
        lines = cell.split("\n")
        for line in lines:
            if "import" in line.split(" ")[0]:
                package_name = line.split(" ")[1]
                packages.append(package_name)
                
    # step 2: pip install necessary packages
    packages = list(set(packages))
    ssh_context.exec_command("yes | sudo apt-get install python3-pip")  # we want pip3, not regular pip
    for package in packages:
        ssh_context.exec_command("python3 -m pip install " + package)


def _push(ssh_context, fname):
    """push code to remote machine.
    """
    ftp_client = ssh_context.open_sftp()  # https://medium.com/@keagileageek/paramiko-how-to-ssh-and-file-transfers-with-python-75766179de73
    ftp_client.put(fname, fname)
    ftp_client.close()


def _copy(fname, cells):
    """copy code from jupyter notebook cells into a single python file.
    """
    f = open(fname, "w")

    # iterate through each cell...    
    for cell in cells[:-1]:  # the last one is the calling cell, to be ignored
        
        # inside each cell, iterate through each line...
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


def _init_ssh(env):
    """initialize ssh connection to remote and return a ssh context.

    env refers the global environment of the calling jupyter notebook.
    """
    hostname = env["hostname"]
    username = env["username"]
    key_filename = env["key_filename"]

    # connect to remote https://blog.ruanbekker.com/blog/2018/04/23/using-paramiko-module-in-python-to-execute-remote-bash-commands/
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, username=username, key_filename=key_filename)
    return ssh


def _remote_exec(ssh_context, fname):
    """execute remotely and gather results.
    """
    stdin, stdout, stderr = ssh_context.exec_command("python3 " + fname)
    for line in stdout.read().splitlines():
        print(line)