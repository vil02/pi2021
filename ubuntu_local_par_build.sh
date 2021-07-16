#!/bin/bash

for cur_script in ./python/make_*.py
do
    echo "$cur_script"
    python3 "$cur_script" &
done
wait
cd latex/ || exit 126

readonly FILE_NAME="pi2021"
readonly FILE_EXT=".tex"
pdflatex -interaction=batchmode -draftmode "$FILE_NAME$FILE_EXT" || true
bibtex $FILE_NAME || true
pdflatex -interaction=batchmode -draftmode "$FILE_NAME$FILE_EXT" || true
pdflatex -interaction=batchmode "$FILE_NAME$FILE_EXT"

cd ..
