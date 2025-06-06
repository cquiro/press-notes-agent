from readability import Document
from lxml import html

def extract_readable_text_and_title(raw_html: str) -> tuple[str, str]:
    doc = Document(raw_html)
    title = doc.short_title()

    readable_html = doc.summary()  # returns cleaned-up HTML as string
    tree = html.fromstring(readable_html)
    text = tree.text_content().strip()

    return text, title
