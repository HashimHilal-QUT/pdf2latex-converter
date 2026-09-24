import pymupdf as fitz

from core.pdf_checker import analyze_pdf


def test_analyze_pdf_detects_text_and_doi(tmp_path):
    pdf_path = tmp_path / "sample.pdf"
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "This paper studies a DOI: 10.1000/example123.")
    doc.save(pdf_path)
    doc.close()

    result = analyze_pdf(str(pdf_path))

    assert result["page_count"] == 1
    assert result["char_count"] > 0
    assert result["is_scanned"] is False
    assert result["detected_doi"] == "10.1000/example123"
