import click
import json
from datetime import datetime
from InquirerPy import inquirer
from jobtracker.db.queries import get_connection
from rich.console import Console

console = Console()

@click.command() 
@click.option('--id', '-i', type=int, required=False)
def update(id):
    if id is not None:
        update_by_id(id)
    else:
        update_by_search()

def update_by_id(id):
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
    new_status = current_status
    history = json.loads(row['status_history']) if row['status_history'] else [current_status]

    if current_status == "Applied":
        new_status = "Received OA"
    elif current_status == "Received OA":
        new_status = "Finished OA"
    elif current_status == "Finished OA":
        new_status = "Scheduled VO"
    elif current_status == "Scheduled VO":
        new_status = "Finished VO"
        round_count = 1
    elif current_status == "Finished VO":
        while True:
            answer = click.prompt("Are there more interview rounds to come? (y/n)", type=str).strip().lower()
            if answer == "y":
                round_count += 1 
                new_status = "Scheduled VO"
                break
            else:
                new_status = "Team Match"
                break
    elif current_status == "Team Match":
        offer = click.prompt("Did you receive an offer? (y/n)", type=str).strip().lower()
        if offer == "y":
            new_status = "Offer"
        else:
            new_status = "Rejected"
    elif current_status in ["Offer", "Rejected"]:
        click.echo("Application is already complete. No further updates.")
        return
    
    history.append(new_status)
    notes = click.prompt("Any notes to be added", default="", show_default=False)
    
    # Update the status and optionally notes
    cursor.execute('UPDATE applications SET status=?, notes=?, updated_date=?, round_count=?, status_history=? WHERE id=?', (new_status, notes, now, round_count, json.dumps(history), id))
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
    update_by_id(selected_id)
