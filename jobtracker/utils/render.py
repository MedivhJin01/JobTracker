from rich.text import Text

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
    label_row = "    "
    for stage in completed_statuses:
        pad = SEGMENT_WIDTH - len(stage)
        label_row += stage + (" " * pad)

    # Progress line
    progress_line = Text("    ")
    progress_line.append("+", style=marker_color)

    for _ in range(1, len(completed_statuses)):
        progress_line.append("===============", style=bar_color)
        progress_line.append("+", style=marker_color)

    return label_row, progress_line