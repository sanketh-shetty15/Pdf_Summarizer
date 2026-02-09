import pdfplumber
from typing import Union
import io

def extract_text_from_pdf(pdf_file: Union[str, bytes, "io.BytesIO"]) -> str:
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            content = page.extract_text()
            if content:
                cleaned = "\n".join(line.strip() for line in content.splitlines())
                text += cleaned + "\n\n"
    return text.strip()
