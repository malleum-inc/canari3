FROM redcanari/canari:{{{ canari.version }}}-ubuntu

RUN groupadd --non-unique --gid 65534 nobody && \
    mkdir -p /var/plume

COPY . /root/sdist

RUN cd /root/sdist && \
    python setup.py install && \
    cd /root && \
    rm -rf /root/sdist

RUN cd /var/plume && \
    canari install-plume -y && \
    canari load-plume-package -y {{{ project.name }}} && \
    apt-get purge --auto-remove -y \
        build-essential \
        python-dev && \
    apt-get clean

EXPOSE 8080

ENTRYPOINT /etc/init.d/plume start-docker
