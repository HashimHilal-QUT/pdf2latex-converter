import re

import pymupdf as fitz


def sanitize_latex_text(value: str) -> str:
    """Strip markup and escape characters that are invalid in LaTeX."""
    if value is None:
        return ""

    cleaned = re.sub(r"<[^>]+>", "", value)
    cleaned = re.sub(r"(?<=\b[A-Z])\s+(?=[a-z])", "", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    cleaned = cleaned.replace("\\", r"\textbackslash{}")
    cleaned = cleaned.replace("&", r"\&")
    cleaned = cleaned.replace("%", r"\%")
    cleaned = cleaned.replace("$", r"\$")
    cleaned = cleaned.replace("#", r"\#")
    cleaned = cleaned.replace("_", r"\_")
    cleaned = cleaned.replace("{", r"\{")
    cleaned = cleaned.replace("}", r"\}")
    return cleaned.strip()


def pdf_to_latex(pdf_path: str, metadata: dict = None) -> str:
    """Parse PDF layout and generate LaTeX document code."""
    doc = fitz.open(pdf_path)
    metadata = metadata or {}

    title = sanitize_latex_text(metadata.get("title", "Document Title")) or "Untitled"
    title = re.sub(r"\s+", " ", title).strip()
    authors = [sanitize_latex_text(author) for author in metadata.get("authors", []) if author]
    authors = [re.sub(r"\s+", " ", author).strip() for author in authors]
    author_text = " \\and ".join(authors) if authors else "Author Name"

    latex_code = [
        "\\documentclass[10pt,a4paper]{article}",
        "\\usepackage[utf8]{inputenc}",
        "\\usepackage{amsmath,amssymb,amsfonts}",
        "\\usepackage{graphicx}",
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

    try:
        for page_num in range(len(doc)):
            page = doc[page_num]
            blocks = page.get_text("blocks")

            for block in blocks:
                text = block[4].strip()
                if not text:
                    continue

                if len(text.split("\n")) == 1 and len(text) < 80:
                    if (
                        text.isupper()
                        or re.match(r"^\d+(\.\d+)*\s+", text)
                        or "Abstract" in text
                        or "Introduction" in text
                    ):
                        clean_heading = sanitize_latex_text(
                            re.sub(r"^\d+(\.\d+)*\s*", "", text)
                        )
                        latex_code.append(f"\n\\section{{{clean_heading}}}\n")
                        continue

                escaped_text = sanitize_latex_text(text)
                latex_code.append(f"{escaped_text}\n")
    finally:
        doc.close()

    latex_code.append("\\end{document}")
    return "\n".join(latex_code)


def pdf_to_markdown(pdf_path: str, metadata: dict = None) -> str:
    """Extract text from a PDF and convert it into a Markdown document."""
    doc = fitz.open(pdf_path)
    metadata = metadata or {}
    title = (metadata.get("title") or "Untitled Document").strip()

    markdown_lines = [f"# {title}", ""] if title else []

    try:
        for page_num in range(len(doc)):
            page = doc[page_num]
            blocks = page.get_text("blocks")

            for block in blocks:
                text = (block[4] or "").strip()
                if not text:
                    continue

                clean_text = re.sub(r"<[^>]+>", "", text)
                clean_text = re.sub(r"\r\n?", "\n", clean_text)
                clean_text = re.sub(r"\n{3,}", "\n\n", clean_text)

                paragraphs = [part.strip() for part in clean_text.split("\n\n") if part.strip()]

                for paragraph in paragraphs:
                    lines = [line.strip() for line in paragraph.splitlines() if line.strip()]
                    if not lines:
                        continue

                    if all(line.startswith(("- ", "* ")) for line in lines):
                        markdown_lines.extend(f"- {line[2:].strip()}" for line in lines)
                    else:
                        markdown_lines.append("\n".join(lines))

                    markdown_lines.append("")
    finally:
        doc.close()

    markdown_text = "\n".join(markdown_lines).strip()
    return markdown_text or "# Untitled Document\n\nNo extractable text was found in this PDF."