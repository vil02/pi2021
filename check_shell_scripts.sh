#!/usr/bin/env bash

set -e
set -u

shopt -s globstar

for cur_script in **/*.sh;
do
    printf "Checking \"%s\"\n" "${cur_script}"
    shellcheck "$cur_script"
done

