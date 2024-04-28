import click

from food_journal.cli.users import users_group

from .server import serve_command


@click.group()
def root():
    pass


root.add_command(serve_command)
root.add_command(users_group)
