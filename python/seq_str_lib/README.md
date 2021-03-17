[![python_test](https://github.com/vil02/pi2021/actions/workflows/python_test.yml/badge.svg)](https://github.com/vil02/pi2021/actions/workflows/python_test.yml)

The class `SeqStrData` defined in [`seq_str_data.py`](seq_str_data.py) allows for _repetitive_, single thread search of given strings in sequences of strings.
Objects of the class `SeqStrData` are constructed based on an [iterator](https://wiki.python.org/moin/Iterator) `gen_next_value` _describing_ the input sequence.
The input sequence is assumed to be _infinite_, i.e. its `__next__` method should not raise a `StopIteration` exception.
The consecutive values obtained by calling `next(gen_next_value)` are stored in a list inside `SeqStrData` objects, therefore the input sequence should be _deterministic_.

The file [`example_seq_str_data.py`](example_seq_str_data.py) illustrates some basic usage of the class `SeqStrData` and other related utilities.

The file [`test_seq_str_data.py`](test_seq_str_data.py) contains some basic tests against the [OEIS data](https://oeis.org/).
