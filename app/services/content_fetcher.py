from app.models.article import ArticleContent
from app.services.xai_client import XAIClient
from app.utils.html_cleaner import extract_readable_text
import logging
import httpx

logger = logging.getLogger("app.content_fetcher")

class ContentFetcher:
    def __init__(self, xai_client: XAIClient):
        self.xai_client = xai_client

    async def fetch(self, url: str) -> ArticleContent:
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(url)
                response.raise_for_status
                raw_html = response.text
                raw_content = extract_readable_text(raw_html)
                return await self.xai_client.extract_article_content(url, raw_content)
            except httpx.HTTPError as e:
                raise RuntimeError(f"HTTP error fetching {url}: {e}")

        try:
            return await self.xai_client.extract_article_content(url, raw_content)
        except Exception as e:
            raise RuntimeError(f"xAI extraction failed for {url}: {e}") from e
