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
