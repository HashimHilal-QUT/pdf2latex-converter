import fitz  # PyMuPDF
import re


def pdf_to_latex(pdf_path: str, metadata: dict = None) -> str:
    """Parse PDF layout and generate LaTeX document code."""
    doc = fitz.open(pdf_path)

    # Document Header Setup
    title = (
        metadata.get("title", "Document Title") if metadata else "Untitled"
    )
    authors = (
        " \\and ".join(metadata.get("authors", []))
        if metadata and metadata.get("authors")
        else "Author Name"
    )

    latex_code = [
        "\\documentclass[10pt,a4paper]{article}",
        "\\usepackage[utf8]{inputenc}",
        "\\usepackage{amsmath,amssymb,amsfonts}",
        "\\usepackage{graphicx}",
        "\\usepackage{hyperref}",
        "",
        f"\\title{{{title}}}",
        f"\\author{{{authors}}}",
        "\\date{\\today}",
        "",
        "\\begin{document}",
        "\\maketitle",
        "",
    ]

    # Extract text block by block across pages
    for page_num in range(len(doc)):
        page = doc[page_num]
        # get_text("blocks") returns list of tuples: (x0, y0, x1, y1, "text", block_no, block_type)
        blocks = page.get_text("blocks")

        for b in blocks:
            text = b[4].strip()
            if not text:
                continue

            # Detect potential Section Headings (heuristic based on formatting/case)
            if len(text.split("\n")) == 1 and len(text) < 80:
                if (
                    text.isupper()
                    or re.match(r"^\d+(\.\d+)*\s+", text)
                    or "Abstract" in text
                    or "Introduction" in text
                ):
                    clean_heading = re.sub(r"^\d+(\.\d+)*\s*", "", text)
                    latex_code.append(f"\n\\section{{{clean_heading}}}\n")
                    continue

            # Escape LaTeX special characters in body text
            escaped_text = (
                text.replace("&", "\\&")
                .replace("%", "\\%")
                .replace("$", "\\$")
                .replace("#", "\\#")
                .replace("_", "\\_")
            )

            latex_code.append(f"{escaped_text}\n")

    latex_code.append("\\end{document}")
    return "\n".join(latex_code)