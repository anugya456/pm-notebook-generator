from data_sources.github_fetcher import fetch_commits
from data_sources.notes_parser import parse_meeting_notes
from data_sources.clickup_fetcher import (
    fetch_tasks_from_list,
    fetch_tasks_from_csv
)
from writers.report_writer import generate_markdown_report
from writers.sheets_writer import write_to_google_sheets
from writers.emailer import send_email
from config import (
    CLICKUP_LIST_IDS,
    GOOGLE_SHEET_NAME
)

def main():
    print("Fetching GitHub commits...\n")
    commits = fetch_commits()
    if not commits:
        print("No commits found.")
    else:
        print(f"Found {len(commits)} commits.")

    print("\n\U0001F4DD Parsing meeting notes...")
    notes = parse_meeting_notes()

    print("\n\U0001F4CC Key Decisions:")
    for d in notes["decisions"]:
        print(f"- {d}")

    print("\n\U0001F6A7 Blockers / Risks:")
    for b in notes["blockers"]:
        print(f"- {b}")

    # === Step 3: Try ClickUp API, fallback to CSV if not
    print("\nFetching ClickUp tasks from multiple lists...\n")
    tasks = {"done": [], "in_progress": [], "blocked": []}

    for list_id in CLICKUP_LIST_IDS:
        print(f"Fetching from ClickUp list: {list_id}")
        result = fetch_tasks_from_list(list_id)
        tasks["done"].extend(result["done"])
        tasks["in_progress"].extend(result["in_progress"])
        tasks["blocked"].extend(result["blocked"])

    total = len(tasks["done"]) + len(tasks["in_progress"]) + len(tasks["blocked"])

    if total == 0:
        print("⚠️ API returned no tasks — switching to CSV fallback...")
        tasks = fetch_tasks_from_csv()
    else:
        print(f"\n✅ Combined ClickUp Tasks: {len(tasks['done'])} done, {len(tasks['in_progress'])} in progress, {len(tasks['blocked'])} blocked.")

    print("\nGenerating report...")
    generate_markdown_report(commits, notes, tasks)
    write_to_google_sheets(tasks, sheet_name=GOOGLE_SHEET_NAME)
    send_email()

if __name__ == "__main__":
    main()
