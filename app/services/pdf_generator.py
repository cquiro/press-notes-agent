from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from app.models.article import ArticleContent
from datetime import datetime
from typing import List
import os
import re


class PDFGenerator:
    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def wrap_text(self, text: str, max_width: float, canvas_obj, font_name: str = "Helvetica", font_size: int = 12) -> List[str]:
        words = text.split()
        lines = []
        line = ""
        canvas_obj.setFont(font_name, font_size)

        for word in words:
            test_line = f"{line} {word}" if line else word
            if canvas_obj.stringWidth(test_line, font_name, font_size) < max_width:
                line = test_line
            else:
                lines.append(line)
                line = word

        if line:
            lines.append(line)

        return lines

    def generate_pdf(self, articles: List[ArticleContent]) -> Path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = Path(self.output_dir) / f"press_notes_{timestamp}.pdf"
        c = canvas.Canvas(str(output_path), pagesize=A4)
        width, height = A4
        margin = 2 * cm
        max_width = width - 2 * margin
        min_y = margin

        def maybe_new_page(text_obj):
            if text_obj and text_obj.getY() < min_y:
                c.drawText(text_obj)
                c.showPage()
                new_text_obj = c.beginText(margin, height - margin)
                new_text_obj.setFont("Helvetica", 12)
                return new_text_obj
            return text_obj

        text_object = c.beginText(margin, height - margin)
        text_object.setFont("Helvetica", 12)

        for i, article in enumerate(articles):
            if i > 0:
                # Before starting a new article, flush and start new page
                if text_object is not None:
                    c.drawText(text_object)
                c.showPage()
                text_object = c.beginText(margin, height - margin)
                text_object.setFont("Helvetica", 12)

            # Title in bold and larger font
            title_lines = self.wrap_text(article.title, max_width, c, font_name="Helvetica-Bold", font_size=16)
            text_object.setFont("Helvetica-Bold", 16)
            for line in title_lines:
                text_object.textLine(line)
                text_object = maybe_new_page(text_object)

            # URL in very small font
            text_object.setFont("Helvetica", 6)
            url_lines = self.wrap_text(article.url, max_width, c, font_name="Helvetica", font_size=6)
            for line in url_lines:
                text_object.textLine(line)
                text_object = maybe_new_page(text_object)

            # Space before content
            text_object.setFont("Helvetica", 12)
            text_object.textLine("")
            text_object = maybe_new_page(text_object)

            # Article content
            paragraphs = re.split(r'\n\s*\n+', article.content.strip())
            for paragraph in paragraphs:
                lines = paragraph.strip().splitlines()
                merged = " ".join(line.strip() for line in lines if line.strip())
                if not merged:
                    continue
                wrapped_lines = self.wrap_text(merged, max_width, c)
                for line in wrapped_lines:
                    text_object.textLine(line)
                    text_object = maybe_new_page(text_object)
                text_object.textLine("")
                text_object = maybe_new_page(text_object)

        if text_object is not None:
            c.drawText(text_object)

        c.save()
        return output_path
