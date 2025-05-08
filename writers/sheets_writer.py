import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from config import GOOGLE_API_SCOPE

def write_to_google_sheets(tasks, notes, sheet_name="PM Weekly Report"):
    scope = GOOGLE_API_SCOPE
    creds = ServiceAccountCredentials.from_json_keyfile_name("gcp_credentials.json", scope)
    client = gspread.authorize(creds)

    now = datetime.now()
    year = now.strftime("%Y")
    tab_name = now.strftime("%B %Y")
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")

    if not sheet_name:
        sheet_name = f"PM Reports {year}"

    try:
        spreadsheet = client.open(sheet_name)
    except gspread.SpreadsheetNotFound:
        print(f"⚠️ Spreadsheet '{sheet_name}' not found. Please create it and share with your service account.")
        return

    try:
        sheet = spreadsheet.worksheet(tab_name)
    except gspread.WorksheetNotFound:
        print(f"➕ Creating new tab: {tab_name}")
        sheet = spreadsheet.add_worksheet(title=tab_name, rows="1000", cols="5")

    all_rows = sheet.col_values(1)
    existing_dates = [
        all_rows[i + 1]
        for i, val in enumerate(all_rows)
        if val.strip() == "📌 Generated On" and i + 1 < len(all_rows)
    ]

    if current_time in existing_dates:
        print("⚠️ Duplicate entry detected. Skipping write.")
        return

    # === Write report ===
    sheet.append_row(["------------------------------------------------------------"])
    sheet.append_row(["📌 Generated On", current_time])
    sheet.append_row(["------------------------------------------------------------"])

    sheet.append_row(["MEETING NOTES"])

    def write_section(title, emoji, key, empty_msg):
        sheet.append_row([f"{emoji} {title}"])
        if notes.get(key):
            for line in notes[key]:
                sheet.append_row(["- " + line])
        else:
            sheet.append_row([f"*{empty_msg}*"])
        sheet.append_row([""])

    write_section("Key Decisions", "📌", "decisions", "No decisions recorded for this period.")
    write_section("Blockers / Risks", "🚧", "blockers", "No blockers or risks recorded this week.")
    write_section("Action Items", "✅", "actions", "No action items this week.")
    write_section("Learnings", "", "learnings", "No learnings captured.")
    write_section("Highlights", "", "highlights", "No highlights this week.")
    write_section("Agreements", "", "agreements", "No agreements documented.")

    sheet.append_row(["-------------------------------------------------------------------------------------------------------"])
    sheet.append_row(["CLICKUP TASKS"])
    sheet.append_row(["STATUS", "TASK NAME"])
    for task in tasks["done"]:
        sheet.append_row(["✅ Done", task])
    for task in tasks["in_progress"]:
        sheet.append_row(["🚧 In Progress", task])
    for task in tasks["blocked"]:
        sheet.append_row(["🔒 Blocked", task])

    sheet.append_row(["--------------------------------------------------------------------------------------------------------"])
    sheet.append_row(["______________________________________________________________"])

    print(f"✅ Google Sheet tab '{tab_name}' updated successfully.")
