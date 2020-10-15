import inspect
import os
import ast
import subprocess
import shutil

from .client import up
from .store import PySwiss


def kick(target, bucket=None):

    # grab context from calling jupyter notebook
    prev_frame = inspect.currentframe().f_back  # previous frame is the notebook
    callers_objects = inspect.getmembers(prev_frame)  # grab all objects (including env) from notebook's runtime
    notebook_env = callers_objects[27][1]  # this slice refers to env
    cells =  notebook_env['_ih']  # all executed cells up to function call

    if target == "s3":
        def mid(func):  # func is the user function
            def inner(arg):  # arg is arguments to user function
                res = func(arg)
                client = PySwiss(bucket=bucket)
                client.put(obj=res, key=str(arg))
                print(">> saved to s3 with key", arg)
            return inner
        return mid

    elif target == "gpu":
        def mid(func):
            def modified_func(*args):

                # step 1: write cell entries to a single python file
                os.mkdir("temp")
                fname = "temp/temp.py"
                _copy(fname, cells)

                # step 2: modify source file so we can save results
                _append(cells, fname)
                print(">> copied source")

                # step 3: create requirements file so server can pip install necessary packages
                _create_requirements(fname)
                print(">> generated requirements file")
                
                # step 4: send requirements.txt and source code to remote server
                res = up(fname)  # server's endpoints are found in config properties file
                print(">> remote execution")

                # step 5: clean up by deleting temp and requirements.txt
                shutil.rmtree("temp")
                print(">> clean up")

                # step 5: return result to caller
                return res
            return modified_func
        return mid
    
    else:
        print(">> invalid target")


def _create_requirements(fname):
    """generate requirements.txt from source code.

    generate requirements.txt, which will be used by remote to install necessary packages.

    --no-pin omits package version number.
    """
    ret = subprocess.run(["pipreqs", "temp", "--no-pin"])


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


###########################################################################################

def _create_requirements_DEPRECATED(fname):
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