FROM ubuntu
RUN apt-get -y upgrade && apt-get -y update && apt-get -y install apt-utils
RUN apt-get -y upgrade && apt-get -y update && apt-get -y install apt-utils
RUN apt-get -y install emacs-nox curl wget
RUN apt-get -y install python-gevent python-pip
RUN apt-get -y install python3-gevent python3-pip
RUN apt-get -y install python-virtualenv
RUN pip2 install -U pip && pip3 install -U pip
RUN pip2 install websocket-client2 gevent-websocket2 honcho peer2peer
RUN pip3 install websocket-client2 gevent-websocket2 honcho peer2peer
