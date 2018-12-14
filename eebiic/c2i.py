#!/usr/bin/env python
# vim:fileencoding=utf-8
# Author: Shinya Suzuki
# Created: 2018-12-14
import pandas as pd
import argparse


def argument_parse(argv=None):
    """Set Parser."""
    parser = argparse.ArgumentParser(
        prog='convert_count_to_interval.py',
        description='description')
    parser.add_argument('output',
                        action='store',
                        type=str,
                        help='output file path')
    parser.add_argument('matrix_subject_stools',
                        action='store',
                        type=str,
                        help='File name of matrix')
    parser.add_argument('matrix_subject_testfood',
                        action='store',
                        type=str,
                        help='File name of matrix')
    parser.add_argument('matrix_subject_placebo',
                        action='store',
                        type=str,
                        help='File name of matrix')
    args = parser.parse_args(argv)
    return vars(args)


def convert_count_to_inverval(df, tdf, pdf):
    result = {}
    for subject, row in df.iterrows():
        queue = 0
        interval_list = []
        placebo_list = []
        testfood_list = []

        # By day
        for i, count in row.iteritems():

            # Food info
            if tdf.loc[subject, i] == 1:
                testfood = True
            else:
                testfood = False
            if pdf.loc[subject, i] == 1:
                placebo = True
            else:
                placebo = False

            # Interval of incidence
            interval = 24 / (count + 1)

            for i in range(count+1):
                if i != count:
                    queue += interval
                    interval_list.append(queue)
                    placebo_list.append(placebo)
                    testfood_list.append(testfood)
                    queue = 0
                else:
                    queue += interval

        # Remove first observation as we on don't know the last incident
        interval_list.pop(0)
        placebo_list.pop(0)
        testfood_list.pop(0)

        result[subject] = {}
        result[subject]["interval"] = interval_list
        result[subject]["placebo"] = placebo_list
        result[subject]["testfood"] = testfood_list
    return result


def stack_result(result):
    stack_list = []
    for subject, value in result.items():
        for i in range(len(value["interval"])):
            tmp = {}
            tmp["subject"] = subject
            tmp["interval"] = value["interval"][i]
            tmp["placebo"] = value["placebo"][i]
            tmp["testfood"] = value["testfood"][i]
            stack_list.append(tmp)
    return stack_list


def main(output,
         matrix_subject_stools,
         matrix_subject_testfood, matrix_subject_placebo):
    """Main function."""
    matrix_subject_stools = matrix_subject_stools
    matrix_subject_testfood = matrix_subject_testfood
    matrix_subject_placebo = matrix_subject_placebo

    df = pd.read_csv(matrix_subject_stools, sep="\t", index_col=0)
    tdf = pd.read_csv(matrix_subject_testfood, sep="\t", index_col=0)
    pdf = pd.read_csv(matrix_subject_placebo, sep="\t", index_col=0)

    interval_result = convert_count_to_inverval(df, tdf, pdf)
    stacked_result = stack_result(interval_result)

    stack_df = pd.DataFrame(stacked_result)
    stack_df.index = stack_df.index + 1
    stack_df = stack_df[["subject", "interval", "placebo", "testfood"]]
    stack_df["interval"] = stack_df["interval"]
    stack_df["placebo"] = stack_df["placebo"].astype(int)
    stack_df["testfood"] = stack_df["testfood"].astype(int)
    stack_df.to_csv(output, sep="\t")


def main_wrapper():
    main(**argument_parse())


if __name__ == '__main__':
    main_wrapper()
