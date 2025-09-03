# Deterministic stats → Markdown + PDF (your exact format)
from datetime import datetime
from pathlib import Path
from typing import Tuple
import pandas as pd
import markdown
from weasyprint import HTML

def _int(v) -> int:
    try:
        return int(v)
    except Exception:
        try:
            return int(float(v))
        except Exception:
            return 0

def make_summary_markdown(df: pd.DataFrame, campaign: str) -> str:
    total = int(len(df))
    emails_sent = int((df["status"].astype(str).str.lower() == "emailed").sum())
    high_priority = int((df["priority"].astype(str).str.lower() == "high").sum())

    # Response categories (case-insensitive)
    cats = df["response_category"].astype(str).str.lower().value_counts().to_dict()
    interested = cats.get("interested", 0)
    follow_later = cats.get("follow-up later", 0) + cats.get("follow up later", 0)
    not_fit = cats.get("not a fit", 0)

    # Top 5 by score
    safe = df.copy()
    safe["__score_int__"] = safe["score"].apply(_int)
    top5 = safe.sort_values("__score_int__", ascending=False).head(5)

    lines = []
    lines.append(f'# Campaign Summary\n')
    lines.append(f'- Total leads processed: **{total}**')
    lines.append(f'- Emails sent: **{emails_sent}**')
    lines.append(f'- High-priority leads: **{high_priority}**\n')
    lines.append(f'## Response Categories')
    lines.append(f'- interested: {interested}')
    lines.append(f'- follow-up later: {follow_later}')
    lines.append(f'- not a fit: {not_fit}\n')
    lines.append(f'## Top 5 Leads by Score')

    for _, r in top5.iterrows():
        company = str(r.get("company", "") or "").strip() or "Unknown Co"
        name = f'{str(r.get("first_name","")).strip()} {str(r.get("last_name","")).strip()}'.strip()
        score = _int(r.get("score", 0))
        prio = str(r.get("priority","")).lower() or "medium"
        lines.append(f'- {company} ({name}): score {score} / priority {prio}')

    return "\n".join(lines) + "\n"

def write_report_files(markdown_text: str) -> Tuple[str, str]:
    Path("reports").mkdir(parents=True, exist_ok=True)
    stamp = datetime.utcnow().strftime("report-%Y%m%d-%H%M")
    md_path = f"reports/{stamp}.md"
    pdf_path = f"reports/{stamp}.pdf"

    # Save Markdown file
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(markdown_text)

    # Convert Markdown → HTML
    html = markdown.markdown(markdown_text)

    # Convert HTML → PDF using WeasyPrint
    HTML(string=html).write_pdf(pdf_path)

    return md_path, pdf_path
