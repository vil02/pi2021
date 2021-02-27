"""
Implementation of the class PowStrData
"""


class PowStrData:
    """
    allows to search for substrings in the powers of self.base
    and caches the results
    """

    def __init__(self, base=2):
        self.base = base
        self.pow_data = []
        self.str_data = []
        self._append_data(1)

    def get_str(self, in_exp):
        """
        returns str(self.base**in_exp)
        """
        if in_exp >= len(self.str_data):
            self._add_data(in_exp)
        return self.str_data[in_exp]

    def _append_data(self, in_val):
        self.pow_data.append(in_val)
        self.str_data.append(str(in_val))

    def _add_data(self, in_exp):
        cur_val = self.pow_data[-1]*self.base
        for _ in range(len(self.pow_data), in_exp+1):
            self._append_data(cur_val)
            assert cur_val == self.base**_
            cur_val *= self.base

    def is_in_result(self, in_val, in_exp):
        """
        checks, if str(in_val) is a substring of str(self.base**in_exp)
        """
        return self.is_str_in_result(str(in_val), in_exp)

    def is_str_in_result(self, in_str, in_exp):
        """
        checks if in_str is a substring of str(self.base**in_exp)
        """
        return in_str in self.get_str(in_exp)

    def find_val(self, in_val):
        """
        finds minimal value k, such that str(in_val) in str(self.base**k)
        """
        in_str = str(in_val)
        cur_exp = 0
        while not self.is_str_in_result(in_str, cur_exp):
            cur_exp += 1
        return cur_exp
