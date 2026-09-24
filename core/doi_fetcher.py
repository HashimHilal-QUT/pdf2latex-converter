"""Utilities for looking up metadata from DOI or arXiv sources."""


def fetch_metadata(identifier: str):
    """Placeholder for DOI/arXiv metadata retrieval.

    This should eventually query Crossref or arXiv and return contextual
    metadata needed for conversion decisions.
    """
    return {
        "identifier": identifier,
        "title": None,
        "source": "not_implemented",
    }
