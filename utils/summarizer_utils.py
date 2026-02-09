import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)


def chunk_text(text, max_chars=6000):
    """
    Split long text into manageable chunks.
    """
    paragraphs = text.split("\n")
    chunks, current = [], ""
    for para in paragraphs:
        if len(current) + len(para) < max_chars:
            current += para + "\n"
        else:
            chunks.append(current.strip())
            current = para + "\n"
    if current.strip():
        chunks.append(current.strip())
    return chunks


def summarize_text(text: str, length: str = "short") -> str:
    """
    Summarizes text using Google Gemini API.
    Scales output length: short ~1/3 of input, medium ~1/2, long ~2/3.
    Ensures structured output (## headings, - bullet points).
    """

    if length == "short":
        instruction = (
            "Summarize this text into a structured outline about one-third "
            "the length of the original. Use ## headings for sections and - for bullet points. "
            "Target around 12–14 pages if the document is ~40 pages."
        )
        compression_ratio = 0.33

    elif length == "medium":
        instruction = (
            "Summarize this text into a detailed structured summary about half "
            "the length of the original. Use clear section headings (## ...) and bullet points. "
            "Target around 16–18 pages if the document is ~40 pages."
        )
        compression_ratio = 0.5

    else:  # long
        instruction = (
            "Create a comprehensive, structured summary about two-thirds "
            "the length of the original. Organize with headings (## ...) and bullets (- ...). "
            "Target around 20–22 pages if the document is ~40 pages."
        )
        compression_ratio = 0.66

    # chunk size based on ratio
    chunk_size = int(6000 * compression_ratio)
    chunks = chunk_text(text, max_chars=chunk_size)
    final_summary = ""

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        for i, chunk in enumerate(chunks, 1):
            prompt = f"{instruction}\n\nText (part {i}/{len(chunks)}):\n{chunk}"
            response = model.generate_content(prompt)
            final_summary += "\n\n" + response.text.strip()

        return final_summary.strip()

    except Exception as e:
        return f"API request failed: {str(e)}"
