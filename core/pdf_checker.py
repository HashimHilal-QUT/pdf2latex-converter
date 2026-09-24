import fitz  # PyMuPDF

def analyze_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    total_text = ""
    for page in doc:
        total_text += page.get_text()
    
    is_scanned = len(total_text.strip()) < 100
    return {
        "page_count": len(doc),
        "is_scanned": is_scanned,
        "char_count": len(total_text)
    }