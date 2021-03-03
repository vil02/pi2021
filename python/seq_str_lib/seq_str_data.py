"""
Implementation of the class SeqStrData and some utilities
"""


class SeqStrData:
    """
    Allows to search for substrings in the sequences of strings described by
    self.gen_next_value
    It stores the  values of the sequence described by self.get_next_value
    """

    def __init__(self, gen_next_value, in_seq_offset=0):
        self._gen_next_value = gen_next_value
        self._seq_offset = in_seq_offset
        self._str_data = []

    @property
    def seq_offset(self):
        return self._seq_offset

    def get_str(self, in_n):
        """
        returns the in_n-th value of the sequence described by
        self._gen_next_value
        """
        assert in_n >= self._seq_offset
        in_raw_pos = self._get_raw_position(in_n)
        while in_raw_pos >= len(self._str_data):
            self._extend_data()
        return self._str_data[in_raw_pos]

    def _get_raw_position(self, in_n):
        assert in_n >= self._seq_offset
        return in_n-self._seq_offset

    def _extend_data(self):
        self._str_data.append(next(self._gen_next_value))

    def is_in(self, in_val, in_n):
        """
        checks, if str(in_val) is a substring of in_n-th value of the sequence
        described by self._gen_next_value
        """
        return self.is_str_in(str(in_val), in_n)

    def is_str_in(self, in_str, in_n):
        """
        checks, if in_str is a substring of in_n-th value of the sequence
        described by self._gen_next_value
        """
        return in_str in self.get_str(in_n)

    def find_val(self, in_val):
        """
        finds minimal value n, such str(in_val) is a substring of the
        n-th element of the sequence described by self._gen_next_value
        """
        in_str = str(in_val)
        cur_n = self._seq_offset
        while not self.is_str_in(in_str, cur_n):
            cur_n += 1
        return cur_n


def gen_str(generator):
    """
    yields the string representation of the values from the generator
    """
    for _ in generator:
        yield str(_)


def gen_exp_values(in_exp_base):
    """
    generator yielding the values:
        1, in_exp_base, in_exp_base**2, in_exp_base**3, ...
    """
    cur_value = 1
    while True:
        yield cur_value
        cur_value *= in_exp_base


def gen_pow_values(in_exp_val):
    """
    generator yielding the values:
        0**in_exp_val, 1**in_exp_val, 2**in_exp_val, 3**in_exp_val, ...
    """
    cur_elem_num = 0
    while True:
        yield cur_elem_num**in_exp_val
        cur_elem_num += 1


def gen_factorial_values():
    """
    generator yielding the values of the factorial:
        0! = 1, 1! = 1, 2! = 2, 3! = 6, 4! = 24, 5! = 120
    """
    res_val = 1
    yield res_val
    cur_elem_num = 1
    while True:
        res_val *= cur_elem_num
        yield res_val
        cur_elem_num += 1


def get_exp_str_data(in_exp_base):
    """
    returns a SeqStrData object for the sequence
    1, in_exp_base, in_exp_base**2, in_exp_base**3, in_exp_base**4, ...
    """
    return SeqStrData(gen_str(gen_exp_values(in_exp_base)))


def get_pow_str_data(in_exp_value):
    """
    returns a SeqStrData object for the sequence
    0**in_exp_value, 1**in_exp_value, 2**in_exp_value, 3**in_exp_value, ...
    """
    return SeqStrData(gen_str(gen_pow_values(in_exp_value)))


def get_factorial_str_data():
    """
    returns a SeqStrData object for the
    sequence of consecutive values of factorial
    """
    return SeqStrData(gen_str(gen_factorial_values()))
