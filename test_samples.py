import os
from pathlib import Path

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

if not sample_files:
    print(
        "No sample PDFs found! Please place a sample PDF in the directory to test."
    )
else:
    print(f"Found {len(sample_files)} sample paper(s):\n")
    for sample in sorted(sample_files):
        results = analyze_pdf(str(sample))
        print(f"📄 File: {os.path.basename(sample)}")
        print(f"   ├─ Total Pages: {results['page_count']}")
        print(f"   ├─ Character Count: {results['char_count']}")
        print(f"   ├─ Is Scanned?: {results['is_scanned']}")
        print(f"   └─ Detected DOI: {results['detected_doi'] or 'None found'}")
        print("-" * 50)