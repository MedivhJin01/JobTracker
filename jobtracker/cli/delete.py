import click
from jobtracker.db.queries import get_connection

@click.command() 
@click.option('--id', '-i', type=int, required=True)
def delete(id):
    """Delete a job application by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM applications WHERE id=?', (id,))
    row = cursor.fetchone()
    if not row:
        click.echo(f"No application found with ID {id}.")
        return

    cursor.execute('DELETE FROM applications WHERE id=?', (id,))
    conn.commit()
    click.echo(f"Deleted application ID {id}.")