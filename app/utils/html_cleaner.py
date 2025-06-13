from readability import Document
from lxml import html

from readability import Document
from lxml import html

def extract_readable_text_and_title(raw_html: str) -> tuple[str, str]:
    doc = Document(raw_html)
    readable_html = doc.summary()
    body_tree = html.fromstring(readable_html)

    # Extract cleaned article content with paragraph breaks
    paragraphs = [p.text_content().strip() for p in body_tree.findall(".//p") if p.text_content().strip()]
    text = "\n\n".join(paragraphs)

    # Extract the best available <h1> from the full raw HTML (not the summary)
    full_tree = html.fromstring(raw_html)
    h1 = full_tree.find(".//h1")
    title = h1.text_content().strip() if h1 is not None else doc.short_title()

    return text, title
