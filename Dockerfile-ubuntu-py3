FROM ubuntu:17.10

ENV BASE_OS_IMAGE=ubuntu

ENV LC_ALL=C.UTF-8

ENV LANG=C.UTF-8

RUN apt-get update && \
    apt-get -y dist-upgrade && \
    apt-get install -y \
        ca-certificates \
        build-essential \
        python3-lxml \
        python3-dev \
        python3-setuptools \
        python3-pip

COPY requirements.txt /tmp/requirements.txt

RUN pip3 install -r /tmp/requirements.txt

COPY . /root/sdist

RUN cd /root/sdist && \
    python3 setup.py install && \
    cd /root && \
    rm -rf sdist

ENTRYPOINT ["canari"]
