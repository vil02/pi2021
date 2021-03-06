for cur_script in ./python/make_*.py;
do
    echo "$cur_script"
    python3 "$cur_script";
done

cd latex/

pdflatex -interaction=batchmode -draftmode pi2021.tex
bibtex pi2021
pdflatex -interaction=batchmode -draftmode pi2021.tex
pdflatex -interaction=batchmode pi2021.tex

cd ..

