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


def test_fetch_crossref_metadata_parses_response(monkeypatch):
    class DummyResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {
                "message": {
                    "title": ["Example Title"],
                    "author": [{"given": "Ada", "family": "Lovelace"}],
                    "publisher": "Example Press",
                    "container-title": ["Example Journal"],
                    "issued": {"date-parts": [[2024, 1]]},
                }
            }

    def fake_get(url, timeout):
        assert url.startswith("https://api.crossref.org/works/")
        return DummyResponse()

    monkeypatch.setattr("core.doi_fetcher.requests.get", fake_get)

    result = __import__("core.doi_fetcher", fromlist=["fetch_crossref_metadata"]).fetch_crossref_metadata(
        "10.1000/example"
    )

    assert result["title"] == "Example Title"
    assert result["authors"] == ["Ada Lovelace"]
    assert result["publisher"] == "Example Press"
    assert result["journal"] == "Example Journal"
    assert result["year"] == 2024
