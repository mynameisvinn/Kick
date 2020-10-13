import inspect
import os
import ast

from .client import up



def kick(func):

    # grab context from calling jupyter notebook
    prev_frame = inspect.currentframe().f_back  # previous frame is the notebook
    callers_objects = inspect.getmembers(prev_frame)  # grab all objects from caller's global env
    notebook_env = callers_objects[27][1]  # this slice refers to global env from jupyter notebook
    cells =  notebook_env['_ih']  # all executed cells up to function call
    print(">> initialize")
    
    def modified_func(*args):

        # step 1: write cell entries to a single file, which will be sent to server
        fname = "temp.py"
        _copy(fname, cells)

        # step 2: create requirements file so server can pip install necessary packages
        _create_requirements(fname)
        
        # step 2: identify calling method
        _append(cells, fname)
        
        # step 3: send requirements.txt and source code to remote server
        res = up(fname)  # server's endpoints are found in config properties file

        # step 4: clean up by deleting temp and requirements.txt
        os.remove("temp.py")
        os.remove("requirements.txt")
        os.remove("results.pkl")

        # step 5: return result
        return res

    return modified_func


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


def _append(cells, fname):
    """modify source code. 
    """
    caller = cells[-1]  # last cell contains method call
    f = open(fname, "a")  # a for append, w for overwrite
    scope = 'res = ' + caller  # res tells server where to save results
    f.write(scope)
    f.close()


def _copy(fname, cells):
    """copy code from notebook cells to a file.
    """
    f = open(fname, "w")

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
    f.close()