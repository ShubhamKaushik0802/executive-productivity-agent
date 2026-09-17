# 15-Minute Demo & Defence Script

**Candidate: Shubham Kaushik**

## 0:00–1:00 — Problem

“An executive does not have a single source of truth. A commitment can appear in a meeting, change over email, be reinforced by a voice note, and have its timing corroborated by a calendar. The challenge is turning that mess into one reliable action view without inventing missing information.”

## 1:00–2:30 — Architecture

Walk through:

**Observe → Extract → Reconcile → Guardrails → Brief/Q&A → Evidence**

Emphasize the hybrid design: AI is useful for meaning extraction, but deterministic rules protect ownership, deadline and completion states.

## 2:30–6:00 — Main demo

Set the brief date to **24 Sep 2026**.

1. Vendor list appears overdue.
2. Q3 campaign deck is a due-today action at 9:30 AM.
3. Mumbai lease appears as **OWNER UNKNOWN**.
4. Expense report and Meridian call appear as completed.

## 6:00–9:00 — Q&A

Ask:

**“What did I promise Raghav?”**

Expected: one vendor-list commitment, latest Wednesday-morning deadline, merged evidence.

Ask:

**“Who owns the Mumbai lease?”**

Expected: ownership is unclear. Facilities is mentioned as a possible/typical owner, not a confirmed assignment.

Ask:

**“What am I waiting for?”**

Change the date to 22 Sep 2026 first so the dependency state can be shown.

## 9:00–11:30 — Edge cases

### Edge case 1: repeated task
Vendor list appears in meeting + 5 emails + voice note. The agent keeps one TASK-001 with all source IDs.

### Edge case 2: changing deadline
Campaign deck starts as Wednesday, then moves to Thursday, then 9:30 AM is confirmed. The history is retained; the latest explicit commitment is active.

### Edge case 3: unclear ownership
Mumbai lease is intentionally not assigned to Facilities.

## 11:30–13:30 — Engineering choices

- Pydantic: structured task records.
- Streamlit: fast reviewer-accessible UI.
- PyMuPDF: supplied PDF can be read locally.
- Optional OpenAI extraction: semantic parsing when an API key is present.
- Deterministic task engine: auditable status calculations.
- Unit tests: protect edge cases.

## 13:30–15:00 — Closing

“The important part is not just extracting a task. It is preserving the executive's latest intent, collapsing duplicate mentions, separating action from dependency, and surfacing ambiguity instead of turning it into a false fact.”

## Likely defence questions

**Why not let the LLM decide the owner?**  
Because the source contains an explicit ownership ambiguity. A deterministic guardrail prevents a plausible guess from becoming a false assignment.

**How do you handle revised deadlines?**  
The latest explicit commitment becomes the active deadline; previous commitments remain in the audit history.

**How do you prevent duplicates?**  
Related mentions are reconciled under one canonical TASK-ID and retain all supporting source IDs.

**How would you productionize it?**  
Replace the local source pack with connectors for email/calendar/chat, store canonical tasks in a database, add authentication and approval controls, and preserve evidence for every agent action.
