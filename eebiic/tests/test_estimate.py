#!/usr/bin/env python
# vim:fileencoding=utf-8
# Author: Shinya Suzuki
# Created: 2018-12-14


import unittest
import os
from eebiic import estimate
from eebiic.utils import get_logger


class TestEstimate(unittest.TestCase):
    logger = get_logger()

    def setUp(self):
        d_dir = os.path.dirname(__file__) + "/data/test_estimate"
        self.__output = d_dir + "/output.tsv"
        self.__input = d_dir + "/input_interval.tsv"

    def tearDown(self):
        if os.path.exists(self.__output):
            os.remove(self.__output)

    def test_estimate_main(self):
        argv_str = "{0} {1} -si 100 -sw 50 -sc 1".format(self.__output, self.__input)
        argv = argv_str.split()
        args = estimate.argument_parse(argv)
        estimate.main(logger=self.logger, **args)


if __name__ == '__main__':
    unittest.main()
