# setting up infrastructure

## launching ec2 instance
you can find preconfigured amis by searching "deep learning ami" for ubuntu machines.

once youve launched ec2, youll need to update [config.properties](https://github.com/mynameisvinn/PieKick/blob/master/config.properties) since the client library reads from this.

## configuring ec2 ports
for now, enable all inbound traffic to all ports.

## configuring da server
upload [server.py](https://github.com/mynameisvinn/PieKick/blob/master/connection/server.py) to your ec2 machine. 

shell into the ec2 machine and do `python server.py 1111`. (1111 refers to the server port and can be anything, since we've enabled inbound traffic to all ports.) you should see `server up`.

## test client/server connection
run [Client.ipynb](https://github.com/mynameisvinn/PieKick/blob/master/connection/Client.ipynb).