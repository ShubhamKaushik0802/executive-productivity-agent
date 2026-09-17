from pydantic import BaseModel, Field
from typing import List, Optional


class Source(BaseModel):
    source_id: str
    source_type: str
    date: str
    title: str
    speaker_or_sender: str
    excerpt: str


class Task(BaseModel):
    task_id: str
    title: str
    action_owner: Optional[str] = None
    stakeholder: Optional[str] = None
    waiting_on: Optional[str] = None
    deadline: Optional[str] = None
    deadline_label: Optional[str] = None
    deadline_history: List[str] = Field(default_factory=list)
    dependency_ready_at: Optional[str] = None
    completed_at: Optional[str] = None
    priority: str = "Medium"
    commitment_type: str = "Action"
    source_ids: List[str] = Field(default_factory=list)
    confidence: float = 0.9
    notes: Optional[str] = None
    reconciliation: Optional[str] = None
