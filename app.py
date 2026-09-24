import tempfile
from urllib.parse import urlparse

import streamlit as st

from core.doi_fetcher import check_arxiv_by_title_or_doi, fetch_crossref_metadata
from core.pdf_checker import analyze_pdf
from core.parser import pdf_to_latex, sanitize_latex_text


def normalize_doi(value: str):
    """Accept DOI URLs or raw DOI strings and normalize to a DOI value."""
    if value is None:
        return None

    normalized = value.strip()
    if not normalized:
        return None

    if normalized.lower().startswith(("http://", "https://")):
        parsed = urlparse(normalized)
        if "doi.org" in parsed.netloc or "dx.doi.org" in parsed.netloc:
            normalized = parsed.path.lstrip("/")
        else:
            normalized = parsed.path.strip("/")

    normalized = normalized.replace("doi:", "", 1).strip()
    return normalized


def build_doi_latex(doi: str, metadata: dict | None = None):
    """Build a minimal LaTeX document from DOI metadata when no PDF is uploaded."""
    metadata = metadata or {}
    title = sanitize_latex_text(metadata.get("title") or "Untitled")
    authors = metadata.get("authors") or ["Author Name"]
    author_text = " \\and ".join(
        sanitize_latex_text(author) for author in authors if author
    ) or "Author Name"
    journal = sanitize_latex_text(metadata.get("journal") or "Journal")
    year = metadata.get("year") or ""

    lines = [
        "\\documentclass[10pt,a4paper]{article}",
        "\\usepackage[utf8]{inputenc}",
        "\\usepackage{hyperref}",
        "",
        f"\\title{{{title}}}",
        f"\\author{{{author_text}}}",
        "\\date{\\today}",
        "",
        "\\begin{document}",
        "\\maketitle",
        "",
    ]

    if doi:
        lines.append(f"\\textbf{{DOI:}} \\url{{https://doi.org/{doi}}}")
    if journal:
        lines.append(f"\\textbf{{Journal:}} {journal} ({year})")
    lines.extend(["", "\\end{document}"])
    return "\n".join(lines)


st.title("Academic PDF to LaTeX Converter")

input_type = st.radio("Input Method", ["Upload PDF", "DOI URL/ID"])

if input_type == "Upload PDF":
    uploaded_file = st.file_uploader("Choose an Academic Paper PDF", type=["pdf"])
    if uploaded_file and st.button("Convert to LaTeX"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        st.info("Analyzing PDF structure...")
        stats = analyze_pdf(tmp_path)
        st.write(f"Pages: {stats['page_count']} | Scanned: {stats['is_scanned']}")

        metadata = {}
        doi = stats.get("detected_doi")
        if doi:
            metadata = fetch_crossref_metadata(doi) or {}

        latex_output = pdf_to_latex(tmp_path, metadata)
        st.success("Conversion Complete!")
        st.code(latex_output, language="latex")

elif input_type == "DOI URL/ID":
    doi_input = st.text_input("Enter DOI or DOI URL", value="")
    if doi_input and st.button("Fetch & Convert"):
        doi = normalize_doi(doi_input)
        if not doi:
            st.warning("Please enter a valid DOI or DOI URL.")
        else:
            st.info(f"Searching metadata for DOI: {doi}...")
            metadata = fetch_crossref_metadata(doi) or {}
            arxiv_source = check_arxiv_by_title_or_doi(
                title=metadata.get("title"), doi=doi
            )
            latex_output = build_doi_latex(doi, metadata)
            if arxiv_source:
                latex_output += "\n\\textbf{arXiv source:} \\url{" + arxiv_source + "}"
            st.success("Metadata retrieved and LaTeX generated.")
            st.code(latex_output, language="latex")