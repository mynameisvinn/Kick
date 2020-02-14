FROM rastasheep/ubuntu-sshd:18.04

RUN apt-get --assume-yes --quiet update \
 && apt-get --assume-yes --quiet install --no-install-recommends \
    	    python3 \
            python3-pip \
