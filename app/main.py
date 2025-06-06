from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.logging_config import setup_logging
from app.models.article import ArticleRequest, ArticleError, ArticleExtractionResponse
from app.services.content_fetcher import ContentFetcher
from app.services.xai_client import XAIClient
import asyncio

setup_logging()

xai_client = XAIClient()

@asynccontextmanager
async def lifespan(app: FastAPI):
    xai_client = XAIClient()
    await xai_client.init()
    app.state.content_fetcher = ContentFetcher(xai_client=xai_client)
    yield
    await xai_client.close()

app = FastAPI(lifespan=lifespan)

content_fetcher = ContentFetcher(xai_client=xai_client)

@app.post("/extract-content", response_model=ArticleExtractionResponse)
async def extract_relevant_content(request: ArticleRequest):
    async def extract_with_error_handling(url):
        try:
            content = await content_fetcher.fetch(str(url))
            return content
        except Exception as e:
            return ArticleError(url=str(url), error=str(e))

    tasks = [extract_with_error_handling(url) for url in request.urls]
    results = await asyncio.gather(*tasks)
    return {"results": results}
