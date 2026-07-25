from urllib.parse import urlparse

BLOCKED_DOMAINS = [
    "facebook.com",
    "instagram.com",
    "linkedin.com",
    "youtube.com",
    "justdial.com",
    "sulekha.com",
    "indiamart.com",
    "wikipedia.org",
    "twitter.com",
    "x.com"
]

def is_valid_company_url(url: str) -> bool:
    """
    Check whether URL is likely a company website.
    """

    if not url:
        return False

    domain = urlparse(url).netloc.lower()

    for blocked in BLOCKED_DOMAINS:
        if blocked in domain:
            return False

    return True

def filter_company_urls(results):
    filtered=[]
    seen_domains=set()
    for result in results:
        url = result.get("url")
        if is_valid_company_url(url):
            domain = urlparse(url).netloc

            if domain not in seen_domains:
                filtered.append(result)
                seen_domains.add(domain)

    return filtered