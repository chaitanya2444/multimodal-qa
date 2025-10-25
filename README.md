
# Multimodal Data Processing System - Starter Repo

This starter repository ingests PDFs, DOCX, PPTX, images, audio/video (including YouTube),
converts them to text, embeds using Gemini (free tier), stores vectors in FAISS, and answers
natural language queries via retrieval + generation.

## Quickstart

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set your Gemini API key (replace with your key):
   ```bash
   export GEMINI_API_KEY="your_gemini_key_here"
   ```
   On Windows PowerShell:
   ```powershell
   $env:GEMINI_API_KEY = "your_gemini_key_here"
   ```

4. (Optional) Install system deps:
   - tesseract-ocr (for pytesseract)
   - ffmpeg (for video/audio extraction)

5. Ingest sample data:
   ```bash
   python app/ingest.py sample_data/
   ```

6. Run the Streamlit demo:
   ```bash
   streamlit run app/main.py
   ```

## Notes
- The repo uses placeholder defaults for Gemini models and VECTOR_DIM — you may need to adjust VECTOR_DIM to match embedding size.
- This starter aims to be simple and runnable for evaluation purposes. For production usage, add batching, persistence of FAISS index, improved chunking, and robust error handling.
