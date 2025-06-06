from bs4 import BeautifulSoup, Tag

def extract_readable_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    article = soup.find("article")
    if not article:
        article = soup.find("div", class_="article-body") or \
                  soup.find("div", class_="content") or \
                  soup

    if not isinstance(article, Tag):
        return ""

    for tag in article.find_all(["script", "style", "noscript", "header", "footer", "nav", "aside"]):
        tag.decompose()

    text = article.get_text(separator="\n")
    return text.strip()
