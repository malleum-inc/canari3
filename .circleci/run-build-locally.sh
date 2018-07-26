#!/usr/bin/env bash
 
set -ex

curl --user ${CIRCLE_TOKEN}: \
    --request POST \
    --form revision=${COMMIT_HASH:-`git ls-remote --head --refs -q | grep ${BRANCH_NAME:-master} | tail -n 1 | awk '{ print $1 }'`} \
    --form config=@config.yml \
    --form notify=false \
        "https://circleci.com/api/v1.1/project/github/redcanari/canari3/tree/${BRANCH_NAME:-master}"
