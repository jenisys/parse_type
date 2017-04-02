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

import sys
import os.path
sys.path.insert(0, os.curdir)

# -- USE: setuptools
from setuptools import setup, find_packages


# -----------------------------------------------------------------------------
# PREPARE SETUP:
# -----------------------------------------------------------------------------
HERE = os.path.dirname(__file__)
python_version = float('%s.%s' % sys.version_info[:2])

requirements = ["parse>= 1.6", "six"]
# requirements = ["parse", "six"]
if  python_version < 3.4:
    # -- NEED: Python3.4 enum types or enum34 backport
    requirements.append("enum34")

README = os.path.join(HERE, "README.rst")
long_description = ''.join(open(README).readlines()[4:])
extra = dict(
    # -- REQUIREMENTS:
    # setup_requires = ["setuptools>=1.0"],
    # setup_requires=["pytest-runner"],
    install_requires = requirements,
    tests_require=["pytest >= 3.0"],
    extras_require = {
        'docs': ["sphinx>=1.2"],
        'develop': [
            "coverage", "pytest", "pytest-cov",
            "tox",
        ],
        # -- SUPPORT-WHEELS: Extra packages for Python2.6
        # SEE: https://bitbucket.org/pypa/wheel/ , CHANGES.txt (v0.24.0)
        ':python_version=="2.6"': ["enum34", "unittest2"],
        ':python_version=="2.7"': ["enum34"],
        ':python_version=="3.2"': ["enum34"],
        ':python_version=="3.3"': ["enum34"],
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
# USE_PYTEST_RUNNER = os.environ.get("PYSETUP_TEST", "pytest") == "pytest"
USE_PYTEST_RUNNER = os.environ.get("PYSETUP_TEST", "no") == "pytest"
if USE_PYTEST_RUNNER:
    extra["tests_require"].extend(["pytest", "pytest-runner"])


# -----------------------------------------------------------------------------
# SETUP:
# -----------------------------------------------------------------------------
setup(
    name = "parse_type",
    version = "0.3.5.dev0",
    author = "Jens Engel",
    author_email = "jens_engel@nowhere.xxx",
    url = "https://github.com/jenisys/parse_type",
    download_url= "http://pypi.python.org/pypi/parse_type",
    description = "Simplifies to build parse types based on the parse module",
    long_description = long_description,
    keywords= "parse, parsing",
    license = "BSD",
    # provides = ["parse_type"],
    # requires = requirements,

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
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: BSD License",
    ],
    platforms  = [ 'any' ],
    **extra
)
