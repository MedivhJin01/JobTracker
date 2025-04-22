import click
import json
from InquirerPy import inquirer
from jobtracker.db.queries import get_connection
from rich.console import Console
from jobtracker.utils.render import render_progress_bar

console = Console()
SEGMENT_WIDTH = 15
FUZZY_SEARCH_SEGEMENT_WIDTH = 7

# fuzzy search
# -a list all
# -s stages
# -c companies


STAGE_MAP = {
    'a': ["Applied"],
    'o': ["Received OA", "Finished OA"],
    'v': ["Scheduled VO", "Finished VO", "Team Match"],
    'f': ["Offer", "Rejected"]
}

ORDER_MAP = {
    "Applied": 1,
    "Received OA": 2,
    "Finished OA": 3,
    "Scheduled VO": 4,
    "Finished VO": 5,
    "Team Match": 6,
    "Offer": 100,
    "Rejected": 101
}

@click.command() 

@click.option('--all', '-a', is_flag=True, default=None, help="List all applications")
@click.option('--company', '-c', default=None, help="Filter by company name")
@click.option('--stage', '-s', type=click.Choice(['a', 'o', 'v', 'f']), default=None)
def list_apps(all, company, stage):
    """Show all applications or filter by stage."""
    conn = get_connection()
    cursor = conn.cursor()

    if not any([all, company, stage]):
        cursor.execute("SELECT company FROM applications GROUP BY company")
        result = cursor.fetchall()
        if not result:
            console.print("No companies found.", style="bold red")
            return
        companies = []
        mapping = {}

        for row in result:
            company = row['company']
            cursor.execute("SELECT COUNT(*) FROM applications WHERE company=?", (company,))
            total_count = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM applications WHERE company=? AND status NOT IN ('Offer', 'Rejected')", (company,))
            active_count = cursor.fetchone()[0]

            finalized_count = total_count - active_count
            display = f"{company.ljust(10)} In Progress {str(active_count).ljust(5)} Finalized {str(finalized_count)}"

            companies.append(display)
            mapping[display] = company

        selected_company = inquirer.fuzzy(
            message="Search company to list applications",
            choices=companies
        ).execute()
        company = mapping[selected_company]
    
    query = "SELECT * FROM applications"
    conditions = []
    params = []

    if not all:
        if company:
            conditions.append("company LIKE ?")
            params.append(f"%{company}%")
        if stage:
            filters = STAGE_MAP[stage]
            placeholders = ','.join('?' * len(filters))
            conditions.append(f"status IN ({placeholders})")
            params.extend(filters)
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    if not rows:
        console.print("No applications found.", style="bold red")
        return
    
    def sort_key(row):
        status = row['status']
        base_order = ORDER_MAP.get(status, 0)
        round_count = row['round_count']
        return round_count * base_order
    
    rows.sort(key=sort_key)

    for row in rows:
        company_line = f"{str(row['id']).ljust(3)} {row['company'].ljust(SEGMENT_WIDTH)} {row['title'].ljust(SEGMENT_WIDTH)} {row['location'].ljust(SEGMENT_WIDTH)} {row['applied_date'][:10]}"
        console.print(company_line, style="bold white")

        completed_statuses = json.loads(row['status_history']) if row['status_history'] else [row['status']]
        label_row, progress_line = render_progress_bar(completed_statuses)
        console.print(label_row)
        console.print(progress_line)