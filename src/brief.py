from .task_engine import task_views


def make_brief(data, as_of: str):
    rows = task_views(data, as_of)
    return {
        "today": [r for r in rows if r["status"] == "MY ACTION" and r["deadline_status"] == "DUE TODAY"],
        "overdue": [r for r in rows if r["deadline_status"] == "OVERDUE"],
        "waiting": [r for r in rows if r["status"] == "WAITING ON OTHERS"],
        "unclear": [r for r in rows if r["status"] == "UNCLEAR OWNERSHIP"],
        "completed": [r for r in rows if r["status"] == "COMPLETED"],
        "upcoming": [r for r in rows if r["deadline_status"] == "UPCOMING" and r["status"] != "UNCLEAR OWNERSHIP"],
        "all": rows,
    }
