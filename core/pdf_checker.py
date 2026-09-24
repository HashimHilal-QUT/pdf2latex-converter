import re
import fitz  # PyMuPDF


def extract_doi_from_text(text: str) -> str | None:
    """Search for standard DOI patterns in extracted text."""
    doi_regex = r"\b10\.\d{4,9}/[-._;()/:A-Za-z0-9]+\b"
    match = re.search(doi_regex, text)
    return match.group(0) if match else None


def analyze_pdf(pdf_path: str) -> dict:
    """Analyze PDF structure to check searchability and look for DOI."""
    doc = fitz.open(pdf_path)
    total_text = ""
    first_page_text = ""
    page_count = doc.page_count

    try:
        for idx, page in enumerate(doc):
            page_text = page.get_text()
            total_text += page_text
            if idx == 0:
                first_page_text = page_text
    finally:
        doc.close()

    char_count = len(total_text.strip())
    has_extractable_text = bool(total_text.strip())

    # If a PDF contains selectable text, it is not a scanned image-only document.
    is_scanned = not has_extractable_text
    doi = extract_doi_from_text(first_page_text) or extract_doi_from_text(
        total_text
    )

    return {
        "page_count": page_count,
        "char_count": char_count,
        "is_scanned": is_scanned,
        "detected_doi": doi,
    }