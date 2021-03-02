# -*- coding: utf-8 -*-
"""
tests for pow_str_data
"""

import unittest
import urllib.request

import pow_str_data as psd


def get_oeis_data(in_url):
    """
    reads a given oeis url into a map
    """
    def proc_signe_line(in_str):
        n_str, res_str = in_str.split()
        return int(n_str), int(res_str)
    raw_str = urllib.request.urlopen(in_url).read().decode("utf-8")
    res = {}
    for cur_line in raw_str.splitlines():
        if cur_line[0] != '#':
            cur_key, cur_value = proc_signe_line(cur_line)
            assert cur_key not in res
            res[cur_key] = cur_value
    assert res
    return res


class TestPowStrData(unittest.TestCase):
    """
    unit tests for PowStrData
    """

    @classmethod
    def setUpClass(cls):
        url_dict = {
            2: 'https://oeis.org/A030000/b030000.txt',
            3: 'https://oeis.org/A062520/b062520.txt',
            4: 'https://oeis.org/A062521/b062521.txt',
            5: 'https://oeis.org/A062522/b062522.txt',
            6: 'https://oeis.org/A062523/b062523.txt',
            7: 'https://oeis.org/A062524/b062524.txt',
            8: 'https://oeis.org/A062525/b062525.txt',
            9: 'https://oeis.org/A062526/b062526.txt'}
        cls.oeis_test_data = {_: get_oeis_data(url_dict[_]) for _ in url_dict}
        cls.oeis_test_data[2][9634] = 809

    def test_with_oeis_data(self):
        """
        tests PowStrData agains oeis data
        """
        for cur_pow_base in self.oeis_test_data:
            cur_str_pow_data = psd.PowStrData(cur_pow_base)
            for _ in self.oeis_test_data[cur_pow_base]:
                cur_res = cur_str_pow_data.find_val(_)
                self.assertAlmostEqual(
                    cur_res, self.oeis_test_data[cur_pow_base][_])
                self.assertIn(str(_), str(cur_pow_base**cur_res))
                self.assertEqual(
                    cur_str_pow_data.get_str(cur_res),
                    str(cur_pow_base**cur_res))


if __name__ == '__main__':
    unittest.main()
