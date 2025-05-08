from datetime import datetime

def generate_markdown_report(commits, notes=None, tasks=None, output_path="weekly_report.md"):
    if notes is None:
        notes = {
            "decisions": [], "blockers": [],
            "actions": [], "learnings": [],
            "highlights": [], "agreements": []
        }
    if tasks is None:
        tasks = {"done": [], "in_progress": [], "blocked": []}

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# Weekly PM Notebook\n\n")
        f.write(f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        # === GitHub Commits ===
        f.write("## ✅ Completed This Week (GitHub)\n\n")
        if commits:
            for commit in commits:
                date = commit["date"][:10]
                message = commit["message"].strip().replace("\n", " ")
                author = commit["author"]
                url = commit["url"]
                f.write(f"- **{date}** | {author}: {message}\n  - [View Commit]({url})\n")
        else:
            f.write("*No new commits for this period.*\n")

        # === Meeting Notes Sections ===
        def write_section(title, emoji, key, empty_msg):
            f.write(f"\n\n## {emoji} {title}\n\n")
            if notes.get(key):
                for item in notes[key]:
                    f.write(f"- {item}\n")
            else:
                f.write(f"*{empty_msg}*\n")

        write_section("Key Decisions", "📌", "decisions", "No decisions recorded for this period.")
        write_section("Blockers / Risks", "🚧", "blockers", "No blockers or risks recorded this week.")
        write_section("Action Items", "✅", "actions", "No action items this week.")
        write_section("Learnings", "🧠", "learnings", "No learnings captured.")
        write_section("Highlights", "🚀", "highlights", "No highlights this week.")
        write_section("Agreements", "🤝", "agreements", "No agreements documented.")

        # === ClickUp Tasks ===
        f.write("\n\n## Task Tracker (ClickUp)\n")
        if any([tasks["done"], tasks["in_progress"], tasks["blocked"]]):
            if tasks["done"]:
                f.write("\n### ✅ Done\n")
                for item in tasks["done"]:
                    f.write(f"- {item}\n")
            if tasks["in_progress"]:
                f.write("\n### 🚧 In Progress\n")
                for item in tasks["in_progress"]:
                    f.write(f"- {item}\n")
            if tasks["blocked"]:
                f.write("\n### 🔒 Blocked\n")
                for item in tasks["blocked"]:
                    f.write(f"- {item}\n")
        else:
            f.write("*No task updates from ClickUp for this period.*\n")

    print(f"\n✅ Report written to: {output_path}")
