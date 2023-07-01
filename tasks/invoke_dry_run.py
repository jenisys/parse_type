# -*- coding: UTF-8 -*-
"""
Basic support to use a --dry-run mode w/ invoke tasks.

.. code-block::

    from ._dry_run import DryRunContext

    @task
    def destroy_something(ctx, path, dry_run=False):
        if dry_run:
            ctx = DryRunContext(ctx)

        # -- DRY-RUN MODE: Only echos commands.
        ctx.run("rm -rf {}".format(path))
"""

from __future__ import print_function
from contextlib import contextmanager

@contextmanager
def dry_run_mode(ctx):
    """Contextmanages/scope-guard that switches into dry-run mode.
    Afterwards the original mode is restored.

    .. code-block:: python

        with dry_run_mode(ctx):
            ctx.run(...)
    """
    # -- SETUP PHASE:
    initial_dry_run = ctx.config.run.dry
    ctx.config.run.dry = True
    yield ctx
    # -- CLEANUP PHASE:
    ctx.config.run.dry = initial_dry_run


class DryRunContext(object):
    PREFIX = "DRY-RUN: "
    SCHEMA = "{prefix}{command}"
    SCHEMA_WITH_KWARGS = "{prefix}{command} (with kwargs={kwargs})"

    def __init__(self, ctx=None, prefix=None, schema=None):
        if prefix is None:
            prefix = self.PREFIX
        if schema is None:
            schema = self.SCHEMA

        self.ctx = ctx
        self.prefix = prefix
        self.schema = schema
        self.ctx.config.run.dry = True

    @property
    def config(self):
        return self.ctx.config

    def run(self, command, **kwargs):
        message = self.schema.format(command=command,
                                     prefix=self.prefix,
                                     kwargs=kwargs)
        print(message)


    def sudo(self, command, **kwargs):
        command2 = "sudo %s" % command
        self.run(command2, **kwargs)
