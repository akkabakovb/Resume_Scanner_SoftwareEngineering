from fastapi import FastAPI
from app.routers import roles

app = FastAPI(
    title="Resume Analyzer API",
    description="AI-powered resume analysis and job role matching",
    version="1.0.0"
)

app.include_router(roles.router)

@app.get("/")
async def root():
    return {"message": "Resume Analyzer API is running!"}

@app.get("/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}
