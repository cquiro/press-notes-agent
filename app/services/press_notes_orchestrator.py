from pathlib import Path
from typing import List, Union, Tuple
import logging

from app.services.content_fetcher import ContentFetcher
from app.services.pdf_generator import PDFGenerator
from app.models.article import ArticleContent, ArticleError

logger = logging.getLogger("app.orchestrator")

class PressNotesOrchestrator:
    def __init__(self, content_fetcher: ContentFetcher):
        self.content_fetcher = content_fetcher

    async def build_press_notes(self, urls: List[str]) -> Tuple[List[Union[ArticleContent, ArticleError]], Path]:
        logger.info("Starting press notes build process")

        articles: List[Union[ArticleContent, ArticleError]] = []

        for url in urls:
            try:
                article = await self.content_fetcher.fetch(url)
                articles.append(article)
                logger.info(f"Fetched and parsed article from {url}")
            except Exception as e:
                logger.error(f"Failed to process {url}: {e}")
                articles.append(ArticleError(url=url, error=str(e)))

        valid_articles: List[ArticleContent] = [a for a in articles if isinstance(a, ArticleContent)]
        pdf_path = PDFGenerator().generate_pdf(valid_articles)
        logger.info(f"PDF generated at {pdf_path}")

        return articles, pdf_path
