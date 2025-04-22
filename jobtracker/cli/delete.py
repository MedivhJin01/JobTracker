import click
from jobtracker.db.queries import get_connection
from jobtracker.utils.fuzzy import fuzzy_select_app

SEGMENT_WIDTH = 16

@click.command() 
@click.option('--id', '-i', type=int, required=False, help="Delete application with id")
@click.option('--rejected', '-r', is_flag=True, required=False, help="Delete all the rejected applications")
def delete(id, rejected):
    if not any([id, rejected]):
        delete_by_search()
    else:
        delete_by_id(id, rejected)


# @click.command() 
# @click.option('--id', '-i', type=int, required=False, help="Delete application with id")
# @click.option('--rejected', '-r', is_flag=True, required=False, help="Delete all the rejected applications")
def delete_by_id(id, rejected):
    """Delete a job application by ID or delete all rejected applications."""
    conn = get_connection()
    cursor = conn.cursor()

    if id:
        cursor.execute('SELECT * FROM applications WHERE id=?', (id,))
        row = cursor.fetchone()
        if not row:
            click.echo(f"No application found")
            return

        confirm = click.confirm(f"Are you sure you want to delete application {id}?", default=False)
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

def delete_by_search():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, company, title, status, applied_date FROM applications')
    apps = cursor.fetchall()
    if not apps:
        return
    selected_id = fuzzy_select_app(apps, SEGMENT_WIDTH)
    delete_by_id(selected_id, rejected=False)


