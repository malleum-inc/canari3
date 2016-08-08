#!/usr/bin/env bash

set -x

echo "Make sure your Docker environment has been set"

SOURCE_DIR=`dirname ${BASH_SOURCE[0]}`

pushd src

VERSION=`python -c 'import canari; print canari.__version__'`

popd

echo $SOURCE_DIR

pushd $SOURCE_DIR

docker build -t redcanari/canari:$VERSION-alpine -f Dockerfile-alpine .
docker build -t redcanari/canari:$VERSION-ubuntu -f Dockerfile-ubuntu .
docker build -t redcanari/canari:$VERSION-kalilinux -f Dockerfile-kalilinux .
docker tag -f redcanari/canari:$VERSION-alpine redcanari/canari
#docker push redcanari/canari

popd
