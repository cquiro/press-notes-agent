from pydantic import BaseModel, HttpUrl, Field
from pydantic.types import conlist
from typing import List

class ArticleRequest(BaseModel):
    urls: List[HttpUrl] = Field(..., max_length=10)

class ArticleContent(BaseModel):
    url: str
    title: str
    content: str

class ArticleResponse(BaseModel):
    articles: List[ArticleContent]