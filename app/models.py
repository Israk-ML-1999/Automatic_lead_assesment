# Pydantic models for structured I/O
from pydantic import BaseModel, Field
from typing import Optional, Dict

class Lead(BaseModel):
    first_name: str = ""
    last_name: str = ""
    email: str
    company: Optional[str] = None
    job_title: Optional[str] = None
    linkedin_url: Optional[str] = None
    notes: Optional[str] = None

class EnrichmentOutput(BaseModel):
    persona: str
    priority: str  # High | Medium | Low
    status: str    # "Emailed"
    email_subject: str
    email_body: str
    score: int = Field(ge=0, le=100)
    response_category: str  # interested | follow-up later | not a fit
    extra: Dict[str, str] = Field(default_factory=dict)
