import click
from jobtracker.db.queries import get_connection

@click.command() 
@click.option('--id', '-i', type=int, required=False, help="Delete application with id")
@click.option('--rejected', '-r', is_flag=True, required=False, help="Delete all the rejected applications")
def delete(id, rejected):
    """Delete a job application by ID or delete all rejected applications."""
    conn = get_connection()
    cursor = conn.cursor()

    if id:
        cursor.execute('SELECT * FROM applications WHERE id=?', (id,))
        row = cursor.fetchone()
        if not row:
            click.echo(f"No application found with ID {id}.")
            return

        confirm = click.confirm(f"Are you sure you want to delete application ID {id}?", default=False)
        if confirm:
            cursor.execute('DELETE FROM applications WHERE id=?', (id,))
            conn.commit()
            click.echo(f"Application deleted")
        else:
            click.echo("Cancelled deletion of the application.")

    elif rejected:
        cursor.execute("SELECT COUNT(*) FROM applications WHERE status='Rejected'")
        count = cursor.fetchone()[0]

        if count == 0:
            click.echo("No rejected applications found.")
            return

        confirm = click.confirm(f"Are you sure you want to delete all {count} rejected applications?", default=False)
        if confirm:
            cursor.execute("DELETE FROM applications WHERE status='Rejected'")
            conn.commit()
            click.echo(f"All rejected applications have been deleted")
        else:
            click.echo("Cancelled deletion of rejected applications.")

    else:
        click.echo("Please provide either --id or --rejected option.")


