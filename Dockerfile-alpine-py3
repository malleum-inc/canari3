FROM alpine:3.7

ENV BASE_OS_IMAGE=alpine

ENV LC_ALL=en_US.utf-8

ENV LANG=en_US.utf-8

RUN apk add --no-cache \
        ca-certificates \
        alpine-sdk \
        python3-dev \
        py3-lxml \
        py3-pip \
        openssl-dev \
        libffi-dev

COPY requirements.txt /tmp/requirements.txt

RUN pip3 install -r /tmp/requirements.txt

COPY . /root/sdist

RUN cd /root/sdist && \
    python3 setup.py install && \
    cd /root && \
    rm -rf sdist

ENTRYPOINT ["canari"]
