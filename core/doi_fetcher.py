import urllib.parse
import xml.etree.ElementTree as ET

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
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        entry = root.find("atom:entry", ns)
        if entry is not None:
            arxiv_id = entry.find("atom:id", ns).text.split("/abs/")[-1]
            return f"https://arxiv.org/e-print/{arxiv_id}"

    return None


def fetch_crossref_metadata(doi: str) -> dict | None:
    """Fetch structured bibliographic metadata from Crossref."""
    encoded_doi = urllib.parse.quote(doi, safe="")
    url = f"https://api.crossref.org/works/{encoded_doi}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        message = response.json().get("message", {})

        title = ""
        if isinstance(message.get("title"), list) and message.get("title"):
            title = message["title"][0]

        authors = []
        for author in message.get("author", []):
            given = author.get("given", "").strip()
            family = author.get("family", "").strip()
            if given and family:
                authors.append(f"{given} {family}")
            elif family:
                authors.append(family)
            elif given:
                authors.append(given)

        journal = ""
        container_title = message.get("container-title", [])
        if isinstance(container_title, list) and container_title:
            journal = container_title[0]

        year = None
        issued = message.get("issued", {})
        date_parts = issued.get("date-parts", [[None]])
        if date_parts and date_parts[0]:
            year = date_parts[0][0]

        return {
            "title": title,
            "authors": authors,
            "publisher": message.get("publisher"),
            "journal": journal,
            "year": year,
        }
    except requests.RequestException as exc:
        print(f"Crossref lookup failed for DOI {doi}: {exc}")
        return None