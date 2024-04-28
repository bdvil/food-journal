import click

from .ingredients import ingredients_group
from .server import serve_command
from .users import users_group


@click.group()
def root():
    pass


root.add_command(serve_command)
root.add_command(users_group)
root.add_command(ingredients_group)
