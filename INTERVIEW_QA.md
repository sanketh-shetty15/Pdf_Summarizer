# INTERVIEW QUESTIONS & ANSWERS - PDF SUMMARISER + Q&A PROJECT

---

## **PROJECT OVERVIEW**

**Q1. What does your PDF Summariser project do?**  
**Answer:**  
It's a Streamlit app with 3 modes: (1) Summarize plain text, (2) Summarize PDFs, and (3) Answer questions from PDFs using AI. Users can download summaries as PDF, TXT, or DOCX files.

---

**Q2. What are the main technologies you used?**  
**Answer:**  
Python, Streamlit for UI, Google Gemini API for summarization, OpenAI GPT-4o-mini for Q&A, FAISS for vector search, Sentence Transformers for embeddings, and PDFPlumber for extracting text from PDFs.

---

## **STREAMLIT & FRONTEND**

**Q3. Why did you choose Streamlit instead of Flask?**  
**Answer:**  
Streamlit is faster to build data/AI apps with. It has built-in UI components like file uploaders, buttons, and text areas. No need for HTML/CSS or separate frontend code.

---

**Q4. How does the user choose between the 3 modes?**  
**Answer:**  
Using `st.radio()` - it creates radio buttons for "Text", "PDF Summarizer", and "PDF Q&A". Based on the selection, different UI components are shown.

---

## **PDF EXTRACTION**

**Q5. How do you extract text from PDFs?**  
**Answer:**  
Using `pdfplumber.open()`. It loops through each page, extracts text, cleans up extra spaces, and combines all pages into one string.

---

**Q6. What library handles PDF reading, and why?**  
**Answer:**  
PDFPlumber. It's reliable for text extraction, handles multi-page PDFs well, and works with file uploads or file paths.

---

## **SUMMARIZATION**

**Q7. Which API do you use for summarization?**  
**Answer:**  
Google Gemini API (`gemini-1.5-flash` model). It generates structured summaries with headings and bullet points based on short/medium/long length options.

---

**Q8. How does the length option work (short/medium/long)?**  
**Answer:**  
It changes the compression ratio: short = 1/3 of original text, medium = 1/2, long = 2/3. The prompt tells Gemini how detailed the summary should be.

---

**Q9. Why do you chunk the text before sending it to Gemini?**  
**Answer:**  
Long documents exceed API token limits. Chunking splits text into smaller parts (~6000 chars each), processes them separately, then combines the summaries.

---

**Q10. How does the chunk_text function work?**  
**Answer:**  
It splits text by paragraphs (`\n`). It adds paragraphs to a chunk until reaching max_chars, then starts a new chunk. This keeps paragraphs intact for better context.

---

## **Q&A SYSTEM**

**Q11. How does the PDF Q&A feature work?**  
**Answer:**  
(1) Extract text and split into chunks, (2) Convert chunks to embeddings using Sentence Transformers, (3) Store embeddings in FAISS index, (4) When user asks a question, find relevant chunks, (5) Send chunks + question to OpenAI GPT to generate an answer.

---

**Q12. What is FAISS and why do you use it?**  
**Answer:**  
FAISS is a vector similarity search library by Facebook. It quickly finds the most relevant text chunks by comparing embeddings. This makes Q&A faster and more accurate.

---

**Q13. What are embeddings and which model creates them?**  
**Answer:**  
Embeddings are numeric vectors that represent text meaning. I use `all-MiniLM-L6-v2` from Sentence Transformers - it's lightweight, fast, and runs locally without API calls.

---

**Q14. Why do you retrieve top-5 chunks instead of just 1?**  
**Answer:**  
One chunk might not have the complete answer. Top-5 gives more context, so the AI can combine information from multiple parts of the document for better answers.

---

**Q15. How do you prevent the AI from hallucinating (making up answers)?**  
**Answer:**  
I use a strict prompt that says "ONLY answer using the provided context. If not found, say 'I cannot find the answer in the document.'" This forces GPT to stay within the PDF content.

---

**Q16. Which OpenAI model do you use for Q&A, and why?**  
**Answer:**  
GPT-4o-mini. It's cheaper than GPT-4, faster, and good enough for document Q&A tasks. It understands context well and follows instructions strictly.

---

## **FILE DOWNLOADS**

**Q17. How do you generate downloadable files in 3 formats?**  
**Answer:**  
TXT: encode summary as UTF-8 bytes. DOCX: use `python-docx` library to create a Word document. PDF: convert HTML-formatted summary to PDF using `pdfkit` and `wkhtmltopdf`.

---

**Q18. What is pdfkit and wkhtmltopdf?**  
**Answer:**  
`pdfkit` is a Python wrapper that converts HTML to PDF. `wkhtmltopdf` is the underlying tool (installed separately) that does the actual conversion. I configured the path to its .exe file.

---

**Q19. Why do you format the summary as HTML before converting to PDF?**  
**Answer:**  
Because `pdfkit` needs HTML input. I add CSS styling (fonts, colors, spacing) to make the PDF look clean and professional with proper headings and bullets.

---

## **TECHNICAL WORKFLOW**

**Q20. Explain the end-to-end workflow for PDF summarization.**  
**Answer:**  
(1) User uploads PDF → (2) PDFPlumber extracts text → (3) Text is chunked → (4) Each chunk sent to Gemini API → (5) Summaries combined → (6) Displayed in UI → (7) User downloads in chosen format.

---

**Q21. Explain the end-to-end workflow for PDF Q&A.**  
**Answer:**  
(1) User uploads PDF → (2) Extract text and chunk it → (3) Generate embeddings with Sentence Transformers → (4) Store in FAISS index → (5) User asks question → (6) Encode question, search FAISS for top-5 chunks → (7) Send chunks + question to GPT → (8) Display answer.

---

## **DESIGN DECISIONS**

**Q22. Why use 2 different AI models (Gemini + OpenAI)?**  
**Answer:**  
Gemini is better for long-form text generation (summaries) and cheaper for large documents. OpenAI GPT is better for conversational Q&A and following strict instructions.

---

**Q23. Why use Sentence Transformers instead of OpenAI embeddings?**  
**Answer:**  
Sentence Transformers runs locally and is free. OpenAI embeddings cost money per API call. For 100+ chunks, local embeddings save costs significantly.

---

**Q24. What happens if the PDF has no text (only images)?**  
**Answer:**  
PDFPlumber returns empty text, and the app shows a warning: "Please upload a valid PDF." To handle scanned PDFs, I'd need to add OCR (like Tesseract).

---

**Q25. How would you improve this project?**  
**Answer:**  
Add OCR for scanned PDFs, support more file types (Word, images), add chat history for Q&A, deploy to cloud (Streamlit Cloud or AWS), and add user authentication for saving documents.

---

## **CODING & DEBUGGING**

**Q26. Why do you clean text by removing * and # symbols?**  
**Answer:**  
Gemini outputs Markdown formatting (like `**bold**` or `## Heading`). When exporting to TXT/DOCX/PDF, I remove these symbols so the output looks clean and professional.

---

**Q27. What is the purpose of the `chunk_text` function in the Q&A module?**  
**Answer:**  
PDFs can be very long. Splitting into smaller chunks (1000 chars) ensures each chunk has focused content, making embedding and retrieval more accurate.

---

**Q28. How does the `st.spinner()` improve user experience?**  
**Answer:**  
It shows a loading message ("Summarising...") while the API processes the request. This tells users the app is working, not frozen.

---

**Q29. Why do you use `BytesIO()` for DOCX downloads?**  
**Answer:**  
`python-docx` saves files to disk by default. BytesIO creates an in-memory file buffer, so I can generate the file and send it for download without saving it to disk.

---

**Q30. What is the role of `st.file_uploader()`?**  
**Answer:**  
It creates a file upload button in the Streamlit UI. Users can drag-and-drop or browse files. It returns a file object that I pass to PDFPlumber for text extraction.

---

## **QUICK REFERENCE SUMMARY**

### **Key Technologies:**
- **Frontend:** Streamlit
- **PDF Processing:** PDFPlumber
- **Summarization:** Google Gemini API (gemini-1.5-flash)
- **Q&A:** OpenAI GPT-4o-mini
- **Embeddings:** Sentence Transformers (all-MiniLM-L6-v2)
- **Vector Search:** FAISS
- **File Generation:** python-docx, pdfkit, wkhtmltopdf

### **Main Features:**
1. Text/PDF summarization with 3 length options
2. PDF Question & Answering with context retrieval
3. Multi-format downloads (PDF, TXT, DOCX)

### **Project Structure:**
```
├── app.py                 # Main Streamlit application
├── utils/
│   ├── pdf_utils.py      # PDF text extraction
│   ├── summarizer_utils.py # Gemini summarization
│   └── qa_utils.py       # Q&A with FAISS + OpenAI
├── requirements.txt      # Dependencies
└── README.md            # Project documentation
```

---

**Good luck with your interview! 🎯**
