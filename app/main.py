from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from app.logging_config import setup_logging
from app.models.article import ArticleRequest, ArticleExtractionResponse
from app.services.content_fetcher import ContentFetcher
from app.services.xai_client import XAIClient
from app.services.press_notes_orchestrator import PressNotesOrchestrator
import os

setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    xai_client = XAIClient()
    await xai_client.init()
    content_fetcher = ContentFetcher(xai_client=xai_client)
    app.state.orchestrator = PressNotesOrchestrator(content_fetcher=content_fetcher)
    yield
    await xai_client.close()

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
async def read_root():
    return FileResponse("app/static/index.html")

@app.post("/extract-content", response_model=ArticleExtractionResponse)
async def extract_relevant_content(request: ArticleRequest, req: Request):
    orchestrator: PressNotesOrchestrator = req.app.state.orchestrator

    articles, pdf_path = await orchestrator.build_press_notes([str(url) for url in request.urls])
    return {
        "results": articles,
        "pdf_path": str(pdf_path)
    }

@app.get("/download/{pdf_filename}")
async def download_pdf(pdf_filename: str):
    # ToDo: Sanitize the filename and ensure the path is securely constructed to prevent directory traversal attacks.
    pdf_path = os.path.join("output", pdf_filename)
    if os.path.exists(pdf_path):
        return FileResponse(pdf_path, media_type='application/pdf', filename=pdf_filename)
    return {"error": "File not found"}
