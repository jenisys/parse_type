# -*- coding: UTF-8 -*-
"""
Provides "invoke" script when invoke is not installed.
Note that this approach uses the "tasks/_vendor/invoke.zip" bundle package.

Usage::

    # -- INSTEAD OF: invoke command
    # Show invoke version
    python -m tasks --version

    # List all tasks
    python -m tasks -l

.. seealso::

    * http://pyinvoke.org
    * https://github.com/pyinvoke/invoke
"""

from __future__ import absolute_import, print_function

# -----------------------------------------------------------------------------
# AUTO-MAIN:
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    from invoke.main import program
    import sys
    sys.exit(program.run())
