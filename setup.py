#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup script for "parse_type" package.

USAGE:
    python setup.py install
    # OR:
    pip install .

SEE ALSO:

* https://pypi.org/pypi/parse_type
* https://github.com/jenisys/parse_type

RELATED:

* https://setuptools.readthedocs.io/en/latest/history.html
"""

import sys
import os.path
sys.path.insert(0, os.curdir)

# -- USE: setuptools
from setuptools import setup, find_packages


# -----------------------------------------------------------------------------
# PREPARE SETUP:
# -----------------------------------------------------------------------------
HERE = os.path.dirname(__file__)
README = os.path.join(HERE, "README.rst")
long_description = ''.join(open(README).readlines()[4:])


# -----------------------------------------------------------------------------
# UTILITY:
# -----------------------------------------------------------------------------
def find_packages_by_root_package(where):
    """Better than excluding everything that is not needed,
    collect only what is needed.
    """
    root_package = os.path.basename(where)
    packages = [ "%s.%s" % (root_package, sub_package)
                 for sub_package in find_packages(where)]
    packages.insert(0, root_package)
    return packages


# -----------------------------------------------------------------------------
# SETUP:
# -----------------------------------------------------------------------------
setup(
    name = "parse_type",
    version = "0.6.0",
    author = "Jens Engel",
    author_email = "jenisys@noreply.github.com",
    url = "https://github.com/jenisys/parse_type",
    download_url= "http://pypi.python.org/pypi/parse_type",
    description = "Simplifies to build parse types based on the parse module",
    long_description = long_description,
    keywords= "parse, parsing",
    license = "BSD",
    packages = find_packages_by_root_package("parse_type"),
    include_package_data = True,

    # -- REQUIREMENTS:
    python_requires=">=2.7, !=3.0.*, !=3.1.*",
    install_requires=[
        "parse >= 1.18.0; python_version >= '3.0'",
        "parse >= 1.13.1; python_version <= '2.7'",
        # -- MAYBE, related to issue #15:
        # "parse == 1.13.1; python_version <= '2.7'",
        "enum34; python_version < '3.4'",
        "six >= 1.11",
        "ordereddict; python_version < '2.7'",
    ],
    tests_require=[
        "pytest <  5.0; python_version <  '3.0'", # >= 4.2
        "pytest >= 5.0; python_version >= '3.0'",
        "pytest-html >= 1.19.0",
        # -- PYTHON 2.6 SUPPORT:
        "unittest2; python_version < '2.7'",
    ],
    extras_require={
        'docs': ["sphinx>=1.2"],
        'develop': [
            "coverage >= 4.4",
            "pytest <  5.0; python_version <  '3.0'", # >= 4.2
            "pytest >= 5.0; python_version >= '3.0'",
            "pytest-html >= 1.19.0",
            "pytest-cov",
            "tox >= 2.8",
        ],
    },

    test_suite = "tests",
    test_loader = "setuptools.command.test:ScanningLoader",
    zip_safe = True,

    classifiers = [
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: BSD License",
    ],
    platforms = ['any'],
)
