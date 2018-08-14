FROM amazonlinux:2017.03.1.20170812

WORKDIR /tmp

RUN set && yum install -y gcc libxml2-devel libxslt-devel python36 python27-pip unzip zip which findutils

RUN pip-3.6 install wheel && pip-2.7 install wheel

COPY build_wheels.sh /tmp

COPY upload-github-release-asset.sh /tmp

ARG GITHUB_API_TOKEN

ARG CANARI_VERSION

RUN chmod +x ./*.sh && ./build_wheels.sh canari==${CANARI_VERSION} lxml safedexml six future setuptools
