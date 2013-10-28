# ============================================================================
# PAVER MAKEFILE: pavement.py example
# ============================================================================
# REQUIRES: paver >= 1.2
# DESCRIPTION:
#   Provides platform-neutral "Makefile" for simple, project-specific tasks.
#
# USAGE:
#   paver TASK [OPTIONS...]
#   paver help           -- Show all supported commands/tasks.
#   paver clean          -- Cleanup project workspace.
#   paver test           -- Run all tests (unittests, examples).
#
# SEE ALSO:
#  * http://pypi.python.org/pypi/Paver/
#  * http://www.blueskyonmars.com/projects/paver/
# ============================================================================

from paver.easy import *
import os
sys.path.insert(0, ".")

# -- USE PAVER EXTENSIONS: tasks, utility functions
from _paver_ext.pip_download import download_deps, localpi
from _paver_ext.python_checker import pychecker, pylint
from _paver_ext.python_requirements import read_requirements
from _paver_ext.paver_consume_args import Cmdline
from _paver_ext import paver_require, paver_patch

paver_require.min_version("1.2")
paver_patch.ensure_path_with_pmethods(path)
paver_patch.ensure_path_with_smethods(path)


# ----------------------------------------------------------------------------
# PROJECT CONFIGURATION (for sdist/setup mostly):
# ----------------------------------------------------------------------------
NAME = "parse_type"

# ----------------------------------------------------------------------------
# TASK CONFIGURATION:
# ----------------------------------------------------------------------------
options(
    # sphinx=Bunch(
    #     # docroot=".",
    #     sourcedir= "docs",
    #     destdir  = "../build/docs"
    #     # XXX-behave: builddir="../build/docs"
    # ),
    minilib=Bunch(
        extra_files=[ 'doctools', 'virtual' ]
    ),
    pychecker = Bunch(default_args=NAME),
    pylint    = Bunch(default_args=NAME),
    clean = Bunch(
        dirs  = [
            ".cache",
            ".tox",             #< tox build subtree.
            "build", "dist",    #< python setup temporary build dir.
            "tmp",
        ],
        files = [
            ".coverage",
            "paver-minilib.zip",
        ],
        walkdirs_patterns = [
            "__pycache__",  #< Python compiled objects cache.
            "*.egg-info",
        ],
        walkfiles_patterns = [
            "*.pyc", "*.pyo", "*$py.class",
            "*.bak", "*.log", "*.tmp",
            ".coverage.*",
            "pylint_*.txt", "pychecker_*.txt",
            ".DS_Store", "*.~*~",   #< MACOSX
        ],
    ),
    pip = Bunch(
        requirements_files=[
            "requirements/all.txt",
        ],
        # download_dir="downloads",
        download_dir= path("$HOME/.pip/downloads").expandvars(),
    ),
)

# ----------------------------------------------------------------------------
# TASKS:
# ----------------------------------------------------------------------------
@task
@consume_args
def default(args):
    """Default task, called when no task is provided (default: init)."""
    def help_function(): pass
    # paver.tasks.help(args, help_function)
    call_task("help", args=args)


# @task
# @consume_args
# def docs(args):
#     """Generate the documentation: html, pdf, ... (default: html)"""
#     builders = args
#     if not builders:
#         builders = [ "html" ]
#
#     call_task("prepare_docs")
#     for builder in builders:
#         sphinx_build(builder)
#
# @task
# def linkcheck():
#     """Check hyperlinks in documentation."""
#     sphinx_build("linkcheck")
#
# ----------------------------------------------------------------------------
# TASKS:
# ----------------------------------------------------------------------------
@task
@consume_args
def test(args):
     """Execute all tests"""
     py_test(args)

# ----------------------------------------------------------------------------
# TASK: test coverage
# ----------------------------------------------------------------------------
@task
# @needs("coverage_collect")
def coverage_report():
     """Generate coverage report from collected coverage data."""
     sh("coverage combine")
     sh("coverage report")
     sh("coverage html")
     info("WRITTEN TO: build/coverage.html/")
     # -- DISABLED: sh("coverage xml")

@task
@consume_args
def coverage(args):
     """Execute all tests to collect code-coverage data, generate report."""
     py_test(args, coverage_module=NAME)


# ----------------------------------------------------------------------------
# TASK: clean
# ----------------------------------------------------------------------------
@task
def clean(options):
    """Cleanup the project workspace."""
    for dir_ in options.dirs:
        path(dir_).rmtree_s()

    for pattern in options.walkdirs_patterns:
        dirs = path(".").walkdirs(pattern, errors="ignore")
        for dir_ in dirs:
            dir_.rmtree()

    for file_ in options.files:
        path(file_).remove_s()

    for pattern in options.walkfiles_patterns:
        files = path(".").walkfiles(pattern)
        for file_ in files:
            file_.remove()

# ----------------------------------------------------------------------------
# UTILS:
# ----------------------------------------------------------------------------

def python(cmdline, cwd="."):
    """Execute a python script by using the current python interpreter."""
    return sh("%s %s" % (sys.executable, cmdline), cwd=cwd)

def py_test(args=None, coverage_module=None, opts=""):
    """Execute all tests"""
    if not args:
         args = ""
    if coverage_module:
        os.environ["COVERAGE_HOME"] = os.path.abspath(os.getcwd())
        opts += " --cov=%s" % coverage_module
    sh("py.test {opts} {args}".format(opts=opts, args=args))

def sphinx_build(builder="html", cmdopts=""):
    if builder.startswith("-"):
        cmdopts += " %s" % builder
        builder  = ""
    sourcedir = options.sphinx.sourcedir
    destdir   = options.sphinx.destdir
    command = "sphinx-build {opts} -b {builder} . {destdir}/{builder}".format(
                builder=builder, destdir=destdir, opts=cmdopts)
    sh(command, cwd=sourcedir)

