import glob
import os
from core.doi_fetcher import check_arxiv_by_title_or_doi, fetch_crossref_metadata
from core.pdf_checker import analyze_pdf

sample_files = glob.glob("samples/*.pdf") or glob.glob("*.pdf")

for sample in sample_files:
    print(f"📄 Testing DOI Fetcher for: {os.path.basename(sample)}")
    results = analyze_pdf(sample)
    doi = results["detected_doi"]

    if doi:
        print(f"   ├─ Detected DOI: {doi}")

        # Check Crossref Metadata
        meta = fetch_crossref_metadata(doi)
        if meta:
            print(f"   ├─ Title: {meta['title']}")
            print(
                f"   ├─ Authors: {', '.join(meta['authors'][:3])}{'...' if len(meta['authors']) > 3 else ''}"
            )
            print(f"   ├─ Journal: {meta['journal']} ({meta['year']})")

        # Check arXiv TeX source availability
        arxiv_source = check_arxiv_by_title_or_doi(
            title=meta.get("title") if meta else None, doi=doi
        )
        print(
            f"   └─ arXiv LaTeX Source URL: {arxiv_source or 'Not available on arXiv'}"
        )
    else:
        print("   └─ No DOI detected.")

    print("-" * 60)