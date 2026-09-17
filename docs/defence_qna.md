# Defence Q&A Cheat Sheet

**Candidate: Shubham Kaushik**

| Question | Response |
|---|---|
| What makes this an agent? | It observes multiple sources, extracts commitments, reconciles duplicates, calculates state, produces a brief and answers follow-up questions with evidence. |
| Why hybrid instead of LLM-only? | Business-critical decisions such as ownership and deadline state should be deterministic and explainable. |
| Where is the ambiguity guardrail? | `status_for()` keeps a missing owner as `UNCLEAR OWNERSHIP`; Q&A also states the ambiguity rather than guessing. |
| How does deduplication work? | A canonical task ID links related mentions. Source IDs remain attached so the reviewer can inspect the evidence. |
| What happens when the user changes the date? | The status engine recalculates waiting/action/completed and overdue/due-today/upcoming state using that selected date. |
| What is the role of the optional LLM? | It demonstrates structured semantic extraction from raw text; the final demo status remains controlled by deterministic reconciliation rules. |
| How do you handle auditability? | Each task stores source IDs, notes, deadline history and a reconciliation explanation. |
| Why use a local demo? | It makes the prototype deterministic and reviewer-accessible even without external API credentials. |
| How would this scale? | Add source connectors, persistent storage, authentication, observability and approval flows while keeping the same canonical task model. |
