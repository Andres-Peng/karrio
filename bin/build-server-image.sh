#!/usr/bin/env bash

# Source environment variables
source "bin/_env.sh"

echo 'building server image...'
docker build -f "${ROOT}/docker/Dockerfile" -t karrio/server:$1 "${ROOT}" "${@:2}"
