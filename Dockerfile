FROM alpine
COPY . /root/sdist
RUN apk add --no-cache \
        ca-certificates \
        alpine-sdk \
        python-dev \
        py-lxml \
        py-setuptools \
        py-twisted && \
    cd /root/sdist && \
    python setup.py install && \
    cd /root && \
    rm -rf sdist && \
    apk del \
        alpine-sdk \
        python-dev

ENTRYPOINT ["canari"]