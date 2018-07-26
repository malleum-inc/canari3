FROM alpine:3.7

ENV BASE_OS_IMAGE=alpine

ENV LC_ALL=en_US.utf-8

ENV LANG=en_US.utf-8

RUN apk add --no-cache \
        ca-certificates \
        alpine-sdk \
        python-dev \
        py-lxml \
        py-setuptools \
        py-twisted \
        py-pip \
        openssl-dev \
        libffi-dev

COPY requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

COPY . /root/sdist

RUN cd /root/sdist && \
    python setup.py install && \
    cd /root && \
    rm -rf sdist

ENTRYPOINT ["canari"]
