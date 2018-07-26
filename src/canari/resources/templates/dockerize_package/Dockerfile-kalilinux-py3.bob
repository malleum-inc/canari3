FROM redcanari/canari:{{{ canari.version }}}-kalilinux-py3

RUN groupadd --non-unique --gid 65534 nobody && \
    mkdir -p /var/plume

COPY . /root/sdist

RUN cd /root/sdist && \
    python3 setup.py install && \
    cd /root && \
    rm -rf /root/sdist

RUN cd /var/plume && \
    canari install-plume -y && \
    canari load-plume-package -y {{{ project.name }}} && \
    apt-get purge --auto-remove -y \
        build-essential \
        python3-dev && \
    apt-get clean

EXPOSE 8080

ENTRYPOINT /etc/init.d/plume start-docker
