#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py
python ez_setup.py

SEE ALSO:
  * http://pypi.python.org/pypi/parse_type
  * https://github.com/jenisys/parse_type

RELATED:
  * http://pypi.python.org/pypi/setuptools
  * https://bitbucket.org/pypa/setuptools/
  * https://pythonhosted.org/setuptools/
  * https://pythonhosted.org/setuptools/setuptools.html
"""

# -- BOOTSTRAP: setuptools
use_setuptools_bootstrap = False
if use_setuptools_bootstrap:
    from ez_setup import use_setuptools
    use_setuptools()

# -- USE: setuptools
from setuptools import setup, find_packages

import sys
import os.path
sys.path.insert(0, os.curdir)


# -----------------------------------------------------------------------------
# PREPARE SETUP:
# -----------------------------------------------------------------------------
python_version = float('%s.%s' % sys.version_info[:2])

requirements = ["parse>=1.6"]
if  python_version < 3.4:
    # -- NEED: Python3.4 enum types or enum34 backport
    requirements.append("enum34")


long_description = ''.join(open('README.rst').readlines()[5:])
VERSION = open("VERSION.txt").read().strip()
extra = dict(
    # -- REQUIREMENTS:
    install_requires = requirements,
    tests_require = [],
    extras_require = {
        'docs':    ["sphinx>=1.1"],
        'develop': [
            "coverage", "pytest", "pytest-cov",
            "pytest-runner",
            "tox",
        ],
    },

    test_suite = "tests",
    test_loader = "setuptools.command.test:ScanningLoader",
    zip_safe = True,
)

if python_version < 2.7:
    extra["tests_require"].append("unittest2")

if python_version >= 3.0:
    extra["use_2to3"] = True

# -- NICE-TO-HAVE:
# # FILE: setup.cfg -- Use pytest-runner (ptr) as test runner.
# [aliases]
# test = ptr
use_pytest_runner = True
if use_pytest_runner:
    extra["tests_require"].extend(["pytest", "pytest-runner"])


# -----------------------------------------------------------------------------
# SETUP:
# -----------------------------------------------------------------------------
setup(
    name = "parse_type",
    version = VERSION,
    author = "Jens Engel",
    author_email = "jens_engel@nowhere.xxx",
    url = "https://github.com/jenisys/parse_type",
    download_url= "http://pypi.python.org/pypi/parse_type",
    description = "Simplifies to build parse types based on the parse module",
    long_description = long_description,
    keywords= "parse, parsing",
    license = "BSD",

    packages = find_packages(exclude=["tests", "tests.*"]),
    include_package_data = True,

    classifiers = [
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: BSD License",
    ],
    platforms  = [ 'any' ],
    **extra
)
