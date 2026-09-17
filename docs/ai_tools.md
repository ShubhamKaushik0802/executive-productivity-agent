# AI Tools Used

**Candidate: Shubham Kaushik**

## ChatGPT

Used for architecture ideation, implementation assistance, edge-case/test design, UI/content drafting, README documentation and 10-slide presentation drafting.

## Optional OpenAI API

`src/ai_agent.py` contains an optional structured extraction layer. With an API key configured, it asks an LLM to extract:

- action title
- action owner
- stakeholder
- waiting-on person
- deadline
- evidence quote
- ownership confidence

The API output is not allowed to override the demo's deterministic business rules. This keeps owner, deadline and completion logic auditable.

## Non-AI implementation tools

Python, Streamlit, pandas, Pydantic, PyMuPDF, python-pptx and Git/GitHub.
