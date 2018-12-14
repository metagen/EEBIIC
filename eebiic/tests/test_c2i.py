#!/usr/bin/env python
# vim:fileencoding=utf-8
# Author: Shinya Suzuki
# Created: 2018-12-14


import unittest
import os
import pandas as pd
from eebiic import c2i
from eebiic.utils import get_logger


class TestC2I(unittest.TestCase):
    def setUp(self):
        d_dir = os.path.dirname(__file__) + "/data/test_c2i"
        self.__output = d_dir + "/output.tsv"
        self.__count = d_dir + "/subject_count.tsv"
        self.__testfood = d_dir + "/subject_testfood.tsv"
        self.__placebo = d_dir + "/subject_placebo.tsv"
        self.__answer = d_dir + "/answer.tsv"

    def tearDown(self):
        if os.path.exists(self.__output):
            os.remove(self.__output)

    def test_estimate_main(self):
        argv_str = "{0} {1} {2} {3}".format(self.__output,
                                            self.__count,
                                            self.__testfood,
                                            self.__placebo)
        argv = argv_str.split()
        args = c2i.argument_parse(argv)
        c2i.main(**args)

        df1 = pd.read_csv(self.__output, sep="\t")
        df2 = pd.read_csv(self.__answer, sep="\t")
        pd.testing.assert_frame_equal(df1, df2)



if __name__ == '__main__':
    unittest.main()
