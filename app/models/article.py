from pydantic import BaseModel, HttpUrl, Field
from typing import List, Union

class ArticleRequest(BaseModel):
    urls: List[HttpUrl] = Field(..., max_length=10)

class ArticleContent(BaseModel):
    url: str
    title: str
    content: str

class ArticleResponse(BaseModel):
    articles: List[ArticleContent]

class ArticleError(BaseModel):
    url: str
    error: str

class ArticleExtractionResponse(BaseModel):
    results: List[Union[ArticleContent, ArticleError]]