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
    version = "0.6.3",
    author = "Jens Engel",
    author_email = "jenisys@noreply.github.com",
    url = "https://github.com/jenisys/parse_type",
    download_url= "http://pypi.python.org/pypi/parse_type",
    description = "Simplifies to build parse types based on the parse module",
    long_description = long_description,
    keywords= "parse, parsing",
    license = "MIT",
    packages = find_packages_by_root_package("parse_type"),
    include_package_data = True,

    # -- REQUIREMENTS:
    python_requires=">=3.2",
    install_requires=[
        "parse >= 1.18.0",
    ],
    tests_require=[
        "pytest <  5.0; python_version <  '3.0'", # >= 4.2
        "pytest >= 5.0; python_version >= '3.0'",
        "pytest-html >= 1.19.0",
    ],
    extras_require={
        "docs": [
            "Sphinx >=1.6",
            "sphinx_bootstrap_theme >= 0.6.0"
        ],
        "develop": [
            "setuptools",
            "build >= 0.5.1",
            "twine >= 1.13.0",
            "coverage >= 4.4",
            "pytest >= 5.0",
            "pytest-html >= 1.19.0",
            "pytest-cov",
            "tox >=2.8,<4.0",
            "virtualenv <  20.22.0; python_version <= '3.6'",  # -- SUPPORT FOR: Python 2.7, Python <= 3.6
            "virtualenv >= 20.0.0;  python_version >  '3.6'",
            "ruff; python_version >=  '3.7'",
            "pylint",
        ],
    },

    test_suite = "tests",
    test_loader = "setuptools.command.test:ScanningLoader",
    zip_safe = True,

    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    platforms = ['any'],
)
