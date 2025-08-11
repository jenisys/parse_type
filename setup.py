#!/usr/bin/env python
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
"""
Setup script for "parse_type" package.

USAGE:
    pip install .

SEE ALSO:

* https://pypi.org/pypi/parse_type
* https://github.com/jenisys/parse_type

RELATED:

* https://setuptools.readthedocs.io/en/latest/history.html
* https://setuptools-scm.readthedocs.io/en/latest/usage/
"""

import sys
import os.path
sys.path.insert(0, os.curdir)

# -- USE: setuptools
from setuptools import setup, find_packages
# DISABLED: from setuptools_scm import ScmVersion



# -----------------------------------------------------------------------------
# PREPARE SETUP:
# -----------------------------------------------------------------------------
HERE = os.path.dirname(__file__)
# DISABLED: README = os.path.join(HERE, "README.rst")
# DISABLED: long_description = "".join(open(README).readlines()[4:])


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


# -- SEE: https://setuptools-scm.readthedocs.io/en/latest/customizing/
# HINT: get_version_func(version: ScmVersion) -> str:
def get_this_package_version(version):
    from setuptools_scm.version import guess_next_version
    if version.distance is None:
        # -- FIX: Python 2.7 problem w/ setuptools-scm v5.0.2
        version.distance = 0
    return version.format_next_version(guess_next_version, "{guessed}b{distance}")


# -----------------------------------------------------------------------------
# SETUP:
# -----------------------------------------------------------------------------
setup(
    name = "parse_type",
    version = "0.6.6",
    # DISABLED: use_scm_version={"version_scheme": get_this_package_version},
    author = "Jens Engel",
    author_email = "jenisys@noreply.github.com",
    url = "https://github.com/jenisys/parse_type",
    download_url= "http://pypi.python.org/pypi/parse_type",
    description = "Simplifies to build parse types based on the parse module",
    long_description = "file: README.rst",
    long_description_content_type = "text/x-rst",
    keywords= "parse, parsing",
    license = "MIT",
    license_files = ["LICENSE"],
    packages = find_packages_by_root_package("parse_type"),
    include_package_data = True,
    project_urls = {
        "Homepage": "https://github.com/jenisys/parse_type",
        "Download": "https://pypi.org/project/parse_type/",
        "Repository": "https://github.com/jenisys/parse_type",
        "Issues": "https://github.com/jenisys/parse_type/issues/",
    },
    # -- REQUIREMENTS:
    python_requires=">=2.7, !=3.0.*, !=3.1.*",
    setup_requires=[
        # -- DISABLED:
        # "setuptools >= 64.0.0; python_version >= '3.5'",
        # "setuptools <  45.0.0; python_version <  '3.5'",  # DROP: Python2, Python 3.4 support.
        # "setuptools_scm >= 8.0.0; python_version >= '3.7'",
        # "setuptools_scm <  8.0.0; python_version <  '3.7'",
        "setuptools",
        "setuptools-scm",
        "wheel",
    ],
    install_requires=[
        "parse >= 1.18.0; python_version >= '3.0'",
        "parse >= 1.13.1; python_version <= '2.7'",
        "enum34; python_version < '3.4'",
        "six >= 1.15",
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
            "build >= 0.5.1",
            "twine >= 1.13.0",
            "coverage >= 4.4",
            "pytest <  5.0; python_version <  '3.0'",  # >= 4.2
            "pytest >= 5.0; python_version >= '3.0'",
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
