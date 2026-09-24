# PDF2LaTeX Converter

A lightweight Streamlit application for analyzing academic PDFs, extracting DOI metadata, and preparing a LaTeX export.

## Features
- Upload a PDF from the browser
- Detect basic PDF structure and text presence
- Extract DOI metadata from the PDF text
- Query Crossref for paper metadata
- Check arXiv availability for TeX source links
- Generate a LaTeX document skeleton

## Requirements
- Python 3.11+
- pip
- A normal CPU-only environment is enough for the current application

## Local setup
```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

## Streamlit Cloud / Streamlit.app
This app can run on Streamlit Community Cloud without a GPU.

The current project relies on:
- PDF parsing with PyMuPDF
- metadata lookup with requests
- the Streamlit web interface

No GPU or Colab notebook is required for the current version.

## Optional future upgrades
If you later add heavy OCR, AI extraction, or large model inference, GPU support may become useful. For now, CPU-only hosting is sufficient.

## Files included
- `app.py` — Streamlit interface
- `core/` — PDF checking, metadata lookup, parsing, and LaTeX generation
- `samples/` — sample PDFs for testing
- `tests/` — automated checks
- `requirements.txt` — Python dependencies
- `packages.txt` — optional system-level dependencies
