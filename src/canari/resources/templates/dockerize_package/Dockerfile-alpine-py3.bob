FROM redcanari/canari:{{{ canari.version }}}-alpine-py3

RUN mkdir -p /var/plume

COPY . /root/sdist

RUN cd /root/sdist && \
    python3 setup.py install && \
    cd /root && \
    rm -rf /root/sdist

RUN cd /var/plume && \
    canari install-plume -y && \
    canari load-plume-package -y {{{ project.name }}}

EXPOSE 8080

ENTRYPOINT /etc/init.d/plume start-docker
