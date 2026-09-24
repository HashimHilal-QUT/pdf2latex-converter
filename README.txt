PDF2LaTeX Converter

Project overview:
This project turns academic PDFs into a lightweight LaTeX document structure by checking the PDF content, detecting metadata such as DOI and journal information, and preparing a LaTeX export for downstream editing.

Requirements:
- Python 3.11+
- pip
- Optional: virtual environment

Local installation:
1. Create a virtual environment:
   python -m venv .venv
2. Activate it:
   . .venv/bin/activate
3. Install dependencies:
   python -m pip install -r requirements.txt
4. Run the app:
   streamlit run app.py

Notes for Streamlit Cloud / Streamlit.app:
- This app does not require a GPU.
- It runs on CPU-only infrastructure because the current workflow uses PDF parsing and metadata fetching, not deep-learning OCR or large-model inference.
- No Colab notebook is required for deployment.
- For future AI/OCR upgrades, GPU may help but is not necessary for the current version.

Optional system packages:
The project also includes packages.txt for system-level dependencies that may be useful if you later add OCR or desktop PDF tooling.
