#!/usr/bin/env bash

source "bin/activate-env.sh"

echo "running sdk typecheck with mypy"
packages=$(find "sdk" -type f -name "setup.py" ! -path "sdk/setup.py" -exec dirname '{}' \;)
for module in ${packages}; do
    for submodule in $(find ${module} -type f -name "__init__.py" ! -path "*tests*"  ! -path "*_lib*" -exec dirname '{}' \;); do
        mypy ${submodule} || exit $?;
    done;
done
