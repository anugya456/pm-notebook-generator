import re

def parse_meeting_notes(file_path="sample_data/meeting_notes.txt"):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"⚠️ File not found: {file_path}")
        return {"blockers": [], "decisions": []}

    blockers = []
    decisions = []

    for line in lines:
        lowered = line.lower()

        if any(keyword in lowered for keyword in ["blocker", "blocked", "issue", "risk"]):
            blockers.append(line.strip())

        if any(keyword in lowered for keyword in ["decided", "agreement", "approved", "finalize"]):
            decisions.append(line.strip())

    return {
        "blockers": blockers,
        "decisions": decisions
    }
