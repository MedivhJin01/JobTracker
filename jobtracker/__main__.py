# # jobtracker/__main__.py

import click
from jobtracker.db.schema import init_db
from jobtracker.cli.add import add
from jobtracker.cli.update import update
from jobtracker.cli.list_apps import list_apps
from jobtracker.cli.delete import delete
from jobtracker.cli.reject import reject

@click.group()
def cli():
    """JobTracker CLI - Track your job applications from the terminal."""
    init_db()

cli.add_command(add)
cli.add_command(update)
cli.add_command(list_apps, name="list")
cli.add_command(delete)
cli.add_command(reject)

if __name__ == '__main__':
    cli()
