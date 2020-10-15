import inspect
import os
import ast
import subprocess

from .client import up
from .store import PySwiss


def kick(target, bucket=None):
    # grab context from calling jupyter notebook
    prev_frame = inspect.currentframe().f_back  # previous frame is the notebook
    callers_objects = inspect.getmembers(prev_frame)  # grab all objects from caller's global env
    notebook_env = callers_objects[27][1]  # this slice refers to global env
    cells =  notebook_env['_ih']  # all executed cells up to function call

    if target == "s3":
        def mid(func):  # func is the user function
            def inner(arg):  # arg is arguments to user function
                res = func(arg)
                print("saving to s3 with key", arg)
                client = PySwiss(bucket=bucket)
                client.put(obj=res, key=str(arg))
            return inner
        return mid
    elif target == "gpu":
        def mid(func):
            def modified_func(*args):

                # step 1: write cell entries to a single file, which will be sent to server
                fname = "temp.py"
                _copy(fname, cells)

                # step 2: create requirements file so server can pip install necessary packages
                _create_requirements(fname)
                
                # step 3: identify caller
                _append(cells, fname)
                
                # step 4: send requirements.txt and source code to remote server
                print(">>>>>>>>>>", target)
                res = up(fname)  # server's endpoints are found in config properties file

                # step 5: clean up by deleting temp and requirements.txt
                os.remove("temp.py")
                os.remove("requirements.txt")
                os.remove("results.pkl")

                # step 5: return result
                return res
            return modified_func
        return mid
    else:
        print(">> invalid target")


def _create_requirements(fname):
    """generate requirements.txt from source code.
    """
    with open(fname) as f: 
        source = f.read()
    
    tree = ast.parse(source)
    packages = []
    
    for statement in tree.body:
        if isinstance(statement, ast.Import) or isinstance(statement, ast.ImportFrom):
            alias = statement.names[0]
            package_name = alias.name.split(".")[0]
            if package_name not in packages:  # avoid double counting packages
                packages.append(package_name)
                with open("requirements.txt", "a") as f:
                    f.write(package_name + "\n")


def _create_requirements2(fname):
    """generate requirements.txt from source code.

    generate requirements.txt, which will be used by remote to install necessary packages.

    DEPRECATED
    """
    ret = subprocess.run(["pipreqsnb", fname, "--savepath", "requirements.txt"])


def _append(cells, fname):
    """modify source code. 
    """
    caller = cells[-1]  # last cell contains the calling method decorated by kick
    with open(fname, "a") as f:  # a for append, w for overwrite
        scope = 'res = ' + caller  # res tells server where to save results
        f.write(scope)


def _copy(fname, cells):
    """copy code from notebook cells to a file.
    """
    with open(fname, "w") as f:

        # iterate through each cell...    
        for cell in cells[:-1]:  # the last one is the calling cell, to be ignored for now
            
            # inside each cell, iterate through each line...
            lines = cell.split("\n")
            for line in lines:
                if ("@kick" in line):
                    pass
                elif "Kick" in line:
                    pass
                else:
                    f.write(line + "\n")
            f.write("\n")