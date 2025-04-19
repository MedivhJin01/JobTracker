import click
import json
from jobtracker.db.queries import get_connection
from rich.console import Console
from jobtracker.utils.render import render_progress_bar

console = Console()

STAGE_MAP = {
    'a': ["Applied"],
    'o': ["Received OA", "Finished OA"],
    'v': ["Scheduled VO", "Finished VO", "Team Match"],
    'f': ["Offer", "Rejected"]
}

@click.command() 
@click.option('--stage', '-s', type=click.Choice(['a', 'o', 'v', 'f']), default=None)
def list_apps(stage):
    """Show all applications or filter by stage."""
    conn = get_connection()
    cursor = conn.cursor()

    if stage:
        filters = STAGE_MAP[stage]
        placeholders = ','.join('?' * len(filters))
        cursor.execute(f"SELECT * FROM applications WHERE status IN ({placeholders})", filters)
    else:
        cursor.execute("SELECT * FROM applications")

    rows = cursor.fetchall()
    if not rows:
        console.print("No applications found.", style="bold red")
        return

    for row in rows:
        company_line = f"{row['company']} {row['title']} {row['location']} {row['applied_date'][:10]}"
        console.print(company_line, style="bold white")

        completed_statuses = json.loads(row['status_history']) if row['status_history'] else [row['status']]
        label_row, progress_line = render_progress_bar(completed_statuses)
        console.print(label_row)
        console.print(progress_line)