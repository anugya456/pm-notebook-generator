import requests
from config import GITHUB_TOKEN, REPO_NAME, START_DATE, END_DATE

def fetch_commits():
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    url = f"https://api.github.com/repos/{REPO_NAME}/commits"
    params = {
        "since": f"{START_DATE}T00:00:00Z",
        "until": f"{END_DATE}T23:59:59Z"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        commits = response.json()
        return [
            {
                "sha": commit["sha"],
                "author": commit["commit"]["author"]["name"],
                "date": commit["commit"]["author"]["date"],
                "message": commit["commit"]["message"],
                "url": commit["html_url"]
            }
            for commit in commits
        ]
    else:
        print("Failed to fetch commits:", response.status_code, response.text)
        return []