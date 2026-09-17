# Executive Productivity Agent

**Candidate:** Shubham Kaushik  
**Assignment:** 1 — Executive Productivity Agent  
**Executive:** Arjun Malhotra, VP Sales  
**Scenario week:** 21–25 September 2026

## 1. What this project does

This prototype converts a messy executive workstream into a daily action brief. It reconciles meeting statements, email threads, calendar timing, and personal voice notes into a small set of canonical tasks, while keeping an evidence trail for every decision.

### Required capabilities covered

- Identify commitments made by the executive
- Separate **My Actions** from **Waiting on Others**
- Detect deadlines, due-today items and overdue items
- Deduplicate repeated mentions across sources
- Flag unclear ownership instead of inventing it
- Produce a daily executive brief
- Answer natural-language questions
- Show the source evidence behind the answer
- Maintain a simple audit/reconciliation trail

## 2. Why the design is intentionally hybrid

The project separates semantic extraction from business-critical status logic.

```text
SOURCE PACK
  ↓
Observe / Normalize
  ↓
Extract commitments + entities + time language
  ↓
Reconcile / Deduplicate
  ↓
Deterministic guardrails
  ├─ explicit owner only
  ├─ latest explicit deadline
  ├─ completion evidence
  └─ dependency readiness
  ↓
Daily brief + Q&A + audit trail
```

An optional OpenAI extraction function is included in `src/ai_agent.py`. The baseline demo does not require an API key, so the reviewer can run the project deterministically.

## 3. Source-grounded task outcomes

### TASK-001 — Vendor list
Arjun committed to sending the updated vendor list to Raghav. The deadline moved over the email sequence and the latest explicit promise was Wednesday morning. Multiple sources are merged into one canonical task.

### TASK-002 — Q3 campaign deck
The original Wednesday review was moved to Thursday morning; the email confirms **Thursday 9:30 AM**, and the calendar corroborates a 9:30 review. The earlier target remains in the deadline history rather than being presented as current.

### TASK-003 — Expense variance report
The dependency was with Divya until the report arrived Wednesday evening. Arjun then acknowledged receipt. The task therefore changes from **Waiting on Others** to **Completed**.

### TASK-004 — Meridian Logistics call
Arjun proposed Wednesday 3:00 PM, Priya confirmed, and Arjun reconfirmed. The messages and calendar are treated as evidence of one commitment rather than multiple tasks.

### TASK-005 — Mumbai lease renewal
The required signature is due Friday end of day, but no source confirms the responsible owner. Facilities is mentioned as a possible/typical owner, while Arjun explicitly said to **flag it, not assume**. The agent therefore keeps the owner as **UNKNOWN**.

## 4. Run locally

### Prerequisites

Python 3.10+ is recommended.

### Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Or use the included launcher:

```bash
./run.sh
```

## 5. Zero-dependency demo fallback

Open `demo.html` directly in a browser. It contains the same core task states and Q&A examples and is useful for a quick evaluator walkthrough when Python packages are unavailable.

## 6. Demo script

1. Set the date to **24 Sep 2026**.
2. Show the vendor list as overdue.
3. Show the campaign deck review as a due-today action at 9:30 AM.
4. Show the Mumbai lease as **OWNER UNKNOWN**.
5. Ask `What did I promise Raghav?`.
6. Ask `Who owns the Mumbai lease?`.
7. Move the date to **22 Sep 2026** and show the campaign-deck / expense-report dependency state.
8. Open **Sources & Evidence** and show how one task links to multiple mentions.

Full defence script: `docs/demo_script.md`.

## 7. Repository structure

```text
.
├── app.py
├── demo.html
├── requirements.txt
├── run.sh
├── .env.example
├── data/
│   ├── datapack.json
│   └── Assignment 1_DataPack_ExecutiveProductivityAgent.pdf
├── src/
│   ├── ai_agent.py
│   ├── brief.py
│   ├── data_loader.py
│   ├── models.py
│   ├── qa.py
│   └── task_engine.py
├── prompts/
├── tests/
└── docs/
```

## 8. Testing

```bash
python3 -m unittest discover -s tests -v
```

The tests cover canonical task count, deduplication, overdue logic, dependency transitions, completion, and the unresolved-ownership case.

## 9. AI tools used

**ChatGPT:** architecture ideation, implementation assistance, test design, documentation and presentation drafting.  
**Optional OpenAI API:** structured extraction from raw source text in `src/ai_agent.py` when an API key is supplied.

The baseline application does not depend on the external API.

## 10. Assumptions and guardrails

- The selected UI date is treated as “today” for the brief.
- A task with no confirmed owner remains **UNKNOWN**.
- “Typically sits with Facilities” is not treated as an assignment.
- A later explicit deadline supersedes an earlier target but the earlier target remains in history.
- Calendar timing can corroborate a commitment but should not create a duplicate action.
- Personal voice notes are treated as Arjun's own source of commitments/open items.
- No external facts are needed for the demo.

Full details: `docs/assumptions.md`.

## 11. Submission checklist

- [x] Working agent / clickable prototype
- [x] Architecture and process flow
- [x] Inputs, sources and assumptions
- [x] AI tools and how they were used
- [x] Demo + defence script
- [x] 10-slide PPT
- [ ] Add final GitHub URL to slide 10
- [ ] Add final Google Drive video URL to slide 10

### Candidate
**Shubham Kaushik**
