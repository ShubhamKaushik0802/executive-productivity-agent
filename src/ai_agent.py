import json
import os


def llm_available() -> bool:
    return bool(os.getenv("OPENAI_API_KEY"))


def llm_extract(source_text: str):
    """Optional AI enhancement for raw-source extraction.

    The baseline app does not require an API key. The LLM returns structured
    candidates only; the deterministic reconciliation engine remains the source
    of truth for the demo's final status and ownership.
    """
    if not llm_available():
        return None
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        prompt = f"""Extract executive commitments from the following source text. Return JSON array only.
Each item: title, action_owner, stakeholder, waiting_on, deadline, deadline_text, evidence_quote, ownership_confidence.
Never invent ownership. If ownership is unclear, use null.
Prefer explicit commitments over inferred intentions.
SOURCE:\n{source_text}"""
        resp = client.chat.completions.create(
            model=model,
            temperature=0,
            messages=[
                {"role": "system", "content": "You are a source-grounded executive productivity extraction assistant."},
                {"role": "user", "content": prompt},
            ],
        )
        return json.loads(resp.choices[0].message.content)
    except Exception:
        return None
