import json, re
from urllib.parse import urlparse
from bs4 import BeautifulSoup

# Words commonly appended to titles that should be removed
TITLE_SEPARATORS = [
    " | ",
    " - ",
    " – ",
    " — ",
    " :: ",
    " • ",
]

def clean_name(name: str) -> str:
    """Clean extracted company name."""

    if not name:
        return ""

    name = " ".join(name.split()).strip()

    for sep in TITLE_SEPARATORS:
        if sep in name:
            name =  name.split(sep)[0].strip()

    return name

def from_og_site_name(soup: BeautifulSoup) -> str | None:
    tag = soup.find("meta", property="og:site_name")
    if tag and tag.get("content"):
        return clean_name(tag["content"])

    return None

def from_application_name(soup: BeautifulSoup) -> str | None:
    tag = soup.find("meta", attrs={"name": "applciation-name"})
    if tag and tag.get("content"):
        return clean_name(tag["content"])

    return None

def from_json_ld(soup: BeautifulSoup) -> str | None:
    scripts = soup.find_all("script", type="application/ld+json")

    for script in scripts:
        if not script.string:
            continue
        try:
            data = json.loads(script.string)
        except Exception:
            continue

        objects = data if isinstance(data, list) else [data]
        for obj in objects:
            if not isinstance(obj, dict):
                continue
            obj_type = obj.get("@type")
            if obj_type in ("Organization", "Corportaion", "LocalBusiness"):
                name = obj.get("name")
                if name:
                    return clean_name(name)

    return None

def from_title(soup: BeautifulSoup) -> str | None:
    if soup.title and soup.title.string:
        return clean_name(soup.title.string)
    return None

def from_h1(soup: BeautifulSoup) -> str | None:
    h1 = soup.find("h1")
    if h1:
        return clean_name(h1.get_text())
    return None

def from_domain(url: str) -> str:
    domain = urlparse(url).netloc.lower()
    if domain.startswith("www."):
        domain = domain[4:]

    domain = domain.split(".")[0]
    domain = re.sub(r"[-_]+", " ", domain)

    return domain.title()

def extract_company_name(html: str, url: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    extractors = [
        from_og_site_name,
        from_application_name,
        from_json_ld,
        from_title,
        from_h1
    ]

    for extractor in extractors:
        try:
            result = extractor(soup)
            if result:
                return {"company_name": result}
        except Exception:
            continue

    return {"company_name": from_domain(url)}