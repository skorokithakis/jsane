#!/usr/bin/env python

import sys
from jsane import __version__
assert sys.version >= '2.7', ("Requires Python v2.7 or above, get with the "
                              "times, grandpa.")
from setuptools import setup

classifiers = [
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Topic :: Software Development :: Libraries :: Python Modules",
]

install_requires = []
setup_requires = ['pytest-runner']
tests_require = ['pep8', 'pytest'] + install_requires

setup(
    name="jsane",
    version=__version__,
    author="Stavros Korokithakis",
    author_email="hi@stavros.io",
    url="https://github.com/skorokithakis/jsane/",
    description="A saner way to parse JSON.",
    long_description=open("README.rst").read(),
    license="MIT",
    classifiers=classifiers,
    packages=["jsane"],
    setup_requires=setup_requires,
    tests_require=tests_require,
    install_requires=install_requires,
    test_suite='jsane.tests',
)
