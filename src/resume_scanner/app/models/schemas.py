from typing import Optional

from pydantic import BaseModel

# ---- REQUEST MODELS ----

class ResumeTextRequest(BaseModel):
    resume_text: str

# ---- RESPONSE MODELS ----

class RoleMatch(BaseModel):
    title: str
    reason: str
    match_score: int
    key_skills: list[str]

class RolesResponse(BaseModel):
    roles: list[RoleMatch]

class AnalysisResult(BaseModel):
    score: int
    strengths: list[str]
    weaknesses: list[str]
    skills: list[str]
    improved_summary: str
    recommendation: str

class AnalysisResponse(BaseModel):
    filename: Optional[str] = None
    analysis: AnalysisResult

class ResumeAnalysisResponse(BaseModel):
    score: int
    strengths: list[str]
    weaknesses: list[str]
    skills: list[str]
    improved_summary: str
    recommendation: str
    matched_roles: list[RoleMatch]

class ATSRequest(BaseModel):
    resume_text: str
    job_description: str

class ATSResult(BaseModel):
    ats_score: int
    matched_keywords: list[str]
    missing_keywords: list[str]
    suggestions: list[str]
    verdict: str

class ATSResponse(BaseModel):
    filename: Optional[str] = None
    result: ATSResult
