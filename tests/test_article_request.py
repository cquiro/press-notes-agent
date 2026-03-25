import pytest
from pydantic import ValidationError

from app.models.article import ArticleRequest


def test_article_request_rejects_empty_url_list():
    with pytest.raises(ValidationError):
        ArticleRequest(urls=[])
