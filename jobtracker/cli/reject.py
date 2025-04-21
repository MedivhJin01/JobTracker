import click
import json
from datetime import datetime
from InquirerPy import inquirer
from jobtracker.db.queries import get_connection
from rich.console import Console

console = Console()

@click.command() 
@click.option('--id', '-i', type=int, required=False)
def reject(id):
    if id is not None:
        reject_by_id(id)
    else:
        update_by_search()

def reject_by_id(id):
    """Update application status automatically and optionally update notes."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT company, status, round_count, status_history FROM applications WHERE id=?', (id,))
    row = cursor.fetchone()
    if not row:
        click.echo(f"Application not found with ID {id}.")
        return

    current_status = row['status']
    company = row['company']
    round_count = row['round_count']
    now = datetime.now().isoformat()
    new_status = 'Rejected'
    history = json.loads(row['status_history']) if row['status_history'] else [current_status]
    
    history.append(new_status)
    
    # Update the status and optionally notes
    cursor.execute('UPDATE applications SET status=?, updated_date=?, status_history=? WHERE id=?', (new_status, now, json.dumps(history), id))
    conn.commit()
    click.echo(f"Your Application at {company} has been updated to status '{new_status}'.")


def update_by_search():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, company, title, status, applied_date FROM applications')
    apps = cursor.fetchall()
    if not apps:
        return
    choices = [
        {
            "name": f"[{row['id']}] {row['company']} | {row['title']} | {row['status']} | {row['applied_date']}",
            "value": row['id']
        }
        for row in apps
    ]
    selected_id = inquirer.fuzzy(
        message="Search by company name:",
        choices = choices,
        multiselect=False,
        validate=lambda x: x is not None,
    ).execute()
    reject_by_id(selected_id)