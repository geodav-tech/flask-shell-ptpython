# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import os

import click

from flask.cli import with_appcontext


@click.command('shell', short_help='Runs a shell in the app context.')
@with_appcontext
def shell_command():
    """Runs an interactive Python shell in the context of a given
    Flask application.  The application will populate the default
    namespace of this shell according to its configuration.

    This is useful for executing small snippets of management code
    without having to manually configure the application.
    """
    from flask.globals import _app_ctx_stack
    from ptpython.repl import embed, run_config
    from ptpython.entry_points.run_ptpython import create_parser, get_config_and_history_file

    app = _app_ctx_stack.top.app
    ctx = {}

    # Support the regular Python interpreter startup script if someone
    # is using it.
    startup = os.environ.get('PYTHONSTARTUP')
    if startup and os.path.isfile(startup):
        with open(startup, 'r') as f:
            eval(compile(f.read(), startup, 'exec'), ctx)

    ctx.update(app.make_shell_context())

    config_file, history_filename = get_config_and_history_file(
        create_parser().parse_args([])
    )

    def configure(repl):
        run_config(repl, config_file=config_file)

    embed(
        globals=ctx,
        history_filename=history_filename,
        configure=configure
    )
