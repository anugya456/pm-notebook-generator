# PM Notebook Generator

**Automated weekly reporting tool for project managers and product teams.**

This tool fetches GitHub commits, parses meeting notes, pulls ClickUp tasks, and generates a clean, organized weekly project report — published to Google Sheets and emailed to you automatically.

---

## Features

- GitHub commit summary by author and date
- Google Docs integration for weekly meeting notes
- Parses: decisions, blockers, action items, learnings, highlights, agreements
- ClickUp task sync via API (CSV fallback optional)
- Google Sheets reporting (monthly/quarterly tabs)
- Email notifications with Markdown report attached
- Compatible with Windows Task Scheduler for full automation


---

## Example Output

- [Markdown Example ›](sample_output/weekly_report_example.md)
- [Google Sheet Screenshot ›](sample_output/sheets_example.png)

---

## How It Works

### Inputs

- GitHub commits via API
- Meeting notes from Google Docs (title: `PM Notes - May 2025`)
- ClickUp tasks via API or CSV

### Process

1. Collects updates from all sources
2. Extracts structured insights: Decisions, Blockers, Action Items, Learnings, Highlights, Agreements
3. Writes the summary to Google Sheets (by month)
4. Sends the same report as a Markdown email attachment

### Automation

- Included `.bat` script to run via Windows Task Scheduler
- Designed for weekly cadence (e.g., every Monday 10:00 AM)


---

## Tech Stack

- **Python 3.11**
- `gspread`, `requests`, `smtplib`, `dotenv`
- Google Sheets API + Gmail App Password
- ClickUp REST API
- Markdown/CSV parsing

---

## Setup

### 1. Clone this repo
git clone https://github.com/anugya456/pm-notebook-generator.git
cd pm-notebook-generator

### 2. Install dependencies
pip install -r requirements.txt

### 3. Add credentials
Create a .env file with:
```env
EMAIL_FROM=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_TO=your_email@gmail.com

GITHUB_USERNAME=your_github_username
GITHUB_REPO=your_repo_name
GITHUB_TOKEN=your_github_token

CLICKUP_API_TOKEN=your_clickup_token
```

Place gcp_credentials.json from Google Cloud Console into the root folder.

### 4. Configure config.py
Do not commit config.py — use config.example.py as a template.

### 5. Run the tool
python main.py

## Why This Exists
Most PMs manually track updates every week. This tool automates that — pulling real activity and packaging it into a readable format you can use in standups, reviews, or executive reports.

## Author
Built by Anugya, a tech-savvy PM with dev roots — passionate about automating grunt work and focusing on what matters: people, progress, and shipping.

## Contact
Found this useful? [Connect on LinkedIn](https://www.linkedin.com/in/fnu-anugya/) or drop a ⭐ on GitHub!
