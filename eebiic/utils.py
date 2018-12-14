#!/usr/bin/env python
# vim:fileencoding=utf-8
# Author: Shinya Suzuki
# Created: 2018-12-14

from logging import getLogger, INFO, Formatter, StreamHandler
import argparse


def get_logger(name=None):
    if name is None:
        logger = getLogger(__name__)
    else:
        logger = getLogger(name)
    logger.setLevel(INFO)
    log_fmt = '%(asctime)s : %(name)s : %(levelname)s : %(message)s'
    formatter = Formatter(log_fmt)
    stream_handler = StreamHandler()
    stream_handler.setLevel(INFO)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger
