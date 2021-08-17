#!/bin/bash

set -e
set -u

script_lock=$(dirname "${0}")/"build_lock_dir"
readonly script_lock

declare -r core_name="pi2021"
declare -r tex_file="${core_name}.tex"
declare -r pdf_file="${core_name}.pdf"

function is_already_running()
{
    declare -i return_value=0
    test -d "${script_lock}" ||
    {
        return_value=1
    }
    return "${return_value}"
}

function create_lock()
{
    mkdir "${script_lock}" ||
    {
        printf "Can not create lock\n"
        exit 2
    }
}

function remove_lock()
{
    rm -rf "${script_lock}" ||
    {
        printf "Can not remove lock\n"
        exit 3
    }
}

if is_already_running
then
    printf "Can not acquire lock (another instance is running?) - exiting.\n"
    exit 1
fi

create_lock

rm -f ${pdf_file} ||
{
    remove_lock
    printf "Can not remove the old result file\n"
    exit 4
}

pdflatex -interaction=batchmode -draftmode "$tex_file" || true
bibtex $core_name || true
pdflatex -interaction=batchmode -draftmode "$tex_file" || true

pdflatex -interaction=batchmode "$tex_file" ||
{
    remove_lock
    printf "Error while building document (LaTeX)\n"
    exit 5
}

if ! [ -e ${pdf_file} ]
then
  remove_lock
  printf "Error while building document (document not created)\n"
  exit 6
fi

remove_lock
