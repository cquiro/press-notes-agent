from dotenv import load_dotenv
from pydantic import ValidationError
import httpx
import json
import logging
import os

from app.models.article import ArticleContent

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class XAIClient:
    def __init__(self):
        self.api_key = os.getenv("XAI_API_KEY")
        if not self.api_key:
            logger.error("xAI API key not found in .env")
            raise ValueError("XAI_API_KEY must be set in .env")
        self.base_url = "https://api.x.ai"

    async def extract_article_content(self, url: str, raw_content: str) -> ArticleContent:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        raw_content = raw_content[:10000]
        prompt = "Extract the main article content from the provided text. Remove ads, author bios, navigation menus, and other irrelevant sections. Return a JSON object with 'title' (the article title) and 'content' (the main body text). If no title is found, use a placeholder."
        payload = {
            "model": "grok-3",
            "messages": [
                {"role": "user", "content": prompt},
                {"role": "user", "content": raw_content}
            ],
            "max_tokens": 2000
        }

        async with httpx.AsyncClient() as client:
            try:
                logger.info(f"Sending xAI API request for {url}")
                response = await client.post(f"{self.base_url}/v1/chat/completions", json=payload, headers=headers)
                response.raise_for_status()
                result = response.json()
                extracted = result["choices"][0]["message"]["content"]
                try:
                    parsed = json.loads(extracted)
                    logger.info(f"Successfully parsed xAI response for {url}")
                    return ArticleContent(url=url, **parsed)
                except json.JSONDecodeError:
                    logger.error(f"Invalid JSON from xAI API for {url}: {extracted}")
                    return ArticleContent(url=url, title="Untitled", content=extracted)
            except httpx.HTTPStatusError as e:
                logger.error(f"xAI API error for {url}: {e}")
                raise Exception(f"xAI API error: {e}")
            except ValidationError as e:
                logger.error(f"Response validation error for {url}: {e}")
                raise Exception(f"Response validation error: {e}")
