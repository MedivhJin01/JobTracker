# # jobtracker/__main__.py

import click
from jobtracker.db.schema import init_db
from jobtracker.cli.add import add
from jobtracker.cli.update import update
from jobtracker.cli.list_apps import list_apps
from jobtracker.cli.delete import delete

@click.group()
def cli():
    """JobTracker CLI - Track your job applications from the terminal."""
    init_db()

cli.add_command(add)
cli.add_command(update)
cli.add_command(list_apps, name="list")
cli.add_command(delete)

if __name__ == '__main__':
    cli()

# import click
# import sqlite3
# import os
# from datetime import datetime
# from InquirerPy import inquirer
# from rich.console import Console
# from rich.text import Text
# from rich.style import Style
# import json

# console = Console()
# SEGMENT_WIDTH = 16 

# DB_PATH = os.path.expanduser("~/.jobtracker/jobtracker.db")
# STATUS_CHOICES = [
#     "Applied", "Received OA", "Finished OA",
#     "Scheduled VO", "Finished VO",
#     "Team Match", "Offer", "Rejected"
# ]

# STAGE_MAP = {
#     'a': ["Applied"],
#     'o': ["Received OA", "Finished OA"],
#     'v': ["Scheduled VO", "Finished VO", "Team Match"],
#     'f': ["Offer", "Rejected"]
# }


# def get_connection():
#     os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
#     conn = sqlite3.connect(DB_PATH)
#     conn.row_factory = sqlite3.Row
#     return conn


# def init_db():
#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS applications (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             company TEXT NOT NULL,
#             title TEXT NOT NULL,
#             location TEXT,
#             status TEXT CHECK(status IN ("Applied", "Received OA", "Finished OA", "Scheduled VO", "Finished VO", "Team Match", "Offer", "Rejected")),
#             notes TEXT,
#             weblink TEXT,
#             applied_date TEXT,
#             important_date TEXT,
#             updated_date TEXT,
#             round_count INTEGER,
#             status_history TEXT
#         )
#     ''')
#     conn.commit()
#     conn.close()


# @click.group()
# def cli():
#     """JobTracker CLI - Track your job applications from the terminal."""
#     init_db()

# @cli.command()
# def add():
#     """Add a new job application interactively."""
#     company = click.prompt("Company", type=str)
#     title = click.prompt("Job Title", type=str)
#     location = click.prompt("Location", default="", show_default=False)
#     notes = click.prompt("Notes", default="", show_default=False)
#     weblink = click.prompt("Web Link", default="", show_default=False)
    
#     important_date = None
#     interview_round = 1

#     status = "Applied"
#     now = datetime.now().isoformat()
#     status_history = json.dumps([status])

#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute('''
#         INSERT INTO applications (company, title, location, status, notes, weblink, applied_date, important_date, updated_date, round_count, status_history)
#         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#     ''', (company, title, location, status, notes, weblink, now, important_date, now, interview_round, status_history))
#     conn.commit()
#     click.echo(f"Applied for {title} at {company}")

# @cli.command()
# @click.option('--id', '-i', type=int, required=False)
# def update(id):
#     if id is not None:
#         update_by_id(id)
#     else:
#         update_by_search()


# def update_by_id(id):
#     """Update application status automatically and optionally update notes."""
#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute('SELECT company, status, round_count, status_history FROM applications WHERE id=?', (id,))
#     row = cursor.fetchone()
#     if not row:
#         click.echo(f"Application not found with ID {id}.")
#         return

#     current_status = row['status']
#     company = row['company']
#     round_count = row['round_count']
#     now = datetime.now().isoformat()
#     new_status = current_status
#     history = json.loads(row['status_history']) if row['status_history'] else [current_status]

#     if current_status == "Applied":
#         new_status = "Received OA"
#     elif current_status == "Received OA":
#         new_status = "Finished OA"
#     elif current_status == "Finished OA":
#         new_status = "Scheduled VO"
#     elif current_status == "Scheduled VO":
#         new_status = "Finished VO"
#         round_count = 1
#     elif current_status == "Finished VO":
#         while True:
#             answer = click.prompt("Are there more interview rounds to come? (y/n)", type=str).strip().lower()
#             if answer == "y":
#                 round_count += 1 
#                 new_status = "Scheduled VO"
#                 break
#             else:
#                 new_status = "Team Match"
#                 break
#     elif current_status == "Team Match":
#         offer = click.prompt("Did you receive an offer? (y/n)", type=str).strip().lower()
#         if offer == "y":
#             new_status = "Offer"
#         else:
#             new_status = "Rejected"
#     elif current_status in ["Offer", "Rejected"]:
#         click.echo("Application is already complete. No further updates.")
#         return
    
#     history.append(new_status)
#     notes = click.prompt("Any notes to be added", default="", show_default=False)
    
#     # Update the status and optionally notes
#     cursor.execute('UPDATE applications SET status=?, notes=?, updated_date=?, round_count=?, status_history=? WHERE id=?', (new_status, notes, now, round_count, json.dumps(history), id))
#     conn.commit()
#     click.echo(f"Your Application at {company} has been updated to status '{new_status}'.")

# def update_by_search():
#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute('SELECT id, company, title, status, applied_date FROM applications')
#     apps = cursor.fetchall()
#     if not apps:
#         return
#     choices = [
#         {
#             "name": f"[{row['id']}] {row['company']} | {row['title']} | {row['status']} | {row['applied_date']}",
#             "value": row['id']
#         }
#         for row in apps
#     ]
#     selected_id = inquirer.fuzzy(
#         message="Search by company name:",
#         choices = choices,
#         multiselect=False,
#         validate=lambda x: x is not None,
#     ).execute()
#     update_by_id(selected_id)

# def render_progress_bar(completed_statuses):
#     current_status = completed_statuses[-1] if completed_statuses else ""
#     is_finalized = current_status in ["Offer", "Rejected"]
    
#     bar_color = {
#         True: "green" if current_status == "Offer" else "red"
#     }.get(is_finalized, "dark_slate_gray1")

#     marker_color = {
#         True: "green" if current_status == "Offer" else "red"
#     }.get(is_finalized, "blue")

#     # Label row
#     label_row = ""
#     for stage in completed_statuses:
#         pad = SEGMENT_WIDTH - len(stage)
#         label_row += stage + (" " * pad)

#     # Progress line
#     progress_line = Text()
#     progress_line.append("+", style=marker_color)

#     for _ in range(1, len(completed_statuses)):
#         progress_line.append("===============", style=bar_color)
#         progress_line.append("+", style=marker_color)

#     return label_row.strip(), progress_line

# @cli.command()
# @click.option('--stage', '-s', type=click.Choice(['a', 'o', 'v', 'f']), default=None)
# def list(stage):
#     """Show all applications or filter by stage."""
#     conn = get_connection()
#     cursor = conn.cursor()

#     if stage:
#         filters = STAGE_MAP[stage]
#         placeholders = ','.join('?' * len(filters))
#         cursor.execute(f"SELECT * FROM applications WHERE status IN ({placeholders})", filters)
#     else:
#         cursor.execute("SELECT * FROM applications")

#     rows = cursor.fetchall()
#     if not rows:
#         console.print("No applications found.", style="bold red")
#         return

#     for row in rows:
#         company_line = f"{row['company']} {row['title']} {row['location']} {row['applied_date'][:10]}"
#         console.print(company_line, style="bold white")

#         completed_statuses = json.loads(row['status_history']) if row['status_history'] else [row['status']]
#         label_row, progress_line = render_progress_bar(completed_statuses)
#         console.print(label_row)
#         console.print(progress_line)


# @cli.command()
# @click.option('--id', '-i', type=int, required=True)
# def delete(id):
#     """Delete a job application by ID."""
#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM applications WHERE id=?', (id,))
#     row = cursor.fetchone()
#     if not row:
#         click.echo(f"No application found with ID {id}.")
#         return

#     cursor.execute('DELETE FROM applications WHERE id=?', (id,))
#     conn.commit()
#     click.echo(f"Deleted application ID {id}.")

# # @cli.command()
# # @click.option('--status', type=click.Choice(STATUS_CHOICES), default=None)
# # def list(status):
# #     """List all job applications, optionally filtered by status."""
# #     conn = get_connection()
# #     cursor = conn.cursor()
# #     if status:
# #         cursor.execute('SELECT * FROM applications WHERE status=?', (status,))
# #     else:
# #         cursor.execute('SELECT * FROM applications')
# #     rows = cursor.fetchall()
# #     if not rows:
# #         click.echo("📭 No job applications found.")
# #         return
# #     for row in rows:
# #         click.echo(f"[{row['id']}] {row['title']} at {row['company']} - {row['status']} (Applied: {row['applied_date']})")


# if __name__ == '__main__':
#     cli()