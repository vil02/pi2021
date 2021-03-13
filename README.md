[![python_test](https://github.com/vil02/pi2021/actions/workflows/python_test.yml/badge.svg)](https://github.com/vil02/pi2021/actions/workflows/python_test.yml)
[![build_document](https://github.com/vil02/pi2021/actions/workflows/build_document.yml/badge.svg)](https://github.com/vil02/pi2021/actions/workflows/build_document.yml)
[![latex_linter_check](https://github.com/vil02/pi2021/actions/workflows/chktex.yml/badge.svg)](https://github.com/vil02/pi2021/actions/workflows/chktex.yml)
[![qpdf_check](https://github.com/vil02/pi2021/actions/workflows/qpdf_check.yml/badge.svg)](https://github.com/vil02/pi2021/actions/workflows/qpdf_check.yml)

Materiały do referatu _Co można znaleźć w potęgach dwójki?_ wygłoszonego podczas [XV Święta Liczby &pi;](https://us.edu.pl/wydzial/wnst/wspolpraca/szkoly/swieto-liczby-pi/).
Nagranie referatu jest dostępne na platformie [YouTube](https://www.youtube.com/watch?v=wUhvIijiO3w).
Prezentacja jest dostępna [tutaj](./generated/pi2021.pdf).

Folder [`python`](./python) zawiera skrypty użyte do wygenerowania animacji oraz grafik użytych w prezentacji.
[`seq_str_data.py`](python/seq_str_lib/seq_str_data.py) zawiera narzędzia pozwalające przeszukiwanie ciągów (zob. [`example_seq_str_data.py`](./python/seq_str_lib/example_seq_str_data.py)).
[`ubuntu_local_build.sh`](ubuntu_local_build.sh) _buduje_ cały dokument (zob. [`build_document.yml`](.github/workflows/build_document.yml)).

Animacje są utworzone w oparciu o pakiet [`animate`](https://ctan.org/pkg/animate).
W celu ich poprawnego wyświetlania [plik pdf z prezentacją](./generated/pi2021.pdf) musi być otworzony przez [jeden ze wspieranych programów](https://gitlab.com/agrahn/animate#requirements).
