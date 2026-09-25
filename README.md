# PDF2LaTeX Converter

A CPU-only Streamlit app that converts an uploaded academic PDF into both LaTeX and Markdown. The app shows the two results side by side and provides a download button for each file.

## Site URL

https://papers-4-ai.streamlit.app/

![Academic Dude](https://github.com/HashimHilal-QUT/pdf2latex-converter/blob/main/Academic_Dude.JPG?raw=true)

## Features

- Extracts selectable PDF text with PyMuPDF.
- Generates a basic editable LaTeX document.
- Generates Markdown from the extracted PDF text.
- Displays `.tex` and `.md` output previews in the browser.
- Downloads the generated files as `converted.tex` and `converted.md`.
- Reports page count and whether the PDF contains extractable text.

This project works from PDFs supplied by the user. It does not retrieve full-text source files from DOI URLs. Commercial publishers may keep PDFs and source files behind paywalls, and a DOI alone does not guarantee access to editable LaTeX.

## Requirements

- Python 3.11 or newer
- pip
- CPU-only environment

No GPU, Colab notebook, OCR engine, Poppler installation, or API key is required for the current workflow.

## Run locally

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

Open the local URL printed by Streamlit, upload a PDF, and select **Convert**.

## Deploy on Streamlit Community Cloud

1. Push this repository to GitHub.
2. In Streamlit Community Cloud, choose **Create app**.
3. Select the repository, branch, and `app.py` as the main file.
4. Deploy the app.

Streamlit Cloud installs Python dependencies from `requirements.txt`. The `packages.txt` file is intentionally empty because this app has no required Linux system packages. The app is suitable for standard CPU hosting and does not need a secrets configuration.

## Test before publishing

Run the automated tests locally:

```bash
. .venv/bin/activate
pytest -q
```

Compile-check the application modules:

```bash
python -m py_compile app.py core/parser.py core/pdf_checker.py core/doi_fetcher.py
```

## Project files

- `app.py` - Streamlit interface and download controls
- `core/parser.py` - LaTeX and Markdown conversion
- `core/pdf_checker.py` - PDF analysis
- `core/doi_fetcher.py` - retained network utility for optional metadata scripts; not used by the app UI
- `tests/` - automated regression tests
- `requirements.txt` - Python dependencies for local and Streamlit deployment
- `packages.txt` - intentionally empty system dependency file
