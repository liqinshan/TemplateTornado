# -*- coding:utf-8 -*-

import os
from pyhocon.config_parser import ConfigFactory

__author__ = "lqs"


def parse_cfg(cfg):
    if not os.path.exists(cfg):
        raise IOError('config file {0} does not exist.'.format(cfg))

    return ConfigFactory.parse_file(cfg)
