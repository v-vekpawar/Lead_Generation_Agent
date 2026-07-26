from urllib.parse import urlparse, urlunparse

PLATFORM_DOMAINS = {
    "linkedin": {"linkedin.com"},
    "facebook": {"facebook.com"},
    "instagram": {"instagram.com"},
    "twitter": {"twitter.com", "x.com"},
    "youtube": {"youtube.com", "youtu.be"},
    "github": {"github.com"},
    "medium": {"medium.com"},
    "telegram": {"t.me", "telegram.me"},
    "discord": {"discord.gg", "discord.com"},
}

def normalize_url(url: str) -> str:
    """
    Normalize a URL.
    - convert to https
    - remove query parameters
    - remove fragments
    - remove trailing slash
    """

    parsed = urlparse(url)
    scheme = "https"
    netloc = parsed.netloc.lower()

    if netloc.startswith("www."):
        netloc = netloc[4:]

    normalized = parsed._replace(
        scheme=scheme,
        netloc=netloc,
        query="",
        fragment=""
    )

    return urlunparse(normalized).rstrip("/")

def get_platform(url: str) -> str | None:
    """
    Detect which platform a url belongs to.
    """
    try:
        netloc = urlparse(url).netloc.lower()
        if netloc.startswith("www."):
            netloc = netloc[4:]

        for platform, domains in PLATFORM_DOMAINS.items():
            if any(netloc == domain or netloc.endswith("." + domain) for domain in domains):
                return platform

    except Exception:
        pass

    return None

def extract_social_links(social_links: list[str]) -> dict[str, list[str]]:
    """
    Extract supported social media links.

    Parameters
    ----------
    social_links : list[str]

    Returns
    -------
    dict

    Example

    {
        "linkedin": [...],
        "facebook": [...],
        ...
    }
    """

    result = {platform: [] for platform in PLATFORM_DOMAINS}
    seen = set()
    for url in social_links:
        try:
            normalized = normalize_url(url)
            if normalized in seen:
                continue

            seen.add(normalized)
            platform = get_platform(normalized)
            # Ignore individual Instagram content
            if platform == "instagram":
                path = urlparse(normalized).path.lower()

                if ( path.startswith("/p/") or path.startswith("/reel/") or path.startswith("/stories/") or path.startswith("/explore/") ):
                    continue

            if platform == "youtube":
                path = urlparse(normalized).path.lower()

                if ( path.startswith("/watch") or path.startswith("/playlist") or path.startswith("/results") or path.startswith("/shorts") ):
                    continue

            if platform is None:
                continue

            if normalized not in result[platform]:
                result[platform].append(normalized)

        except Exception:
            continue

    return result