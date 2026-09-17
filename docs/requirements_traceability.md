# Requirement Traceability

**Candidate: Shubham Kaushik**

| Assignment requirement | Where demonstrated |
|---|---|
| Identify commitments made by executive | `src/task_engine.py` canonical reconciliation + Task Register |
| Separate “my actions” from “waiting on others” | `status_for()` + Daily Executive Brief |
| Detect deadlines and overdue items | `deadline_status()` + brief metrics |
| Deduplicate same action across sources | Canonical TASK-IDs with merged source IDs |
| Flag unclear ownership rather than invent it | TASK-005 owner remains `None` / `UNKNOWN` |
| Produce a daily brief | `src/brief.py` + Overview tab |
| Ask natural-language questions | `src/qa.py` + Ask the Agent tab |
| Architecture / process flow | `docs/architecture.md` + `screenshots/architecture.png` |
| Inputs / sources / assumptions | `docs/assumptions.md` + Source tab |
| AI tools used and how | `docs/ai_tools.md` |
| 15-minute demo and defence | `docs/demo_script.md` + `docs/defence_qna.md` |
| Demo video on Drive | Placeholder included in PPT; upload your recording and paste URL |
| GitHub link | Placeholder included in PPT; push this project root and paste URL |
| 10-slide PPT | `Executive_Productivity_Agent_10_Slide_PPT.pptx` |
