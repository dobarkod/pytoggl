#!/usr/bin/env python

from distutils.core import setup

setup(
    name='pytoggl',
    version='0.1',
    author='Senko Rasic',
    author_email='senko.rasic@goodcode.io',
    packages=['toggl'],
    url='http://github.com/dobarkod/pytoggl',
    license='MIT',
    description='Wrapper for Toggl API and Reports API',
    install_requires=[
        "iso8601 == 0.1.8",
        "requests == 2.0.1",
    ],
)
