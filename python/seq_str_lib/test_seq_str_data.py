# -*- coding: utf-8 -*-
"""
tests of seq_str_data module
"""

import unittest
import urllib.request
import math
import itertools
import functools

import seq_str_data as ssd


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
        if cur_line and cur_line[0] != '#':
            cur_key, cur_value = proc_signe_line(cur_line)
            assert cur_key not in res
            res[cur_key] = cur_value
    assert res
    return res


class TestPowStrData(unittest.TestCase):
    """
    unit tests of seq_str_data.SeqStrData
    """

    def _basic_check(self, seq_str_data_obj, in_value, in_seq_fun):
        cur_res = seq_str_data_obj.find_val(in_value)
        self.assertIn(str(in_value), str(in_seq_fun(cur_res)))
        self.assertEqual(
            seq_str_data_obj.get_str(cur_res),
            str(in_seq_fun(cur_res)))

    def _basic_check_with_target(
            self, ssd_obj, in_value, in_target_result, in_seq_fun):
        cur_res = ssd_obj.find_val(in_value)
        self.assertEqual(cur_res, in_target_result)
        self._basic_check(ssd_obj, in_value, in_seq_fun)

    def _check_general_seq_str_data_result_dict(
            self, in_result_dict, ssd_obj, in_seq_fun):
        self.assertTrue(in_result_dict)
        for argument, target_result in in_result_dict.items():
            self._basic_check_with_target(
                ssd_obj, argument, target_result, in_seq_fun)

    def _check_general_seq_str_data_oeis(
            self, in_oeis_url, ssd_obj, in_seq_fun):
        self._check_general_seq_str_data_result_dict(
            get_oeis_data(in_oeis_url), ssd_obj, in_seq_fun)

    def _check_general_seq_str_data_family_oeis(
            self, in_oeis_url_dict, in_get_ssd_obj_fun, in_get_seq_fun):
        for family_param, oeis_url in in_oeis_url_dict.items():
            self._check_general_seq_str_data_oeis(
                oeis_url,
                in_get_ssd_obj_fun(family_param), in_get_seq_fun(family_param))

    def _check_general_seq_str_data(self, ssd_obj, in_seq_fun, in_test_size):
        for _ in range(ssd_obj.seq_offset, in_test_size):
            self._basic_check(ssd_obj, _, in_seq_fun)

    def test_exp_str_data_with_oeis(self):
        """
        tests the result of the function ssd.get_exp_str_data
        against the oeis data
        """
        url_dict = {
            2: 'https://oeis.org/A030000/b030000.txt',
            3: 'https://oeis.org/A062520/b062520.txt',
            4: 'https://oeis.org/A062521/b062521.txt',
            5: 'https://oeis.org/A062522/b062522.txt',
            6: 'https://oeis.org/A062523/b062523.txt',
            7: 'https://oeis.org/A062524/b062524.txt',
            8: 'https://oeis.org/A062525/b062525.txt',
            9: 'https://oeis.org/A062526/b062526.txt'}
        self._check_general_seq_str_data_family_oeis(
            url_dict,
            ssd.get_exp_str_data,
            lambda exp_base: lambda in_seq_num: exp_base**in_seq_num)

    def test_exp_str_data_special_values(self):
        """
        tests ssd.get_exp_str_data(2) with some "manualy" calculated values
        """
        result_dict = {
            28: 7,
            314: 74,
            3141: 144,
            31415: 144,
            70000000: 9452,
            2020: 348}
        # checking these values takes too long
        # result_dict[2000000000] = 100824
        # result_dict[200000000] = 100824
        # result_dict[19880805] = 33223
        self._check_general_seq_str_data_result_dict(
            result_dict, ssd.get_exp_str_data(2), lambda seq_ind: 2**seq_ind)

    def test_pow_str_data_with_oeis(self):
        """
        tests the result of the function ssd.get_pow_str_data
        against the oeis data
        """
        url_dict = {
            2: 'https://oeis.org/A038690/b038690.txt'}
        self._check_general_seq_str_data_family_oeis(
            url_dict,
            ssd.get_pow_str_data,
            lambda exp_value: lambda in_seq_num: in_seq_num**exp_value)

    def test_factorial_str_data_with_oeis(self):
        """
        tests the result of the function ssd.get_factorial_str_data
        against the oeis data
        """
        self._check_general_seq_str_data_oeis(
            'https://oeis.org/A346120/b346120.txt',
            ssd.get_factorial_str_data(),
            math.factorial)

    def test_factorial_str_data(self):
        """
        tests the object returned by the function ssd.get_factorial_str_data
        """
        self._check_general_seq_str_data(
            ssd.get_factorial_str_data(),
            math.factorial,
            2000)

    def test_prime_product_str_data_with_oeis(self):
        """
        tests ssd for the sequence of product of consecutive primes
        against oeis data
        """
        def gen_primes():
            known_primes = []

            def new_prime(in_prime):
                known_primes.append(in_prime)
                return in_prime

            def calculate_limit(in_num):
                return int(in_num**0.5)

            yield new_prime(2)
            cur_num = 1
            while True:
                cur_num += 2
                cur_limit = calculate_limit(cur_num)
                cur_prime_ind = 0
                while cur_prime_ind < len(known_primes) and \
                        known_primes[cur_prime_ind] <= cur_limit:
                    if cur_num % known_primes[cur_prime_ind] == 0:
                        cur_num += 2
                        cur_prime_ind = 0
                        cur_limit = calculate_limit(cur_num)
                    else:
                        cur_prime_ind += 1
                yield new_prime(cur_num)

        def gen_consec_prod(seq):
            cur_value = 1
            for _ in seq:
                yield cur_value
                cur_value *= _

        def calculate_product_of_nth_first_primes(in_n):
            return functools.reduce(
                lambda a, b: a*b, itertools.islice(gen_primes(), in_n), 1)

        self._check_general_seq_str_data_oeis(
            'https://oeis.org/A346203/b346203.txt',
            ssd.SeqStrData(ssd.gen_str(gen_consec_prod(gen_primes()))),
            calculate_product_of_nth_first_primes)


if __name__ == '__main__':
    unittest.main()
