"""PDF classification utilities."""


def classify_pdf(path: str):
    """Placeholder PDF pre-filter.

    Intended to detect whether a PDF is scanned, contains selectable text,
    or already approximates a LaTeX-native source.
    """
    return {
        "path": path,
        "kind": "unknown",
        "details": "not_implemented",
    }
