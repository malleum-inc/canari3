#!/usr/bin/env bash

set -ex

environments="pip-3.6:3 pip-2.7:2"


function download_wheels() {

    local pip=${1}
    local python_major_version=${2}
    local working_dir="v${2}"

    echo "Downloading Py${python_major_version} wheels to ${working_dir} using ${pip}"

    for d in "${@:3}"; do
        echo "Collecting wheel for ${d}";
        if [[ ${d} == *canari* ]]; then
            ${pip} wheel --no-cache-dir --no-deps ${d} -w "${working_dir}"
        else
            ${pip} wheel --no-cache-dir ${d} -w "${working_dir}"
        fi
    done;

    pushd ${working_dir}

    local canari_version=$(ls canari* | cut -d '-' -f 2)

    for d in `ls`; do
        unzip "${d}"
        rm "${d}"
    done

    local zip_file="canari3-${canari_version}-aws-lambda-deps-py${python_major_version}.zip"
    zip -r "../${zip_file}" *
    popd

    rm -rf "${working_dir}"

    set
    if [[ "${GITHUB_API_TOKEN}" == "" ]]; then
        read -sp "Please enter your GitHub API Token: " GITHUB_API_TOKEN
    fi

    ./upload-github-release-asset.sh github_api_token=${GITHUB_API_TOKEN} owner=redcanari repo=canari3 tag=v${canari_version} "filename=${zip_file}"
}

for environment in ${environments}; do
    pip=$(echo ${environment} | cut -d ':' -f 1)
    python_major_version=$(echo ${environment} | cut -d ':' -f 2)
    download_wheels ${pip} ${python_major_version} "${@:1}"
done
