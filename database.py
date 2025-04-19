import sqlite3
import os
from tabulate import tabulate

DB_PATH = os.path.expanduser("~/.jobtracker/jobtracker.db")

def print_all_applications():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM applications")
    rows = cursor.fetchall()

    if not rows:
        print("No applications found.")
        return

    headers = rows[0].keys()
    data = [tuple(row) for row in rows]

    print(tabulate(data, headers=headers, tablefmt="grid"))

if __name__ == "__main__":
    print_all_applications()