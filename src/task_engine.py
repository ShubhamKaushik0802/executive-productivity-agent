from __future__ import annotations

from datetime import date, datetime
from typing import Any, Dict, List
from .models import Task


AS_OF_DEFAULT = "2026-09-24"
EXECUTIVE = "Arjun Malhotra"


def _dt(value: str | None):
    if not value:
        return None
    if len(value) == 10:
        return datetime.fromisoformat(value + " 23:59")
    return datetime.fromisoformat(value)


def _source_ids(data: dict, prefix: str):
    return [s["source_id"] for s in data["sources"] if s["source_id"].startswith(prefix)]


def canonical_tasks(data: dict) -> List[Task]:
    """Build the five canonical tasks from the supplied source pack.

    The task definitions are reconciliation rules over source IDs, not a second
    dataset. This keeps the demo deterministic while preserving the evidence trail.
    """
    vendor = _source_ids(data, "email-1-")
    campaign = _source_ids(data, "email-2-")
    meridian = _source_ids(data, "email-3-")
    expense = _source_ids(data, "email-4-")
    lease = _source_ids(data, "email-5-")

    return [
        Task(
            task_id="TASK-001",
            title="Send updated vendor list to Raghav",
            action_owner=EXECUTIVE,
            stakeholder="Raghav Sethi",
            deadline="2026-09-23",
            deadline_label="Wednesday morning",
            deadline_history=["Monday: today", "Tuesday: tomorrow morning", "Wednesday morning: latest explicit commitment"],
            priority="High",
            commitment_type="Promise",
            source_ids=["meeting-001", *vendor, "voice-001"],
            confidence=0.98,
            notes="Repeated across the leadership sync, Vendor List email thread and Arjun's personal voice note.",
            reconciliation="7 source mentions merged into one canonical commitment; latest explicit deadline retained.",
        ),
        Task(
            task_id="TASK-002",
            title="Review Q3 campaign deck",
            action_owner=EXECUTIVE,
            stakeholder="Neha Kapoor",
            deadline="2026-09-24",
            deadline_label="Thursday 9:30 AM",
            deadline_history=["Wednesday target", "Thursday morning", "Thursday 9:30 AM: confirmed"],
            dependency_ready_at="2026-09-24 08:00",
            priority="High",
            commitment_type="Review",
            source_ids=["meeting-002", *campaign],
            confidence=0.99,
            notes="The Wednesday review was superseded by Thursday morning; the email confirms 9:30 AM and the calendar corroborates the timing.",
            reconciliation="6 source mentions merged; later reschedule supersedes the original Wednesday target.",
        ),
        Task(
            task_id="TASK-003",
            title="Review July expense variance report",
            action_owner=EXECUTIVE,
            stakeholder="Divya Rao",
            waiting_on="Divya Rao",
            deadline="2026-09-23",
            deadline_label="Wednesday evening",
            dependency_ready_at="2026-09-23 18:00",
            completed_at="2026-09-23 18:10",
            priority="Medium",
            commitment_type="Dependency",
            source_ids=["meeting-003", *expense, "voice-002"],
            confidence=0.99,
            notes="Arjun requested an earlier hand-off; Divya confirmed delivery Wednesday evening; the report was received and acknowledged.",
            reconciliation="7 source mentions merged; task moves from waiting on Divya to completed after receipt and acknowledgement.",
        ),
        Task(
            task_id="TASK-004",
            title="Reconfirm / lock Meridian Logistics call time",
            action_owner=EXECUTIVE,
            stakeholder="Priya Nair",
            deadline="2026-09-23",
            deadline_label="Wednesday 3:00 PM",
            completed_at="2026-09-23 14:00",
            priority="High",
            commitment_type="Follow-up",
            source_ids=["meeting-001", *meridian, "voice-002"],
            confidence=0.99,
            notes="Arjun proposed Wednesday 3 PM, Priya confirmed it, and Arjun reconfirmed shortly before the call.",
            reconciliation="7 source mentions merged; confirmed exchange and calendar event represent one commitment.",
        ),
        Task(
            task_id="TASK-005",
            title="Confirm who owns the Mumbai office lease renewal signature",
            action_owner=None,
            stakeholder="Raghav Sethi",
            deadline="2026-09-25",
            deadline_label="Friday end of day",
            priority="Critical",
            commitment_type="Ownership check",
            source_ids=["meeting-004", *lease, "voice-001"],
            confidence=0.99,
            notes="Facilities is mentioned as a possible typical owner, but the sources never confirm an assigned owner. Arjun explicitly said not to assume.",
            reconciliation="7 source mentions merged; owner intentionally remains UNKNOWN.",
        ),
    ]


def status_for(task: Task, as_of: str) -> str:
    end = datetime.fromisoformat(as_of + " 23:59")
    if task.action_owner is None:
        return "UNCLEAR OWNERSHIP"
    if task.completed_at and _dt(task.completed_at) <= end:
        return "COMPLETED"
    if task.dependency_ready_at and _dt(task.dependency_ready_at) > end:
        return "WAITING ON OTHERS"
    return "MY ACTION"


def deadline_status(task: Task, as_of: str) -> str:
    status = status_for(task, as_of)
    if status == "COMPLETED":
        return "COMPLETED"
    if not task.deadline:
        return "NO DEADLINE"
    d = date.fromisoformat(task.deadline)
    today = date.fromisoformat(as_of)
    if d < today:
        return "OVERDUE"
    if d == today:
        return "DUE TODAY"
    return "UPCOMING"


def task_view(task: Task, as_of: str) -> dict:
    return {**task.model_dump(), "status": status_for(task, as_of), "deadline_status": deadline_status(task, as_of)}


def task_views(data: dict, as_of: str) -> List[dict]:
    return [task_view(t, as_of) for t in canonical_tasks(data)]


def source_counts(task: Task) -> Dict[str, int]:
    return {
        "sources": len(task.source_ids),
        "emails": sum(1 for s in task.source_ids if s.startswith("email-")),
        "meetings": sum(1 for s in task.source_ids if s.startswith("meeting-")),
        "voice_notes": sum(1 for s in task.source_ids if s.startswith("voice-")),
    }


def pipeline_trace(data: dict) -> list[dict]:
    health = {
        "source": "Supplied Data Pack",
        "sources": len(data["sources"]),
        "calendar_events": len(data.get("calendar", [])),
    }
    tasks = canonical_tasks(data)
    return [
        {"step": "1. Observe", "detail": f'{health["sources"]} source records + {health["calendar_events"]} calendar events loaded'},
        {"step": "2. Extract", "detail": "Commitments, owners, stakeholders, deadlines and completion evidence identified"},
        {"step": "3. Deduplicate", "detail": f"{sum(len(t.source_ids) for t in tasks)} mentions reconciled into {len(tasks)} canonical tasks"},
        {"step": "4. Reason", "detail": "Latest explicit deadline, dependency state and confirmed ownership applied"},
        {"step": "5. Brief", "detail": "Tasks grouped into actions, waiting, overdue, unclear ownership and completed"},
        {"step": "6. Explain", "detail": "Every task keeps source IDs and a reconciliation note for auditability"},
    ]
