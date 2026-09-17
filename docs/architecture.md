# Architecture & Process Flow

**Candidate: Shubham Kaushik**

## System view

```text
┌─────────────────────────────────────────────────────┐
│                 SUPPLIED DATA PACK                  │
│ Meeting · 25 Emails · Calendar · 2 Voice Notes    │
└──────────────────────────┬──────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────┐
│ 1. OBSERVE / NORMALIZE                              │
│ Common source schema: id, type, date, sender, text │
└──────────────────────────┬──────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────┐
│ 2. EXTRACT                                          │
│ Action · owner · stakeholder · deadline · evidence │
│ Optional LLM layer for semantic extraction         │
└──────────────────────────┬──────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────┐
│ 3. RECONCILE / DEDUPLICATE                         │
│ Related mentions → one canonical TASK-ID           │
│ Preserve all supporting source IDs                  │
└──────────────────────────┬──────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────┐
│ 4. DETERMINISTIC AGENT RULES                       │
│ Explicit owner only · latest deadline · completion │
│ dependency readiness · ambiguity guardrail         │
└──────────────────────────┬──────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────┐
│ 5. OUTPUT                                           │
│ Daily Brief · Task Register · Q&A · Audit Trail    │
└─────────────────────────────────────────────────────┘
```

## Why this is safer than an LLM-only workflow

The Mumbai lease case makes the risk concrete: Facilities is mentioned, but responsibility is not confirmed. The application therefore never converts a plausible interpretation into a fact.

Likewise, the Q3 campaign review has a changing deadline. The system keeps the old target as history and treats the later explicit 9:30 AM Thursday commitment as the active timing.

## Component responsibilities

| Component | Responsibility |
|---|---|
| `data_loader.py` | Load the normalized source pack and source map |
| `task_engine.py` | Reconcile canonical tasks and calculate status |
| `brief.py` | Group tasks for the daily brief |
| `qa.py` | Answer source-grounded questions and return evidence IDs |
| `ai_agent.py` | Optional LLM-based extraction layer |
| `app.py` | Streamlit presentation and reviewer controls |
| `tests/` | Regression coverage for key edge cases |
