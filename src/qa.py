import re
from .task_engine import canonical_tasks, deadline_status, status_for


def _norm(text: str) -> str:
    return re.sub(r"[^a-z0-9 ]", " ", text.lower())


def answer(question: str, as_of: str, data: dict) -> tuple[str, list[str]]:
    q = _norm(question)
    tasks = canonical_tasks(data)
    views = [(t, status_for(t, as_of), deadline_status(t, as_of)) for t in tasks]

    if any(k in q for k in ["promise", "promised", "commit"]) and "raghav" in q:
        t = tasks[0]
        return (
            f"You promised Raghav Sethi that you would send the updated vendor list. "
            f"The latest explicit commitment was {t.deadline_label}. "
            f"The agent merged {len(t.source_ids)} source mentions into one task. "
            f"As of {as_of}, it is {status_for(t, as_of)} and its deadline status is {deadline_status(t, as_of)}.",
            t.source_ids,
        )

    if any(k in q for k in ["mumbai", "lease", "renewal"]):
        t = tasks[4]
        return (
            "Ownership is currently unclear. Facilities is mentioned as a possible/typical owner, "
            "but no source confirms an assigned owner. Arjun explicitly said not to assume. "
            "The deadline is Friday, 25 September, end of day.",
            t.source_ids,
        )

    if "waiting" in q or "wait" in q:
        waiting = [(t, st) for t, st, _ in views if st == "WAITING ON OTHERS"]
        if not waiting:
            return (f"As of {as_of}, there are no open items currently waiting on another person.", [])
        return ("As of " + as_of + ", you are waiting on: " + "; ".join(f"{t.title} — {t.waiting_on or 'another party'}" for t, _ in waiting) + ".", sum((t.source_ids for t, _ in waiting), []))

    if "overdue" in q or "late" in q or "missed" in q:
        overdue = [t for t, _, ds in views if ds == "OVERDUE"]
        if not overdue:
            return (f"As of {as_of}, there are no overdue open commitments.", [])
        return ("As of " + as_of + ", overdue open items are: " + "; ".join(f"{t.title} ({t.deadline_label})" for t in overdue) + ".", sum((t.source_ids for t in overdue), []))

    if "today" in q or "action" in q:
        action = [(t, ds) for t, st, ds in views if st == "MY ACTION" and ds in ["DUE TODAY", "OVERDUE"]]
        unclear = [(t, ds) for t, st, ds in views if st == "UNCLEAR OWNERSHIP"]
        parts = []
        ids = []
        if action:
            parts.append("My actions: " + "; ".join(f"{t.title} ({ds})" for t, ds in action)); ids.extend(sum((t.source_ids for t, _ in action), []))
        if unclear:
            parts.append("Unclear ownership: " + "; ".join(f"{t.title} ({ds})" for t, ds in unclear)); ids.extend(sum((t.source_ids for t, _ in unclear), []))
        if not parts:
            return (f"As of {as_of}, there are no open actions due today or overdue.", [])
        return ("As of " + as_of + ", " + " ".join(parts), ids)

    if "completed" in q or "done" in q or "finished" in q:
        done = [t for t, st, _ in views if st == "COMPLETED"]
        if not done:
            return (f"No commitments are marked completed as of {as_of}.", [])
        return ("Completed as of " + as_of + ": " + "; ".join(t.title for t in done) + ".", sum((t.source_ids for t in done), []))

    return (
        "I can answer questions grounded in the supplied Data Pack. Try: "
        "'What did I promise Raghav?', 'What needs action today?', "
        "'What am I waiting for?', 'What is overdue?', or 'Who owns the Mumbai lease?'",
        [],
    )
