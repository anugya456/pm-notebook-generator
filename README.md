# pm-notebook-generator

**Automated weekly reporting tool for project managers and product teams.**

This tool fetches GitHub commits, parses meeting notes, pulls ClickUp tasks, and generates a clean weekly project report — published to Google Sheets and emailed to you automatically.

---

## Features

- ✅ GitHub commit summary by author/date
- ✅ Meeting note parser for decisions & blockers
- ✅ ClickUp integration (API + CSV fallback)
- ✅ Google Sheets output (monthly tab per report)
- ✅ Email notifications with Markdown attachment
- ✅ Windows Task Scheduler–ready (automated runs)

---

## Example Output

- [Markdown Example ›](sample_output/weekly_report_example.md)
- [Google Sheet Screenshot ›](sample_output/sheets_example.png)

---

## How It Works

1. **Input sources:**
   - GitHub API
   - Meeting notes (markdown)
   - ClickUp API or CSV fallback

2. **Process:**
   - Parses inputs
   - Formats weekly summary
   - Writes to Google Sheet tab (e.g., `May 2025`)
   - Sends email with Markdown report

3. **Automation:**
   - `.bat` script included
   - Runs weekly via Windows Task Scheduler

---

## Tech Stack

- Python 3.11
- `gspread`, `dotenv`, `requests`, `smtplib`
- Google Sheets API + Gmail App Password
- ClickUp API
- Markdown and CSV parsing

---

## Setup

1. Clone the repo
2. Install dependencies:  
   ```bash
   pip install -r requirements.txt
Add your .env:

ini
Copy
Edit
EMAIL_FROM=you@gmail.com
EMAIL_PASSWORD=xxxx
EMAIL_TO=you@gmail.com
Add gcp_credentials.json from Google Cloud Console

Run the tool:

bash
Copy
Edit
python main.py
