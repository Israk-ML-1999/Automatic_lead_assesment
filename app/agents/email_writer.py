# (stub) finalize drafts if needed
# Drafts are already returned by enrichment; stub for future refinement.
def finalize_email(subject: str, body: str) -> tuple[str, str]:
    return subject.strip(), body.strip()
