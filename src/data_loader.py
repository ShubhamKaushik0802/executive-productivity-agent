from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any
import fitz

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_JSON = ROOT / "data" / "datapack.json"
DEFAULT_PDF = ROOT / "data" / "Assignment 1_DataPack_ExecutiveProductivityAgent.pdf"


def load_data(path: str | Path = DEFAULT_JSON) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_pdf_text(path: str | Path = DEFAULT_PDF) -> str:
    path = Path(path)
    if not path.exists():
        return ""
    doc = fitz.open(path)
    try:
        return "\n".join(page.get_text() for page in doc)
    finally:
        doc.close()


def source_map(data: Dict[str, Any]):
    return {s["source_id"]: s for s in data["sources"]}


def pack_health(data: Dict[str, Any]) -> dict:
    sources = data["sources"]
    return {
        "source_items": len(sources),
        "meetings": sum(1 for s in sources if s["source_type"] == "Meeting"),
        "emails": sum(1 for s in sources if s["source_type"] == "Email"),
        "voice_notes": sum(1 for s in sources if s["source_type"] == "Voice Note"),
        "calendar_events": len(data.get("calendar", [])),
        "week": f'{data["metadata"]["week_start"]} → {data["metadata"]["week_end"]}',
    }
