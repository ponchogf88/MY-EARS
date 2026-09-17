"""
Web Server & Dashboard for MY EARS.
API FastAPI que sirve la interfaz web y gestiona el flujo de procesamiento continuo.
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn
import json
from pathlib import Path

from core.pipeline import MyEarsPipeline

app = FastAPI(title="MY EARS Platform")
templates = Jinja2Templates(directory="web/templates")
pipeline = MyEarsPipeline()

class ExperienceRequest(BaseModel):
    experience: str
    volume: int = 1

@app.get("/", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/process")
async def process_experience(req: ExperienceRequest):
    result = pipeline.process_experience(
        experience_text=req.experience,
        volume=req.volume,
        auto_publish=True
    )
    return result

@app.get("/api/ideas")
async def get_ideas():
    ideas_path = Path("data/ideas_bank.json")
    if ideas_path.exists():
        with open(ideas_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"ideas": []}

@app.get("/api/history")
async def get_history():
    history_path = Path("data/history.json")
    if history_path.exists():
        with open(history_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"playlists": [], "campaigns": []}

if __name__ == "__main__":
    uvicorn.run("web.app:app", host="127.0.0.1", port=8000, reload=False)
