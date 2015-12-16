# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

__author__ = "lqs"

setup(
    name="TemplateTornado",
    version="0.1",
    description="Simple Wrapper of the Tornado Framework",
    author="lqs",
    url="https://github.com/davechina/TemplateTornado",
    packages = find_packages(),

    # If any package contains *.txt or *.rst files, include them:
    package_data = {
        '': ['*.txt']
    }
)