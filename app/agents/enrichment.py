# Fill gaps + persona + score + response_category + drafts
import json
from typing import List, Dict, Any
from app.services.llm import chat_json_array

SYSTEM_PROMPT = (
    "You are a precise B2B lead enrichment assistant for sales outreach.\n"
    "OUTPUT STRICTLY AS A JSON ARRAY — no prose, no markdown, no code fences.\n"
    "For each input lead, return an object with fields:\n"
    '  - "persona": short descriptor like "Marketing Manager at SaaS" or "CTO in HealthTech"\n'
    '  - "priority": one of ["High","Medium","Low"] based on ICP fit & buying intent\n'
    '  - "status": always "Emailed"\n'
    '  - "email_subject": short, crisp, personal\n'
    '  - "email_body": 70–120 words, personalized (use first_name), include one concrete hook and a clear CTA for a 15-min chat\n'
    '  - "score": integer 0–100 reflecting quality/fit/intent (higher is better)\n'
    '  - "response_category": one of ["interested","follow-up later","not a fit"] predicted from context\n'
    "Keep tone professional and specific; avoid fluff.\n"
)

USER_TEMPLATE = """You will be given a batch of leads as JSON.
Return a JSON array with exactly the same length and order. Each element must follow this schema:
{{
  "persona": string,
  "priority": "High" | "Medium" | "Low",
  "status": "Emailed",
  "email_subject": string,
  "email_body": string,
  "score": number,
  "response_category": "interested" | "follow-up later" | "not a fit"
}}

Batch leads:
{batch_json}

Context:
- The product pitch is included per lead as "company_pitch".
- If fields are missing, infer plausibly from title/industry/notes.

IMPORTANT:
- Output must be a single JSON array only (no explanations).
- Keep email_body within 70–120 words.
- Ensure score is an integer 0–100.
"""

def enrich_batch(leads_batch: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    user_prompt = USER_TEMPLATE.format(batch_json=json.dumps(leads_batch, ensure_ascii=False))
    return chat_json_array(SYSTEM_PROMPT, user_prompt)
