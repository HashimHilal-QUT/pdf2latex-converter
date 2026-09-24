import urllib.parse
import xml.etree.ElementTree as ET
from habanero import Crossref
import requests


def check_arxiv_by_title_or_doi(title: str = None, doi: str = None) -> str | None:
    """Check if the paper exists on arXiv to fetch direct TeX source files."""
    base_url = "http://export.arxiv.org/api/query?"
    query = ""

    if doi:
        query = f'doi:"{doi}"'
    elif title:
        query = f'ti:"{title}"'
    else:
        return None

    params = {"search_query": query, "start": 0, "max_results": 1}
    response = requests.get(base_url, params=params, timeout=10)

    if response.status_code == 200:
        root = ET.fromstring(response.content)
        # Atom feed namespace
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        entry = root.find("atom:entry", ns)
        if entry is not None:
            arxiv_id = entry.find("atom:id", ns).text.split("/abs/")[-1]
            return f"https://arxiv.org/e-print/{arxiv_id}"

    return None


def fetch_crossref_metadata(doi: str) -> dict | None:
    """Fetch structured bibliographic metadata from Crossref."""
    cr = Crossref()
    try:
        res = cr.works(ids=doi)
        message = res.get("message", {})
        return {
            "title": message.get("title", [""])[0],
            "authors": [
                f"{a.get('given', '')} {a.get('family', '')}"
                for a in message.get("author", [])
            ],
            "publisher": message.get("publisher"),
            "journal": message.get("container-title", [""])[0],
            "year": message.get("issued", {})
            .get("date-parts", [[None]])[0][0],
        }
    except Exception as e:
        print(f"Crossref lookup failed for DOI {doi}: {e}")
        return None