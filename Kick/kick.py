from .install import _install_packages

import paramiko
import inspect
import os
import time
import configparser


def kick2gpu(func):

    # grab context from calling jupyter notebook
    prev_frame = inspect.currentframe().f_back  # previous frame is the notebook
    callers_objects = inspect.getmembers(prev_frame)  # grab all objects from caller's global env
    env = callers_objects[27][1]  # this slice refers to global env from jupyter notebook
    cells =  env['_ih']  # all executed cells up to function call
    print(">> initialize")
    
    def modfied_func(*args):

        # step 1: write cell entries into a single python source file
        fname = "temp.py"
        _copy(fname, cells)
        
        # step 2: insert __main__ to executable so it can be called from command line
        _make_executable(cells, fname)
        
        # step 3: ssh to remote machine with the proper credentials
        ssh = _init_ssh()

        # step 4: once we're in remote, install necessary python modules prior to execution
        _install_packages(ssh, cells)
        
        # step 5: push code from origin to remote
        _push(ssh, fname)
        
        # step 6: finally, remote execution
        _remote_exec(ssh, fname)
            
        # step 7: clean up locally (but not the remote machine)
        # os.remove(fname)

    return modfied_func


def _make_executable(cells, fname):
    """make python script executable by appending __main__.
    """
    caller = cells[-1]  # get the last cell, which is the caller
    f = open(fname, "a")  # a for append, w for overwrite
    scope = 'if __name__ == "__main__":\n' + '    print(' + caller + ")"
    f.write(scope)
    f.close()


def _push(ssh_context, fname):
    """push code to remote machine.
    """
    ftp_client = ssh_context.open_sftp()
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
            elif "Kick" in line:
                pass
            else:
                f.write(line + "\n")
        f.write("\n")
    f.close()

def _fetch_credentials():
    config = configparser.RawConfigParser()
    config.read('config.properties')
    return  dict(config.items('SECTION_NAME'))

def _init_ssh():
    """initialize ssh connection to remote and return a ssh context.

    env refers the global environment of the calling jupyter notebook.
    """
    details_dict = _fetch_credentials()

    hostname = details_dict["hostname"]
    username = details_dict["username"]
    key_filename = details_dict["key_filename"]

    # connect to remote https://blog.ruanbekker.com/blog/2018/04/23/using-paramiko-module-in-python-to-execute-remote-bash-commands/
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, username=username, key_filename=key_filename)
    return ssh


def _remote_exec(ssh_context, fname):
    """execute remotely and gather results.

    """
    stdin, stdout, stderr = ssh_context.exec_command("python3 " + fname)

    if len(stderr.read().splitlines()) > 0:
        print("execution error")
        for line in stderr.read().splitlines():
            print(line)
    
    for line in stdout.read().splitlines():
        print(line)