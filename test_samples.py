import glob
import os
from core.pdf_checker import analyze_pdf

# Path to your sample PDFs (adjust path if your samples are in a subfolder)
sample_files = glob.glob("samples/*.pdf") or glob.glob("*.pdf")

if not sample_files:
    print(
        "No sample PDFs found! Please place a sample PDF in the directory to test."
    )
else:
    print(f"Found {len(sample_files)} sample paper(s):\n")
    for sample in sample_files:
        results = analyze_pdf(sample)
        print(f"📄 File: {os.path.basename(sample)}")
        print(f"   ├─ Total Pages: {results['page_count']}")
        print(f"   ├─ Character Count: {results['char_count']}")
        print(f"   ├─ Is Scanned?: {results['is_scanned']}")
        print(f"   └─ Detected DOI: {results['detected_doi'] or 'None found'}")
        print("-" * 50)