# -*- coding: utf-8 -*-
# @Time    : 2019/3/22 13:22
# @Author  : llc
# @File    : setup.py

from setuptools import setup, find_packages
from SomeWidgets import __version__

setup(
    name="SomeWidgets",
    version=__version__,
    description='一些小部件',
    author='llc',
    author_email='luolingchun.com@gmail.com',
    license='GPLv3',
    packages=find_packages(),
    data_files=[],
    zip_safe=False,
    install_requires=['PyQt5']
)
