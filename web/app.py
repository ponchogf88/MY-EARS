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
from core.curator_bot import SpotifyCuratorBot
from monetization.review_assistant import CuratorReviewAssistant
from integrations.notion_sync import NotionHustleSync

app = FastAPI(title="MY EARS Platform")
templates = Jinja2Templates(directory="web/templates")
pipeline = MyEarsPipeline()
curator_bot = SpotifyCuratorBot()
review_assistant = CuratorReviewAssistant()
notion_sync = NotionHustleSync()

class ExperienceRequest(BaseModel):
    experience: str
    volume: int = 1

class CuratorBotRequest(BaseModel):
    niche: str
    emotional_prompt: str = ""

class ReviewRequest(BaseModel):
    artist: str
    track_title: str
    genre: str
    playlist_name: str
    decision: str
    key_observation: str = ""

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

@app.post("/api/curator-bot")
async def run_curator_bot(req: CuratorBotRequest):
    package = curator_bot.generate_curator_package(
        niche=req.niche,
        user_emotional_prompt=req.emotional_prompt
    )
    return package

@app.post("/api/review-assistant")
async def generate_review(req: ReviewRequest):
    review = review_assistant.generate_review(
        artist=req.artist,
        track_title=req.track_title,
        genre=req.genre,
        playlist_name=req.playlist_name,
        decision=req.decision,
        key_observation=req.key_observation
    )
    return review

@app.post("/api/export-notion")
async def export_notion(req: CuratorBotRequest):
    package = curator_bot.generate_curator_package(niche=req.niche)
    entry = notion_sync.prepare_notion_entry(package, followers=0, spotify_url="https://open.spotify.com/playlist/simulated")
    csv_path = notion_sync.export_to_notion_csv([entry])
    return {"status": "exported", "file_path": csv_path, "entry": entry}

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
