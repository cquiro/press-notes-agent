from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from app.logging_config import setup_logging
from app.models.article import ArticleRequest, ArticleExtractionResponse
from app.services.content_fetcher import ContentFetcher
from app.services.xai_client import XAIClient
from app.services.press_notes_orchestrator import PressNotesOrchestrator

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

@app.post("/extract-content", response_model=ArticleExtractionResponse)
async def extract_relevant_content(request: ArticleRequest, req: Request):
    orchestrator: PressNotesOrchestrator = req.app.state.orchestrator

    articles, pdf_path = await orchestrator.build_press_notes([str(url) for url in request.urls])
    return {
        "results": articles,
        "pdf_path": str(pdf_path)
    }
