import os
from pathlib import Path

from core.doi_fetcher import check_arxiv_by_title_or_doi, fetch_crossref_metadata
from core.pdf_checker import analyze_pdf

ROOT = Path(__file__).resolve().parent
sample_dir = ROOT / "samples"

sample_files = []
if sample_dir.exists():
    sample_files.extend(
        p for p in sample_dir.rglob("*") if p.is_file() and p.suffix.lower() == ".pdf"
    )

if not sample_files:
    sample_files.extend(
        p for p in ROOT.glob("*") if p.is_file() and p.suffix.lower() == ".pdf"
    )

for sample in sorted(sample_files):
    print(f"📄 Testing DOI Fetcher for: {os.path.basename(sample)}")
    results = analyze_pdf(str(sample))
    doi = results["detected_doi"]

    if doi:
        print(f"   ├─ Detected DOI: {doi}")

        meta = fetch_crossref_metadata(doi)
        if meta:
            print(f"   ├─ Title: {meta['title']}")
            authors = meta.get("authors") or []
            print(
                f"   ├─ Authors: {', '.join(authors[:3])}{'...' if len(authors) > 3 else ''}"
            )
            print(f"   ├─ Journal: {meta.get('journal', '')} ({meta.get('year')})")

        arxiv_source = check_arxiv_by_title_or_doi(
            title=meta.get("title") if meta else None, doi=doi
        )
        print(
            f"   └─ arXiv LaTeX Source URL: {arxiv_source or 'Not available on arXiv'}"
        )
    else:
        print("   └─ No DOI detected.")

    print("-" * 60)