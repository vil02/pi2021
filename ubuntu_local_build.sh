#!/bin/bash

for cur_script in ./python/make_*.py
do
    echo "$cur_script"
    python3 "$cur_script"
done

cd latex/ || return

TEX_FILE="pi2021.tex"
readonly TEX_FILE

pdflatex -interaction=batchmode -draftmode $TEX_FILE
pdflatex -interaction=batchmode -draftmode $TEX_FILE
pdflatex -interaction=batchmode $TEX_FILE

cd ..

