# config.example.py

# GitHub
GITHUB_USERNAME = "your-username"
GITHUB_REPO = "your-repo"
GITHUB_TOKEN = "your-token"
START_DATE = "YYYY-MM-DD" # start date for commit history
END_DATE = "YYYY-MM-DD"  # end date for commit history

# ClickUp
CLICKUP_API_TOKEN = "your-token"
CLICKUP_LIST_IDS = ["your-list-id"]

# Google Sheets
GOOGLE_API_SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

GOOGLE_SHEET_NAME = None  # Optional override
