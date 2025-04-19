import sqlite3
import os

DB_PATH = os.path.expanduser("~/.jobtracker/jobtracker.db")

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            title TEXT NOT NULL,
            location TEXT,
            status TEXT CHECK(status IN ("Applied", "Received OA", "Finished OA", "Scheduled VO", "Finished VO", "Team Match", "Offer", "Rejected")),
            notes TEXT,
            weblink TEXT,
            applied_date TEXT,
            important_date TEXT,
            updated_date TEXT,
            round_count INTEGER,
            status_history TEXT
        )
    ''')
    conn.commit()
    conn.close()