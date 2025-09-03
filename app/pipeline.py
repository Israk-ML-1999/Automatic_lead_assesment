# Orchestrates end-to-end flow
import os
from argparse import ArgumentParser
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any, Optional
from datetime import datetime

import pandas as pd

from app.services.csv_io import read_leads, write_leads
from app.services.emailer import send_email
from app.services.llm import logger

from app.agents.enrichment import enrich_batch
from app.agents.reporting import make_summary_markdown, write_report_files

COMPANY = os.getenv("COMPANY_NAME", "Acme Corp")
CAMPAIGN = os.getenv("CAMPAIGN_NAME", "Default Campaign")
PITCH = os.getenv("PRODUCT_PITCH", "A great product.")
DEFAULT_BATCH = int(os.getenv("BATCH_SIZE", "10"))
DEFAULT_MAX_CONC = int(os.getenv("MAX_CONCURRENT_BATCHES", "5"))

def _build_lead_payload(row: pd.Series) -> Dict[str, Any]:
    return {
        "first_name": row.get("first_name", ""),
        "last_name": row.get("last_name", ""),
        "email": row.get("email", ""),
        "company": row.get("company", ""),
        "job_title": row.get("job_title", ""),
        "linkedin_url": row.get("linkedin_url", ""),
        "notes": row.get("notes", ""),
        "campaign": CAMPAIGN,
        "company_pitch": PITCH
    }

def _chunked(seq: List[Any], size: int) -> List[List[Any]]:
    return [seq[i:i+size] for i in range(0, len(seq), size)]

def _process_batches(batches: List[List[Dict[str, Any]]], max_workers: int) -> List[List[Dict[str, Any]]]:
    results: List[Optional[List[Dict[str, Any]]]] = [None] * len(batches)
    def task(idx: int, payload: List[Dict[str, Any]]):
        logger(f"Enriching batch {idx+1}/{len(batches)} (size {len(payload)})…")
        out = enrich_batch(payload)  # returns list aligned to payload
        results[idx] = out

    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futs = [ex.submit(task, i, b) for i, b in enumerate(batches)]
        for f in as_completed(futs):
            _ = f.result()
    return results  # type: ignore

def run_pipeline(path: str, batch_size: int = DEFAULT_BATCH, max_concurrent_batches: int = DEFAULT_MAX_CONC):
    # Generate CSV if missing
    if not Path(path).exists():
        from scripts.make_sample_leads import ensure_sample
        ensure_sample(path)

    df = read_leads(path)

    # payloads
    leads_payload = [ _build_lead_payload(row) for _, row in df.iterrows() ]

    # batching
    batches = _chunked(leads_payload, batch_size)

    # parallel Groq calls
    batch_results = _process_batches(batches, max_workers=max_concurrent_batches)
    enriched_all = [item for sub in batch_results for item in (sub or [])]
    if len(enriched_all) != len(leads_payload):
        raise RuntimeError(f"Unexpected batch result size: got {len(enriched_all)} vs {len(leads_payload)}")

    # write back + send emails
    sent = 0
    sent_ts = datetime.utcnow().isoformat() + "Z"

    for i, enr in enumerate(enriched_all):
        persona = str(enr.get("persona", "")).strip()
        priority = str(enr.get("priority", "Medium")).strip()
        status = str(enr.get("status", "Emailed")).strip()
        subject = str(enr.get("email_subject", "Quick question")).strip()
        body = str(enr.get("email_body", "")).strip()
        score = int(enr.get("score", 0))
        response_category = str(enr.get("response_category", "")).strip()

        df.at[i, "persona"] = persona
        df.at[i, "priority"] = priority
        df.at[i, "status"] = status
        df.at[i, "email_subject"] = subject
        df.at[i, "email_body"] = body
        df.at[i, "score"] = score
        df.at[i, "response_category"] = response_category
        df.at[i, "email_sent_at"] = sent_ts

        to_email = df.at[i, "email"]
        try:
            if isinstance(to_email, str) and "@" in to_email:
                send_email(to_email, subject, body)
                sent += 1
        except Exception as e:
            logger(f"Email send failed for {to_email}: {e}")

    write_leads(df, path)

    # summary (deterministic — your exact format)
    md = make_summary_markdown(df, CAMPAIGN)
    md_path, pdf_path = write_report_files(md)

    return {
        "leads": len(df),
        "sent": sent,
        "report_md": md_path,
        "report_pdf": pdf_path
    }

if __name__ == "__main__":
    ap = ArgumentParser()
    ap.add_argument("--file", default=os.getenv("LEADS_CSV", "data/leads.csv"))
    ap.add_argument("--batch-size", type=int, default=DEFAULT_BATCH)
    ap.add_argument("--max-concurrent-batches", type=int, default=DEFAULT_MAX_CONC)
    args = ap.parse_args()
    stats = run_pipeline(args.file, batch_size=args.batch_size, max_concurrent_batches=args.max_concurrent_batches)
    print(stats)
