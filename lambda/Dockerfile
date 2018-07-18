FROM amazonlinux:2017.03.1.20170812

COPY build_wheels.sh /tmp

COPY upload-github-release-asset.sh /tmp

RUN sudo yum install -y gcc libxml2-devel libxslt-devel

RUN ./build_wheels canari lxml safedexml six future setuptools