import os
from core.doi_fetcher import fetch_crossref_metadata
from core.parser import pdf_to_latex
from core.pdf_checker import analyze_pdf

sample_pdf = "samples/URBANR~1.PDF"  # Replace with any of your samples

print(f"🚀 Processing: {sample_pdf}")
analysis = analyze_pdf(sample_pdf)
doi = analysis["detected_doi"]

metadata = {}
if doi:
    print(f"Fetching metadata for DOI: {doi}...")
    metadata = fetch_crossref_metadata(doi) or {}

print("Converting PDF to LaTeX...")
latex_output = pdf_to_latex(sample_pdf, metadata)

# Save to a .tex file
output_path = "output_test.tex"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(latex_output)

print(f"✅ Successful! TeX code written to {output_path}")
print("\n--- Preview of generated LaTeX (First 30 lines) ---")
print("\n".join(latex_output.split("\n")[:30]))