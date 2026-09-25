# Papers 4 AI

Transform research papers into clean, editable LaTeX and Markdown with AI-ready precision.

## Live app

https://papers-4-ai.streamlit.app/

<img src="https://myresearchdata.blob.core.windows.net/academic/Academic_Dude.webp" alt="Papers 4 AI" width="28%" />

## Overview

Papers 4 AI is a lightweight Streamlit application that takes an academic PDF and converts it into two usable formats:

- LaTeX (`.tex`)
- Markdown (`.md`)

The app is designed for researchers, students, and AI workflows that need a fast way to turn PDFs into editable text that can be reused in notebooks, prompts, documentation, and technical writing.

## How it works

1. Upload an academic paper PDF.
2. The app analyzes the file to report page count and whether the PDF appears scanned.
3. It extracts the readable text from the document.
4. It generates both LaTeX and Markdown output side by side.
5. You can review the content and download either file directly.

## Features

- PDF upload interface for academic papers
- Extracts selectable text from uploaded PDFs
- Generates editable LaTeX output
- Generates Markdown output
- Displays both outputs in the browser for comparison
- Download buttons for `.tex` and `.md` files
- Reports PDF metadata such as page count and scan status
- CPU-only setup with no GPU required

## Disclaimer

This app is a conversion tool only. It does not store user data, and it does not retrieve full-text files from DOI URLs or publisher systems. Some PDFs may be locked behind publisher paywalls or may not contain fully extractable text.

## Local development

### Requirements

- Python 3.11+
- pip
- CPU-only environment

### Run locally

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

Then open the local Streamlit URL in your browser, upload a PDF, and click Convert.

## Deployment

This project is designed to run on Streamlit Community Cloud.

1. Push the repository to GitHub.
2. In Streamlit Community Cloud, choose Create app.
3. Select the repository and branch.
4. Set `app.py` as the main file.
5. Deploy.

## Project structure

- `app.py` - Streamlit app interface
- `core/parser.py` - LaTeX and Markdown conversion logic
- `core/pdf_checker.py` - PDF analysis and validation
- `core/doi_fetcher.py` - retained utility for optional metadata-related work
- `requirements.txt` - Python dependencies
- `packages.txt` - intentionally empty for this app
- `tests/` - automated regression tests

## Quote

> Are you thinking what I am thinking? We both know what this tool will be used for!

## Copyright

© 2026 Made by AI for AI

Disclaimer: No data is stored in this app; it is just a conversion tool.
