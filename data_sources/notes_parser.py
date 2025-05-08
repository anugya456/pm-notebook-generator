import os
import re
from datetime import datetime
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from config import (
    CREDS_FILE,
    GOOGLE_DOCS_SCOPES,
    USE_REMOTE_NOTES
)

def get_google_doc_text():
    creds = Credentials.from_service_account_file(CREDS_FILE, scopes=GOOGLE_DOCS_SCOPES)
    drive_service = build("drive", "v3", credentials=creds)
    docs_service = build("docs", "v1", credentials=creds)

    month_year = datetime.now().strftime("%B %Y")
    doc_title = f"PM Notes - {month_year}"

    query = (
        f"name='{doc_title}' and "
        "mimeType='application/vnd.google-apps.document' and "
        "trashed=false"
    )

    results = drive_service.files().list(q=query, spaces='drive', fields="files(id, name)").execute()
    items = results.get("files", [])

    if items:
        doc_id = items[0]["id"]
        doc = docs_service.documents().get(documentId=doc_id).execute()

        lines = []
        for content_block in doc.get("body", {}).get("content", []):
            paragraph = content_block.get("paragraph")
            if not paragraph:
                continue

            full_line = ""
            for elem in paragraph.get("elements", []):
                text_run = elem.get("textRun", {}).get("content", "")
                full_line += text_run

            if full_line.strip():
                lines.append(full_line.strip())

        joined = "\n".join(lines)
        print(f"✅ Pulled notes from Google Doc: {doc_title}")
        return joined
    else:
        print(f"⚠️ Google Doc '{doc_title}' not found. Falling back to local notes.")
        return ""

def parse_meeting_notes():
    if USE_REMOTE_NOTES:
        raw_text = get_google_doc_text()
    else:
        raw_text = ""

    if not raw_text:
        fallback_file = next((f for f in os.listdir(".") if f.endswith(".md") or f.endswith(".txt")), None)
        raw_text = open(fallback_file, "r", encoding="utf-8").read() if fallback_file else ""

    # Normalize all lines
    lines = [
        re.sub(r"^[\-\u2022\*\s]+", "", line.strip())
        for line in raw_text.splitlines()
        if line.strip()
    ]

    print("🔍 DEBUG: Cleaned note lines from Google Doc:")
    for line in lines:
        print(f" - {line}")

    # Extract structured categories
    def extract(tag):
        return [re.sub(rf"(?i)^{tag}:\s*", "", line) for line in lines if re.match(rf"(?i)^{tag}:\s*", line)]

    return {
        "decisions": extract("decision"),
        "blockers": extract("blocker"),
        "actions": extract("action(?: item)?"),
        "learnings": extract("learning"),
        "highlights": extract("highlight"),
        "agreements": extract("agreement")
    }
