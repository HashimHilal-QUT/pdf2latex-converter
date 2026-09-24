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

    for idx, page in enumerate(doc):
        page_text = page.get_text()
        total_text += page_text
        if idx == 0:
            first_page_text = page_text

    char_count = len(total_text.strip())
    page_count = len(doc)

    # Simple heuristic: If average characters per page is very low, it's likely scanned
    is_scanned = (char_count / max(page_count, 1)) < 100
    doi = extract_doi_from_text(first_page_text) or extract_doi_from_text(
        total_text
    )

    return {
        "page_count": page_count,
        "char_count": char_count,
        "is_scanned": is_scanned,
        "detected_doi": doi,
    }