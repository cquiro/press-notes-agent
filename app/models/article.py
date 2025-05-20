from pydantic import BaseModel, HttpUrl
from pydantic.types import conlist
from typing import List, Annotated

class ArticleRequest(BaseModel):
    urls: Annotated[List[HttpUrl], conlist(HttpUrl, max_items=10)]

class ArticleContent(BaseModel):
    url: str
    title: str
    content: str

class ArticleResponse(BaseModel):
    articles: List[ArticleContent]