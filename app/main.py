from fastapi import FastAPI
from app.models.article import ArticleRequest
from app.services.content_fetcher import fetch_raw_content
import asyncio

app = FastAPI()

@app.post("/fetch-raw")
async def fetch_raw_articles(request: ArticleRequest):
    async def fetch_with_error_handling(url):
        try:
            raw_html = await fetch_raw_content(str(url))
            return {"url": url, "raw_html": raw_html}
        except Exception as e:
            return {"url": url, "error": str(e)}

    tasks = [fetch_with_error_handling(url) for url in request.urls]
    results = await asyncio.gather(*tasks)
    return {"results": results}
