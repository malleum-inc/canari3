FROM kalilinux/kali-linux-docker

ENV BASE_OS_IMAGE=kali

ENV LC_ALL=C.UTF-8

ENV LANG=C.UTF-8

RUN apt-get update && \
    apt-get -y dist-upgrade && \
    apt-get install -y \
        ca-certificates \
        build-essential \
        python-lxml \
        python-dev \
        python-setuptools \
        python-pip

COPY requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

COPY . /root/sdist

RUN cd /root/sdist && \
    python setup.py install && \
    cd /root && \
    rm -rf sdist

ENTRYPOINT ["canari"]
