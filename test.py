# print("\u001b[31m Applied         Scheduled OA    Finished OA     Scheduled VO    Finished VO     Team Match      Offer\u001b[0m")
# print("\u001b[34m .---------------.---------------.---------------.---------------.---------------.---------------.\u001b[34m")

import click
import sqlite3
import os
from datetime import datetime
from InquirerPy import inquirer
from rich.console import Console
from rich.text import Text
from rich.style import Style

console = Console()
SEGMENT_WIDTH = 16


def render_progress_bar(completed_statuses):
    current_status = completed_statuses[-1] if completed_statuses else ""
    is_finalized = current_status in ["Offer", "Rejected"]
    
    bar_color = {
        True: "green" if current_status == "Offer" else "red"
    }.get(is_finalized, "dark_slate_gray1")

    marker_color = {
        True: "green" if current_status == "Offer" else "red"
    }.get(is_finalized, "blue")

    # Label row
    label_row = ""
    for stage in completed_statuses:
        pad = SEGMENT_WIDTH - len(stage)
        label_row += stage + (" " * pad)

    # Progress line
    progress_line = Text()
    progress_line.append("+", style=marker_color)

    for _ in range(1, len(completed_statuses)):
        progress_line.append("===============", style=bar_color)
        progress_line.append("+", style=marker_color)

    return label_row.strip(), progress_line

job_status = ["Applied", "Received OA", "Finished OA", "Scheduled VO 1", "Finished VO 1", "Scheduled VO 2", "Finished VO 2", "Team Match"]
label_row, progress_line = render_progress_bar(job_status)
console.print(label_row)
console.print(progress_line)

