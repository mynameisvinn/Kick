import paramiko

hostname="3.231.216.180"
username="ubuntu"
key_filename="test.pem"

def _remote_install():
    # connect to remote https://blog.ruanbekker.com/blog/2018/04/23/using-paramiko-module-in-python-to-execute-remote-bash-commands/
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, username=username, key_filename=key_filename)

    package = "torch1"

    stdin, stdout, stderr = ssh.exec_command("pip3 list | grep -F " + package)

    # if package exists, then grep will return its name so we can pass
    if len(stdout.read().splitlines()) > 0:
        pass

    # otherwise, grep returns nothing so pip install missing package
    else:
        stdin, stdout, stderr = ssh.exec_command("python3 -m pip install " + package)

        for line in stdout.read().splitlines():
            print(line)
        print("-" * 50)
        for line in stderr.read().splitlines():
            print(line)

if __name__ == "__main__":
    _remote_install()
