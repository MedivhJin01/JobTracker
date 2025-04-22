from InquirerPy import inquirer

def fuzzy_select_app(apps, segment_width=16):
    if not apps:
        return None

    choices = [
        {
            "name": f"{str(row['id'])} {row['company'].ljust(segment_width)} | {row['title'].ljust(segment_width)} | {row['status'].ljust(segment_width)} | {row['applied_date'][:10]}",
            "value": row['id']
        }
        for row in apps
    ]

    selected_id = inquirer.fuzzy(
        message="Search by company name:",
        choices=choices,
        multiselect=False,
        validate=lambda x: x is not None,
    ).execute()

    return selected_id