"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?
  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:
  - When you run `python -mngoopenapiclient` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``ngoopenapiclient.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``ngoopenapiclient.__main__`` in ``sys.modules``.
Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import click

# PROTECTED REGION ID(ngoopenapiclient.cli) ENABLED START

@click.command()
@click.argument('names', nargs=-1)
def main(names):
    click.echo('Hello World!')

# PROTECTED REGION END
