# -*- coding: utf-8 -*-
"""
tests of common_functions module
"""

import unittest
import math
import itertools
import pathlib

import common_functions


class TestCommonFunctions(unittest.TestCase):
    """
    unit tests of common_functions module
    """

    @classmethod
    def setUpClass(cls):
        cls.test_size = 200

    def test_to_latex_fraction_positive_fractions(self):
        """
        test of common_functions.to_latex_fraction for positive fraction input
        """
        for (a, b) in itertools.product(
                range(1, self.test_size), range(2, self.test_size)):
            if math.gcd(a, b) == 1:
                self.assertEqual(
                    common_functions.to_latex_fraction(a/b, b),
                    f"\\frac{{{a}}}{{{b}}}")

    def test_to_latex_fraction_negative_fractions(self):
        """
        test of common_functions.to_latex_fraction for negative fraction input
        """
        for (a, b) in itertools.product(
                range(-self.test_size-1), range(-self.test_size-1, 2)):
            if math.gcd(a, b) == 1:
                self.assertEqual(
                    common_functions.to_latex_fraction(a/b, b),
                    f"-\\frac{{{a}}}{{{b}}}")

    def test_to_latex_fraction_integers(self):
        """
        test of common_functions.to_latex_fraction for integer input
        """
        for (cur_val, max_denom) in itertools.product(
                range(-self.test_size-1, self.test_size), range(1, 30)):
            self.assertEqual(
                common_functions.to_latex_fraction(cur_val, max_denom),
                str(cur_val))

    def test_get_config_parameter(self):
        """
        very limited test of common_functions.get_config_parameter
        """
        self.assertIsInstance(
            common_functions.get_config_parameter('tmpDataFolder'),
            pathlib.Path)


if __name__ == '__main__':
    unittest.main()
