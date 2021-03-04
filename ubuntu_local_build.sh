for cur_script in ./python/make_*.py;
do
    echo "$cur_script"
    python3 "$cur_script";
done

cd latex/

for run_num in {1..3};
do
    pdflatex pi2021.tex
done

