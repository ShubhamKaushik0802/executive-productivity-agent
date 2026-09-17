from pathlib import Path
import sys
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from src.data_loader import load_data, source_map, pack_health
from src.task_engine import canonical_tasks, task_views, source_counts, pipeline_trace
from src.brief import make_brief
from src.qa import answer
from src.ai_agent import llm_available

st.set_page_config(page_title="Executive Productivity Agent", page_icon="🧭", layout="wide")

CSS = """
<style>
:root { --navy:#102a43; --blue:#1f4e79; --bg:#f5f7fb; --line:#d9e2ec; --muted:#52606d; }
.stApp { background:var(--bg); }
.block-container { padding-top:1rem; padding-bottom:2.5rem; max-width:1380px; }
.hero { background:linear-gradient(135deg,#102a43 0%,#1f4e79 100%); color:#fff; padding:1.45rem 1.65rem; border-radius:18px; margin-bottom:1rem; box-shadow:0 10px 30px rgba(16,42,67,.14); }
.hero h1 { margin:0; font-size:2.1rem; letter-spacing:-.02em; }
.hero p { margin:.35rem 0 0; opacity:.9; }
.card { background:#fff; border:1px solid var(--line); border-radius:15px; padding:1rem; margin:.55rem 0; box-shadow:0 2px 10px rgba(16,42,67,.04); }
.kicker { color:var(--muted); font-size:.82rem; text-transform:uppercase; letter-spacing:.08em; font-weight:700; }
.metric-wrap { background:#fff; border:1px solid var(--line); border-radius:15px; padding:.85rem 1rem; }
.status { display:inline-block; padding:.18rem .55rem; border-radius:999px; font-size:.74rem; font-weight:700; margin-right:.35rem; }
.red { background:#fde8e8; color:#9b1c1c; } .amber { background:#fff4cc; color:#8a5a00; }
.green { background:#e8f7ee; color:#146c43; } .blue { background:#e8f1fb; color:#1d4ed8; }
.small { color:var(--muted); font-size:.86rem; }
.source-chip { display:inline-block; background:#eef2f7; color:#334e68; padding:.2rem .45rem; border-radius:7px; margin:.12rem; font-size:.72rem; }
.trace { border-left:3px solid #1f4e79; padding:.65rem .9rem; margin:.5rem 0; background:#f8fbff; border-radius:0 10px 10px 0; }
.footer { text-align:center; color:#7b8794; font-size:.78rem; padding:1.5rem 0 .2rem; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


@st.cache_data

def get_data():
    return load_data(ROOT / "data" / "datapack.json")


def status_badge(status: str):
    cls = {
        "MY ACTION": "blue",
        "WAITING ON OTHERS": "amber",
        "UNCLEAR OWNERSHIP": "red",
        "COMPLETED": "green",
    }.get(status, "blue")
    return f'<span class="status {cls}">{status}</span>'


def deadline_badge(value: str):
    cls = {"OVERDUE": "red", "DUE TODAY": "red", "COMPLETED": "green", "UPCOMING": "blue"}.get(value, "blue")
    return f'<span class="status {cls}">{value}</span>'


data = get_data()
sources = source_map(data)
health = pack_health(data)

st.markdown(
    """<div class="hero"><h1>🧭 Executive Productivity Agent</h1>
    <p>Source-grounded daily action intelligence for Arjun Malhotra · VP Sales</p>
    <p style="margin-top:.65rem;font-weight:700;opacity:.96">Prepared by Shubham Kaushik · Assignment 1</p></div>""",
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Control Center")
    as_of = st.date_input(
        "Brief date",
        value=pd.Timestamp("2026-09-24"),
        min_value=pd.Timestamp("2026-09-21"),
        max_value=pd.Timestamp("2026-09-25"),
    )
    as_of = str(as_of)
    st.divider()
    st.caption("SOURCE PACK")
    st.write("Assignment 1 Data Pack")
    st.caption("PIPELINE")
    st.write("Deterministic reconciliation + optional LLM extraction")
    st.caption("RUNTIME AI")
    st.write("Enabled" if llm_available() else "Optional / no API key required")
    st.divider()
    st.caption("Data pack health")
    st.write(f"{health['source_items']} source records · {health['calendar_events']} calendar events")

brief = make_brief(data, as_of)

metrics = st.columns(5)
metric_values = [
    ("My actions today", len(brief["today"])),
    ("Overdue", len(brief["overdue"])),
    ("Waiting on others", len(brief["waiting"])),
    ("Owner unknown", len(brief["unclear"])),
    ("Completed", len(brief["completed"])),
]
for col, (label, value) in zip(metrics, metric_values):
    with col:
        st.markdown(f'<div class="metric-wrap"><div class="kicker">{label}</div><div style="font-size:1.8rem;font-weight:800;margin-top:.15rem">{value}</div></div>', unsafe_allow_html=True)

st.markdown("### Daily Executive Brief")
left, right = st.columns([1.25, 1])

with left:
    st.markdown(f"**As of {pd.Timestamp(as_of).strftime('%A, %d %B %Y')}**")
    if brief["today"]:
        st.markdown("#### 🔵 My actions today")
        for t in brief["today"]:
            st.markdown(
                f'<div class="card"><b>{t["title"]}</b><div style="margin:.35rem 0">{status_badge(t["status"])}{deadline_badge(t["deadline_status"])}</div><div class="small">Deadline: {t["deadline_label"]} · Stakeholder: {t["stakeholder"]}</div><div class="small" style="margin-top:.25rem">{t["notes"]}</div></div>',
                unsafe_allow_html=True,
            )
    if brief["overdue"]:
        st.markdown("#### 🔴 Overdue")
        for t in brief["overdue"]:
            st.markdown(
                f'<div class="card"><b>{t["title"]}</b><div style="margin:.35rem 0">{status_badge(t["status"])}{deadline_badge(t["deadline_status"])}</div><div class="small">Original/latest stated deadline: {t["deadline_label"]}</div><div class="small">Owner: {t["action_owner"] or "UNKNOWN"}</div></div>',
                unsafe_allow_html=True,
            )
    if brief["unclear"]:
        st.markdown("#### ⚠️ Needs ownership confirmation")
        for t in brief["unclear"]:
            st.markdown(
                f'<div class="card"><b>{t["title"]}</b><div style="margin:.35rem 0">{status_badge(t["status"])}{deadline_badge(t["deadline_status"])}</div><div class="small">Deadline: {t["deadline_label"]}</div><div class="small">The Data Pack explicitly says not to assume ownership.</div></div>',
                unsafe_allow_html=True,
            )

with right:
    st.markdown("#### Priority signals")
    if brief["overdue"]:
        st.error(f"{len(brief['overdue'])} open item(s) are past their stated deadline.")
    if brief["unclear"]:
        st.warning("Mumbai lease renewal is still unowned; confirm the responsible signer instead of assuming Facilities.")
    if not brief["overdue"] and not brief["unclear"]:
        st.success("No overdue or ownership-ambiguous items in the selected brief.")

    st.markdown("#### Upcoming")
    for t in brief["upcoming"]:
        st.markdown(f"• **{t['title']}** — {t['deadline_label']}")

st.divider()

# ------------------------- Tabs -------------------------
tab_tasks, tab_agent, tab_trace, tab_sources = st.tabs([
    "📋 Task Register", "💬 Ask the Agent", "🔍 Agent Trace", "🗂 Sources & Evidence"
])

with tab_tasks:
    st.caption("One row = one canonical action after reconciliation across meetings, emails, calendars and voice notes.")
    rows = []
    for v in brief["all"]:
        rows.append({
            "ID": v["task_id"],
            "Task": v["title"],
            "Owner": v["action_owner"] or "UNKNOWN",
            "Stakeholder": v["stakeholder"] or "—",
            "Status": v["status"],
            "Deadline status": v["deadline_status"],
            "Deadline": v["deadline_label"] or "—",
            "Priority": v["priority"],
            "Sources": len(v["source_ids"]),
        })
    df = pd.DataFrame(rows)
    status_filter = st.multiselect("Filter status", sorted(df["Status"].unique()), default=sorted(df["Status"].unique()))
    view_df = df[df["Status"].isin(status_filter)]
    st.dataframe(view_df, use_container_width=True, hide_index=True)

    st.markdown("#### Reconciliation notes")
    for t in canonical_tasks(data):
        st.markdown(f"**{t.task_id} · {t.title}** — {t.reconciliation}")

with tab_agent:
    st.markdown("Ask about commitments, deadlines, dependencies or ownership. Answers are grounded in the supplied Data Pack only.")
    examples = [
        "What did I promise Raghav?",
        "What needs action today?",
        "What am I waiting for?",
        "What is overdue?",
        "Who owns the Mumbai lease?",
        "What is completed?",
    ]
    cols = st.columns(3)
    for i, ex in enumerate(examples):
        if cols[i % 3].button(ex, key=f"ex_{i}"):
            st.session_state["question"] = ex
    q = st.text_input("Question", key="question", placeholder="e.g. What did I promise Raghav?")
    if st.button("Run agent", type="primary") and q.strip():
        response, ids = answer(q, as_of, data)
        st.markdown(f'<div class="card"><div class="kicker">Agent response</div><div style="margin-top:.4rem;line-height:1.55">{response}</div></div>', unsafe_allow_html=True)
        if ids:
            st.markdown("**Evidence used**")
            for sid in dict.fromkeys(ids):
                s = sources[sid]
                st.markdown(f'<span class="source-chip">{s["source_type"]} · {s["title"]} · {s["date"]}</span>', unsafe_allow_html=True)

with tab_trace:
    st.markdown("The agent is deliberately hybrid: AI can extract meaning, while deterministic rules protect ownership, deadlines, completion and auditability.")
    for step in pipeline_trace(data):
        st.markdown(f'<div class="trace"><b>{step["step"]}</b><div class="small">{step["detail"]}</div></div>', unsafe_allow_html=True)

    st.markdown("#### Guardrails")
    guards = [
        "Never infer an owner from a typical process owner.",
        "When a deadline changes, keep the history and use the latest explicit commitment as current.",
        "Calendar entries corroborate timing; they do not create duplicate actions when the underlying commitment already exists.",
        "Personal voice notes belong to Arjun's own commitment set, not to an external request queue.",
    ]
    for g in guards:
        st.markdown(f"✓ {g}")

with tab_sources:
    h = pack_health(data)
    st.markdown("#### Source pack overview")
    s_cols = st.columns(4)
    for col, label, val in [
        (s_cols[0], "Meeting sources", h["meetings"]),
        (s_cols[1], "Email messages", h["emails"]),
        (s_cols[2], "Voice notes", h["voice_notes"]),
        (s_cols[3], "Calendar events", h["calendar_events"]),
    ]:
        col.metric(label, val)

    st.markdown("#### Task-level audit trail")
    for t in canonical_tasks(data):
        counts = source_counts(t)
        with st.expander(f"{t.task_id} · {t.title}"):
            st.write(f"**Owner:** {t.action_owner or 'UNKNOWN'} · **Stakeholder:** {t.stakeholder or '—'}")
            st.write(f"**Deadline:** {t.deadline_label or '—'} · **Priority:** {t.priority}")
            st.write(f"**Reconciliation:** {t.reconciliation}")
            if t.deadline_history:
                st.write("**Deadline history:** " + " → ".join(t.deadline_history))
            st.write(f"**Source mentions merged:** {counts['sources']} ({counts['emails']} email, {counts['meetings']} meeting, {counts['voice_notes']} voice)")
            for sid in t.source_ids:
                s = sources[sid]
                st.markdown(f"**{s['source_type']} · {s['title']} · {s['date']} · {s['speaker_or_sender']}**")
                st.caption(s["excerpt"])

st.markdown('<div class="footer">Executive Productivity Agent · Candidate: Shubham Kaushik · Source-grounded prototype</div>', unsafe_allow_html=True)
