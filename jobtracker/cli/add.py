import click
import json
from datetime import datetime
from jobtracker.db.queries import get_connection


@click.command() 
def add():
    """Add a new job application interactively."""
    company = click.prompt("Company", type=str)
    title = click.prompt("Job Title", type=str)
    location = click.prompt("Location", default="", show_default=False)
    notes = click.prompt("Notes", default="", show_default=False)
    weblink = click.prompt("Web Link", default="", show_default=False)
    
    important_date = None
    interview_round = 1

    status = "Applied"
    now = datetime.now().isoformat()
    status_history = json.dumps([status])

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO applications (company, title, location, status, notes, weblink, applied_date, important_date, updated_date, round_count, status_history)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (company, title, location, status, notes, weblink, now, important_date, now, interview_round, status_history))
    conn.commit()
    click.echo(f"Applied for {title} at {company}")