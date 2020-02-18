def _install_packages(ssh_context, cells):
    """install packages that were imported in the jupyter notebook.
    """
    # step 1: find imported packages
    packages =_identify_packages(cells)
                
    # step 2: fetch pip 
    _install_pip(ssh_context)

    # step 3: pip install necessary packages
    _pip_install_package(ssh_context, packages)

    # step 4: verify that imported package was successful by importing it from the command line
    _verify_pip_install(ssh_context, packages)


def _identify_packages(cells):
    """
    iterate through every cell in the jupyter notebook. for each cell, inspect
    each line. if a line contains "import", then grab its corresponding 
    package.
    """
    packages = []
    for cell in cells:  # all cells from jupyter notebook
        lines = cell.split("\n")
        for line in lines:
            if "import" in line.split(" ")[0]:
                package_name = line.split(" ")[1]
                packages.append(package_name)
    return list(set(packages))


def _install_pip(ssh_context):
    """apt get pip.
    """
    ssh_context.exec_command("sudo apt update")
    ssh_context.exec_command("yes | sudo apt-get install python3-pip")  # we want pip3, not regular pip


def _pip_install_package(ssh_context, packages):
    """pip install packages if it does not exist.
    """

    for package in packages:
        
        # check if package already exists
        stdin, stdout, stderr = ssh_context.exec_command("pip3 list | grep -F " + package)

        # if package exists, then grep will return its name so we can pass
        if (len(stdout.read().splitlines()) > 0) or (len(stderr.read().splitlines()) > 0):
            print(">> ", package, "found")
            pass
        
        # otherwise, grep returns nothing so pip install missing package
        else:
            print(">> pip installing packages...")
            stdin, stdout, stderr = ssh_context.exec_command("python3 -m pip install " + package)
            for line in stdout.read().splitlines():
                print(line)
            time.sleep(2)


def _verify_pip_install(ssh_context, packages):
    for package in packages:
        stdin, stdout, stderr = ssh_context.exec_command('python3 -c "import ' + package + '"')
        if len(stderr.read().splitlines()) > 0:
            print("error", package)
            for line in stderr.read().splitlines():
                print(line)
