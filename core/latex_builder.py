"""LaTeX assembly helpers."""


def build_latex(document_text: str):
    """Assemble a minimal valid LaTeX document."""
    return "\\documentclass{article}\n\\usepackage[utf8]{inputenc}\n\\begin{document}\n" + document_text + "\n\\end{document}\n"
