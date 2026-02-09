# 📄 AI PDF/Text Summariser

A simple Streamlit app that extracts text from PDFs or text input and generates simplified summaries using Hugging Face Transformers.

## Features
- Upload PDF or paste text
- Extract text with pdfplumber
- Summarise using Hugging Face models (BART)
- Download summary as text file

## Setup
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
