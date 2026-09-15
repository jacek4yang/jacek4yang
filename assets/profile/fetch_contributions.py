# Fetch the user's contribution data from the GitHub GraphQL API and save it
# as assets/profile/contributions.json for the profile SVG generator.
#
# Usage: gh auth token must be available; run from repo root:
#   python assets/profile/fetch_contributions.py
import json
import os
import subprocess
import sys
from datetime import date, timedelta

LOGIN = os.environ.get("GH_LOGIN", "jacek4yang")

QUERY = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
      totalPullRequestReviewContributions
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            contributionCount
            date
          }
        }
      }
    }
  }
}
"""

def main() -> None:
    today = date.today()
    # GitHub needs the range to start on a Sunday; go back a full year + padding
    start = today - timedelta(days=370)
    out = subprocess.run(
        [
            "gh", "api", "graphql",
            "-f", f"query={QUERY}",
            "-f", f"login={LOGIN}",
            "-F", f"from={start.isoformat()}T00:00:00Z",
            "-F", f"to={today.isoformat()}T23:59:59Z",
        ],
        capture_output=True, text=True, encoding="utf-8", check=True,
    )
    payload = json.loads(out.stdout)
    coll = payload["data"]["user"]["contributionsCollection"]

    calendar = coll["contributionCalendar"]
    days = []
    for week in calendar["weeks"]:
        for d in week["contributionDays"]:
            days.append({"date": d["date"], "count": d["contributionCount"]})
    days.sort(key=lambda d: d["date"])

    # best streak
    streak = best = 0
    for d in days:
        streak = streak + 1 if d["count"] > 0 else 0
        best = max(best, streak)

    active = sum(1 for d in days if d["count"] > 0)
    max_day = max((d["count"] for d in days), default=0)

    data = {
        "login": LOGIN,
        "generated_at": f"{today.isoformat()}",
        "total": calendar["totalContributions"],
        "commits": coll["totalCommitContributions"],
        "prs": coll["totalPullRequestContributions"],
        "issues": coll["totalIssueContributions"],
        "reviews": coll["totalPullRequestReviewContributions"],
        "active_days": active,
        "best_streak": best,
        "max_day": max_day,
        "days": days,
    }
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "contributions.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=1)
    print(f"fetched {len(days)} days, total={data['total']}, streak={best}, active={active}")


if __name__ == "__main__":
    sys.exit(main())
