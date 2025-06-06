from bs4 import BeautifulSoup, Tag

def extract_readable_text_and_title(html: str) -> tuple[str, str]:
    soup = BeautifulSoup(html, "html.parser")

    article = soup.find("article")
    if not article:
        article = soup.find("div", class_="article-body") or \
                  soup.find("div", class_="content") or \
                  soup

    if not isinstance(article, Tag):
        return "", "Untitled"

    for tag in article.find_all(["script", "style", "noscript", "header", "footer", "nav", "aside"]):
        tag.decompose()

    # Try to find the best title candidate
    title_tag = soup.find("h1") or soup.find("h2")
    title = title_tag.get_text(strip=True) if title_tag else "Untitled"

    text = article.get_text(separator="\n")
    return text.strip(), title