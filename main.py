from fastapi import FastAPI
from app.routers import analyze

app = FastAPI()
app.include_router(analyze.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
