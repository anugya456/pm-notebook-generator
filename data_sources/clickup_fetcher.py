from config import CLICKUP_TOKEN
import requests
import csv
import os

BASE_URL = "https://api.clickup.com/api/v2"
headers = { "Authorization": CLICKUP_TOKEN }

def list_spaces():
    teams_resp = requests.get(f"{BASE_URL}/team", headers=headers)
    teams = teams_resp.json().get("teams", [])

    for team in teams:
        print(f"Team: {team['name']} (ID: {team['id']})")
        team_id = team['id']

        spaces_resp = requests.get(f"{BASE_URL}/team/{team_id}/space", headers=headers)
        spaces = spaces_resp.json().get("spaces", [])
        for space in spaces:
            print(f"  ↳ Space: {space['name']} (ID: {space['id']})")

def list_lists(space_id):
    folders_resp = requests.get(f"{BASE_URL}/space/{space_id}/folder", headers=headers)
    folders = folders_resp.json().get("folders", [])
    for folder in folders:
        print(f"\nFolder: {folder['name']} (ID: {folder['id']})")
        for lst in folder["lists"]:
            print(f"  ↳ List: {lst['name']} (ID: {lst['id']})")

    uncategorized = requests.get(f"{BASE_URL}/space/{space_id}/list", headers=headers)
    for lst in uncategorized.json().get("lists", []):
        print(f"Unfoldered List: {lst['name']} (ID: {lst['id']})")

def fetch_tasks_from_list(list_id):
    """Fetch tasks from a specific ClickUp List."""
    url = f"{BASE_URL}/list/{list_id}/task"
    params = {
        "archived": "false"
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    done = []
    in_progress = []
    blocked = []

    for task in data.get("tasks", []):
        name = task["name"]
        status = task["status"]["status"].lower()

        if "done" in status or "complete" in status:
            done.append(name)
        elif "progress" in status or "active" in status or "doing" in status:
            in_progress.append(name)
        elif "blocked" in status or "stuck" in status:
            blocked.append(name)

    return {
        "done": done,
        "in_progress": in_progress,
        "blocked": blocked
    }

def fetch_tasks_from_csv(file_path="sample_data/clickup_tasks.csv"):
    """Load legacy tasks from a CSV file as a fallback."""
    if not os.path.exists(file_path):
        print(f"⚠️ CSV fallback file not found: {file_path}")
        return {"done": [], "in_progress": [], "blocked": []}

    done, in_progress, blocked = [], [], []

    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            task = row["Task"]
            status = row["Status"].lower()

            if "done" in status or "complete" in status:
                done.append(task)
            elif "progress" in status or "in progress" in status or "doing" in status:
                in_progress.append(task)
            elif "blocked" in status or "stuck" in status:
                blocked.append(task)

    return {
        "done": done,
        "in_progress": in_progress,
        "blocked": blocked
    }