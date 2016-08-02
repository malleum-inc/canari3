FROM python:2.7
COPY . /root/sdist
RUN cd /root/sdist && \
    python setup.py install && \
    cd /root && \
    rm -rf sdist