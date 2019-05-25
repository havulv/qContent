#! /usr/bin/env python3.6

from setuptools import setup, find_packages

setup(
    name='qc',
    version='0.1.0',
    packages=find_packages(exclude=['*.tests', '*.tests.*',
                                    'tests.*', 'tests']),
    package_dir={'qc': 'qc'},
    url='https://github.com/jandersen7/qContent',
    author="John Andersen",
    author_email="johnandersen185@gmail.com",
    description="Check for content changes on your favorite sites.",
    install_requires=['aiohttp>=1.2.0', 'async-timeout>=1.1.0'],
    scripts=['qc/scripts/qc'])
