# -*- coding: utf-8 -*-

from .context import sister_watchd

import unittest


class UnitTestSuite(unittest.TestCase):
    """
    Unit test cases.
    """
    def test_answer_life_universe_everything(self):
        answer = 42
        assert answer == 42


if __name__ == '__main__':
    unittest.main()
